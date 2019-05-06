#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "sepp.heid@t-online.de"
__doc__ = """ """

from poorscrum import Poorscrum_Tasks, Status, story_points, __version__

from shutil import copy2

from jinja2 import Template

import configparser

import argparse
import os
import sys

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(sys.argv[0]))

""" Directory with the rendering templates for jinja2 """
TEMPLATES = "poorjinja"
          
def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        prog = os.path.basename(sys.argv[0]),
        description ="Converts the story files from config format to html pages",
        epilog = "Ensure the root directory for 'stories' directory exists!")

    parser.add_argument("--version", action="version", version=__version__)

    parser.add_argument("--dry", required=False,
                        action="store_true", 
                        help="Do not save the presentation")

    parser.add_argument("to_html_dir", nargs=1, 
                        help="PPTX file to import the story slides to")

    parser.add_argument("from_text", nargs="+", 
                        help="Text files with story content")

    return parser.parse_args()


def read_story_as_dict(from_story_file):
    """ Returns a key value pairs from an existing story file as dictionary
    """
    
    story = configparser.ConfigParser()
    story.read(from_story_file)
    
    kv = dict((s.replace(' ', '_'), story.get(s, "text")) 
                  for s in story.sections() if s != "tasks")
    kv.update((o, story.get("tasks", o))
                  for o in story.options("tasks"))

    return kv

    
def read_file_as_template(from_template_file_name):
    """ Returns a template from an existing template file
    """

    try:
        with open(from_template_file_name, 'r') as template:
            return Template(template.read())
    except:
        return None

def write_dict_as_html_file(from_dict, template, html_file_name):
    """ Returns a template from an existing template file
    """
    
    with open(html_file_name, 'w') as html:
        html.write(template.render(story=from_dict))

    return True

def import_tasks(from_tasks, to_prs):
    """ Imports the tasks items for a tasks slide
    """

    """!!! Our tasks layout is always the one before the story layout !!!"""
    tasks_slide_layout = to_prs.slide_layouts[-2]
    to_slide = to_prs.slides.add_slide(tasks_slide_layout)
    to_table = Poorscrum_Tasks(to_slide, to_prs.slide_height, to_prs.slide_width)
    lastrow = len(to_table.table.rows)-1
    
    try:
        tasks = from_tasks.items("tasks")
    except:
        return None

    wstart, wleft, wdone = 0, 0, 0
    for row, task in enumerate(tasks):
        if row < lastrow:
            # Calculate all rows
            data = task[1].split(',')
            wstart += int(data[1]) 
            wleft += int(data[2])
            wdone += int(data[3])
            # Output leading tasks only
            to_table.put_as_row(row, data)

    # Fibonacci!
    total = ["Total",
             str(story_points(wstart)),
             str(story_points(wleft)),
             str(story_points(wdone)), "Points"]
    to_table.put_as_row(lastrow, total)
        
    return to_slide


def main():
    args = parse_arguments()

    if args.to_html_dir is None:
        logger.error("Must provide root directory for html pages!")
        return 1

    if args.from_text is None:
        logger.error("Must provide TEXT backlog files for input!")
        return 2

    if not os.path.isdir(args.to_html_dir[0]):
        logger.error("Root directory '{}' for 'stories' directory does not exist."
                     .format(args.to_html_dir[0]))
        return 3

    stories_dir = os.path.join(args.to_html_dir[0], "stories")
    if not os.path.isdir(stories_dir):
        logger.error("Directory 'stories' for story pages does not exist under '{}'."
                     .format(args.to_html_dir[0]))
        return 4


    """ Check the names of story files """
    
    for story_file in args.from_text:
        name, ext = os.path.splitext(os.path.basename(story_file))

        if ext != ".story":
            logger.error("Must provide story file names with '.story' extension!")
            return 5

        try:
            num = int(name.split('_')[0])
        except:
            logger.error("Must provide story file names with leading digits!")
            return 6


    """ Check templates """
        
    templates_dir = TEMPLATES
    if not os.path.isdir(templates_dir):
        logger.error("Directory 'templates' for story pages does not exist  under '{}'."
                     .format(args.to_html_dir[0]))
        return 7
    
    template_file = os.path.join(templates_dir, "poorstory_template.jinja2")
    template = read_file_as_template(template_file)
    if template is None:
        logger.error("Template file is illegal '{}'.".format(template_file))
        return 8


    """ Copy the CSS file intor the stories directory """
    
    copy2( os.path.join(TEMPLATES, "poorstory_style.css"), stories_dir)
    
    
    """ Convert all provided story files to html pages """

    logger.info("Directory for story pages is '{}'.".format(stories_dir))

    for story_file in args.from_text:

        logger.info("Processing '{}'.".format(story_file))

        story_as_dict = read_story_as_dict(story_file)
        if story_as_dict is None:
            logger.error("Story file is illegal '{}'.".format(story_file))
            continue

        html_file = os.path.splitext(os.path.basename(story_file))[0]+".html"
        html_file = os.path.join(stories_dir, html_file)
        
        if args.dry:
            logger.info("Would save html to '{}' .".format(html_file))
            continue

        if not write_dict_as_html_file(story_as_dict, template, html_file):
            logger.error("Html file writing failed '{}'.".format(html_file))
            continue
        
        logger.info("Html file writing succeeded '{}'.".format(html_file))
        
    return 0

        
if __name__ == "__main__":
    sys.exit(main())

