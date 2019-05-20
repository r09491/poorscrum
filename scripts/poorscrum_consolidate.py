#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "sepp.heid@t-online.de"
__doc__ = """ """

import poorscrum
from poorscrum import __version__
from poorscrum.poorscrum_config import SPRINT_FILE
from poorscrum.poorscrum_tools import story_points
from poorscrum.poorscrum_sprint import *
from poorscrum.poorscrum_plot import *

from shutil import copy2

from jinja2 import Template

import configparser

import argparse
import os
import sys

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(sys.argv[0]))

          
def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        prog = os.path.basename(sys.argv[0]),
        description ="Consolidate the story files in config format",
        epilog = "Ensure the root directory for 'stories' directory exists!")

    parser.add_argument("--version", action="version", version=__version__)

    parser.add_argument("--dry", required=False,
                        action="store_true", 
                        help="Do not save the consolidated stories")

    parser.add_argument('--sprint_day', default=0,
                        help='The day in the sprint for consolidation')

    parser.add_argument('--sprint_file', default=SPRINT_FILE,
                        help='SCRUM sprint setup file')

    parser.add_argument("from_text", nargs="+", 
                        help="Text files with story content")

    return parser.parse_args()


def read_story_as_dict(from_story_file):
    """ Returns the key value pairs from an existing story file as a story and
    task dictionary
    """
    
    story = configparser.ConfigParser()
    story.read(from_story_file)
    
    return dict((s, story.get(s, "text")) 
                for s in story.sections() if s != "tasks"), \
                dict((o, story.get("tasks", o))
                     for o in story.options("tasks"))

def write_story_from_dict(to_story_file, story_as_dict, tasks_as_dict):
    """ 
    """
    
    story = configparser.ConfigParser()
    story.read(to_story_file)

    """ Traverse the story dict and set text """
    for key, value in story_as_dict.items():
        story.set(key, "text", value)

    """ Traverse the task dict and set options """
    for key, value in tasks_as_dict.items():
        story.set("tasks", key, value)
        
    with open(to_story_file, 'w') as storyfile:
            story.write(storyfile)
    
    return to_story_file


def reset_task_points(tasks_as_dict):
    """
    Set tasks to in initial estimated during planing states
    """
    
    """ Filter edited classes """
    tasks = [(key, value.split(',')) for key, value in tasks_as_dict.items()]
    total_key, total_values = tasks[-1]
    tasks = [task for task in tasks[:-1] if '<' + task[0] + '>' != task[1][0]]
    tasks = [task for task in tasks if int(task[1][1]) > 0]

    total_plan = 0
    for estimate in tasks:
        key, (what, plan, todo, done, dev) = estimate
        tasks_as_dict[key] =  ','.join([what, plan, plan, "0", dev])
        total_plan += int(plan)
    total_plan = story_points(total_plan)
    tasks_as_dict[total_key] = ','.join(["Total",
                                         str(total_plan), str(total_plan), "0",
                                         "Points"])

    return tasks_as_dict


def consolidate_task_points(tasks_as_dict):
    """
    Consolidate task points
    """

    """ Filter edited classes """
    tasks = [(key, value.split(',')) for key, value in tasks_as_dict.items()]
    total_key, total_values = tasks[-1]
    tasks = [task for task in tasks[:-1] if '<' + task[0] + '>' != task[1][0]]
    tasks = [task for task in tasks if int(task[1][1]) > 0]

    total_plan, total_todo, total_done = 0, 0, 0
    for estimate in tasks:
        key, (what, plan, todo, done, dev) = estimate
        plan, todo, done = int(plan), int(todo), int(done)
        done = plan - todo if plan >= todo else plan
        ## Regular story points for normal rows
        tasks_as_dict[key] =  ','.join([what, str(plan), str(todo), str(done), dev])
        total_plan += plan
        total_todo += todo
        total_done += done    
    ## Fibonacci story points for total rows
    total_plan, total_todo = story_points(total_plan), story_points(total_todo)
    tasks_as_dict[total_key] = ','.join(["Total", str(total_plan),
                                         str(total_todo), str(total_done), "Points"])

    return tasks_as_dict


def reset_stories(story_as_dict, tasks_as_dict):
    tasks_as_dict = reset_task_points(tasks_as_dict)

    story_as_dict = story_as_dict
    
    return story_as_dict, tasks_as_dict

    
def consolidate_stories(story_as_dict, tasks_as_dict):
    tasks_as_dict = consolidate_task_points(tasks_as_dict)

    story_as_dict = story_as_dict

    return story_as_dict, tasks_as_dict
    

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


def main():
    args = parse_arguments()

    if args.from_text is None:
        logger.error("Must provide TEXT backlog files for input!")
        return 1

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


    """ Read the sprint properties """

    days, periods, points = read_sprint_properties(args.sprint_file)
    if days is None:
        logger.info("Using MAX values for sprint properties.")
        days, periods, points = MAX_POINTS, MAX_PERIODS, MAX_POINTS


    logger.info("The sprint length is '{:d}' days."
                .format(days))
    logger.info("The sprint has '{:d}' periods with '{:d}' working days."
                .format(periods, int(days/periods)))
    logger.info("The team has a capacity '{:d}' story points."
                .format(points))


    """ ------------------------------------------------------------------- """

    """ create a dictionary with story states as keys for indices """

    status_as_dict = {}
    devs_as_dict = {}

    ## total_work_edited = days
    ## total_work_todo = total_work_edited*[0]
    
    """ Create and write all story files """
    
    for story_file in args.from_text:

        if not os.access(story_file, os.W_OK):
            logger.info("Story file is not writable: skipped '{}'.".format(story_file))
            continue
            
        logger.info("Processing '{}'.".format(story_file))

        story_as_dict, tasks_as_dict = read_story_as_dict(story_file)
        if story_as_dict is None or tasks_as_dict is None:
            logger.error("Story file is illegal '{}'.".format(story_file))
            continue

        """ Update the story estimate dependend on identified tasks """

        if story_as_dict['status'] in ["ready", "accepted", "committed"]: 
            story_as_dict, tasks_as_dict = reset_stories(story_as_dict, tasks_as_dict)
        elif story_as_dict['status'] in ["ANALYSING", "SPRINTING"]:
            story_as_dict, tasks_as_dict = consolidate_stories(story_as_dict, tasks_as_dict)
        
        if args.dry:
            logger.error("Would consolidate '{}'.".format(story_file))
            continue

        if write_story_from_dict(story_file, story_as_dict, tasks_as_dict) is None:
            logger.error("Unable to consolidate '{}'.".format(story_file))
        else:
            logger.info("Consolidated '{}'.".format(story_file))

    return 0

        
if __name__ == "__main__":
    sys.exit(main())

