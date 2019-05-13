#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "sepp.heid@t-online.de"
__doc__ = """ """

from poorscrum import Poorscrum_Tasks, Status, burndown_as_image, story_points, __version__

from shutil import copy2

from jinja2 import Template

import configparser

import argparse
import os
import sys

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(sys.argv[0]))

HYPER = '<a href="http://sot2222.eu.eurocopter.corp/index.php?pagename='
PRHYPER = HYPER + 'pr&id={}" target="_blank">PR {}/</a>'
ECRHYPER = HYPER + 'ecr&id={}" target="_blank">ECR {}/</a>'


""" Directory with the rendering templates for jinja2 """
TEMPLATES = os.path.join(os.path.dirname(__file__), "poorjinja")
          
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
    """ Returns a key value pairs from an existing story file as a story and
    task dictionary
    """
    
    story = configparser.ConfigParser()
    story.read(from_story_file)
    
    return dict((s.replace(' ', '_'), story.get(s, "text")) 
                  for s in story.sections() if s != "tasks"), \
                  dict((o, story.get("tasks", o))
                       for o in story.options("tasks"))


def read_file_as_template(from_template_file_name):
    """ Returns a template from an existing template file
    """
    try:
        with open(from_template_file_name, 'r') as template:
            return Template(template.read())
    except:
        return None

def write_story_as_html_file(from_story_dict, from_devs_list, from_tasks_list,
                             template, html_file_name):
    """ Writes a story html file from an existing template file
    """
    
    with open(html_file_name, 'w') as html:
        html.write(template.render(story=from_story_dict,
                                   devs=from_devs_list,
                                   tasks=from_tasks_list))

    return True


def write_index_as_html_file(from_dict, template, index_file_name):
    """ Writes a index html file from an existing template file
    """
    
    with open(index_file_name, 'w') as index:
        index.write(template.render(index=from_dict))

    return True


def get_work_todo(story_as_dict, total_work_edited, total_work_todo):        
    
    story_size_all  = story_as_dict['size_1']
    story_size_all += ' ' + story_as_dict['size_2']
    story_size_all += ' ' + story_as_dict['size_3']
    story_size_all += ' ' + story_as_dict['size_4']

    story_work_todo = story_size_all.split()
    story_work_edited = len(story_size_all.split())

    if story_work_edited == 0: ## no editing yet
        return None, None
    
    if story_work_edited > 1: ## real work done, not only estimate
        total_work_edited = min(total_work_edited, story_work_edited)

    for day in range(story_work_edited):
        total_work_todo[day] += int(story_work_todo[day])
    for day in range(story_work_edited, len(total_work_todo)):
        total_work_todo[day] += int(story_work_todo[-1])

    return total_work_edited, total_work_todo


def patch_reference_for_html(from_string):
    """
    Patch the reference from the config format to the html format
    """
    
    patch = ""

    old = ''
    in_hlink = False
    in_first = True
    for new in from_string:
        if in_hlink: ## in hyperlink text
            if new == '>' :
                in_hlink = False                
                if old == '/':
                    patch += "</a>"
                    in_first = True
                else:
                    patch += '" target="_blank">'
                    in_first = False
            elif new == '/':
                if in_first:
                    patch += new 
            else:
                patch += new 
                
        else: ## standard text

            if new == '<':
                in_hlink = True
                if in_first:
                    patch += '<a href="'
            else:
                patch += new 

        old = old if new.isspace() else new  ## Transitions without space

    return patch

def expand_reference_for_html(from_string):
    """
    Expand the reference from the config automatically for PRs and ECRs
    """
    reports = from_string.split()
    prs = [index for index, item in enumerate(reports) if item.upper() in "PR"]
    ecrs = [index for index, item in enumerate(reports) if item.upper() == "ECR"]

    expand = ""
    for index in prs:
        expand += PRHYPER.format(reports[index+1], reports[index+1])
    for index in prs:
        expand += ECRHYPER.format(reports[index+1], reports[index+1])
           
    return expand


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
        logger.error("Directory '{}' for story pages does not exist."
                     .format(templates_dir))
        return 7
    
    story_template_file = os.path.join(templates_dir, "poorstory_template.jinja2")
    story_template = read_file_as_template(story_template_file)
    if story_template is None:
        logger.error("Template file is illegal '{}'.".format(story_template_file))
        return 8


    status_index_template_file = os.path.join(templates_dir, "poorstatus_template.jinja2")
    status_index_template = read_file_as_template(status_index_template_file)
    if status_index_template is None:
        logger.error("Template file is illegal '{}'.".format(status_index_template_file))
        return 9

    devs_index_template_file = os.path.join(templates_dir, "poordevs_template.jinja2")
    devs_index_template = read_file_as_template(devs_index_template_file)
    if devs_index_template is None:
        logger.error("Template file is illegal '{}'.".format(devs_index_template_file))
        return 9


    """ Copy the CSS file into the html structure """

    copy2( os.path.join(TEMPLATES, "poorindex_style.css"), args.to_html_dir[0])
    copy2( os.path.join(TEMPLATES, "poorstory_style.css"), stories_dir)
    
    
    """ Convert all provided story files to html pages """

    logger.info("Directory for story pages is '{}'.".format(stories_dir))


    """ ------------------------------------------------------------------- """

    """ create a dictionary with story states as keys for indices """

    status_as_dict = {}
    devs_as_dict = {}

    total_work_edited = 20
    total_work_todo = total_work_edited*[0]
    
    """ Create and write all story files """
    
    for story_file in args.from_text:

        logger.info("Processing '{}'.".format(story_file))

        story_as_dict, tasks_as_dict = read_story_as_dict(story_file)
        if story_as_dict is None or tasks_as_dict is None:
            logger.error("Story file is illegal '{}'.".format(story_file))
            continue


        story_html_file = os.path.splitext(os.path.basename(story_file))[0]+".html"
        story_html_file = os.path.join(stories_dir, story_html_file)
        
        if args.dry:
            logger.info("Would save html to '{}' .".format(story_html_file))
            continue

        tasks_as_list = [value.split(',') for value in tasks_as_dict.values()]
        devs_as_list = list(set(task[4] for task in tasks_as_list[:-1]
                                if task[4] != "<dev>" and int(task[2])>0))

        story_as_dict['reference'] = story_as_dict['reference'].strip()
        if story_as_dict['reference'].startswith('<'):
            story_as_dict['reference'] = patch_reference_for_html(story_as_dict['reference'])
        elif story_as_dict['reference'] != "":
            story_as_dict['reference'] = expand_reference_for_html(story_as_dict['reference'])
            
        
        if not write_story_as_html_file(story_as_dict, devs_as_list, tasks_as_list,
                                        story_template, story_html_file):
            logger.error("Story html file writing failed '{}'.".format(story_html_file))
            continue
        
        logger.info("Story html file writing succeeded '{}'.".format(story_html_file))
        

        """ Determine html path relative to root """
        
        story_html_path = os.path.join(
            os.path.split(stories_dir)[-1], # from root
            os.path.split(story_html_file)[-1])

        """ Fill the status dictionary for the story pages """

        if not (story_as_dict['status'] in status_as_dict):
            status_as_dict[story_as_dict['status']] = []
        status_as_dict[story_as_dict['status']].append(
            [story_as_dict['id'], story_html_path])


        """
        Fill the devs dictionary if devs are given for the task page. A story
        may be allocated to several developers.
        """

        if story_as_dict['devs'] != "" and \
               story_as_dict['status'] in  ["ANALYSING", "commited", "SPRINTING"]:

            for dev in devs_as_list:
                if not (dev in devs_as_dict):
                    devs_as_dict[dev] = []
                devs_as_dict[dev].append(
                    [story_as_dict['id'], story_html_path])

            """ Input for burndown """

            total_work_edited, total_work_todo = get_work_todo(
                story_as_dict, total_work_edited, total_work_todo)
            if total_work_edited is None or total_work_todo is None: 
                logger.error("Sizes are not entered '{}'.".format(story_html_file))
                return 10

    """ ------------------------------------------------------------------- """

    """ Create and write the index files """
    
    if not args.dry:
        status_index_html_file = "status_index.html"
        status_index_html_file = os.path.join(args.to_html_dir[0], status_index_html_file)
        if not write_index_as_html_file(status_as_dict, status_index_template,
                                        status_index_html_file):
            logger.error("Status index html file writing failed '{}'."
                         .format(status_index_html_file))
        else:
            logger.info("Status index html file writing succeeded '{}'."
                        .format(status_index_html_file))


        copy2(burndown_as_image(total_work_edited, total_work_todo), args.to_html_dir[0])

        devs_index_html_file = "devs_index.html"
        devs_index_html_file = os.path.join(args.to_html_dir[0], devs_index_html_file)
        if not write_index_as_html_file(devs_as_dict, devs_index_template, devs_index_html_file):
            logger.error("Devs_index html file writing failed '{}'."
                         .format(devs_index_html_file))
        else:
            logger.info("Devs_index html file writing succeeded '{}'."
                        .format(devs_index_html_file))

    return 0

        
if __name__ == "__main__":
    sys.exit(main())

