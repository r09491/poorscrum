#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "sepp.heid@t-online.de"
__doc__ = """ """

import argparse
import os
import sys

from pptx import Presentation
from pptx.exc import PackageNotFoundError
from pptx.util import Inches


import poorscrum
from poorscrum import __version__
from poorscrum.poorscrum_config import SPRINT_FILE
from poorscrum.poorscrum_sprint import *
from poorscrum.poorscrum_story import *
from poorscrum.poorscrum_plot import *


import configparser


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(sys.argv[0]))


def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        prog = os.path.basename(sys.argv[0]),
        description = "Add burnout chart to the PPTX file",
        epilog = "Ensure the '.pptx/pptx_pickup.ini' file exists in the the home directory")
    
    parser.add_argument("--version", action = "version", version=__version__)

    parser.add_argument('-s', '--sprint_file', default=SPRINT_FILE,
                        help='SCRUM sprint setup file')

    parser.add_argument("-d", "--dry", required=False,
                        action="store_true", 
                        help="Do not create image, do not add to PPTX")

    parser.add_argument("the_pptx", nargs="?", 
                        help="The name of the PPTX file to create the burnout chart for")


    return parser.parse_args()


def extract_work(from_slide, with_pickup):
    """ Returns the the work to be done from the slide size items
    """

    text = ""
    for item, index in with_pickup.items():
        if (item != "size 1") and \
               (item != "size 2") and \
               (item != "size 3") and \
               (item != "size 4"):
            continue
            
        try:
            shape = from_slide.placeholders[int(index)]
        except KeyError:
            return list() # Does not contain story, no error
        
        if not shape.has_text_frame:
            continue

        paras = shape.text_frame.paragraphs
        if len(paras) > 1:
            return None # More than one paragraph, error
            
        for p in paras:
            for r in p.runs:
                for c in r.text.strip():
                    if not (c.isdigit() or c.isspace()):
                        return None #  Error
                    text += c
                text += ' '
    return [int(c) for c in text.split()]


def add_burndown_to_pptx(the_pptx, image_path):
    blank_slide_layout = the_pptx.slide_layouts[6]
    slide = the_pptx.slides.add_slide(blank_slide_layout)
    left = top = Inches(1)
    image = slide.shapes.add_picture(image_path, left, top)


def main():
    args = parse_arguments()

    if args.the_pptx is None:
        logger.error("Must provide PPTX backlog file name for work to be done!")
        return 1

    if args.sprint_file is None:
        logger.error("Must provide file with sprint setup!")
        return 2

    fields_map = read_fields()
    if fields_map is None:
        logger.error("Must provide correct story item mappings. Run 'pptx_learn.py'!")
        return 3

    days, periods, points = read_sprint_properties(args.sprint_file)
    if days is None:
        logger.error("Must provide scrum guide legal number of days for sprint!")
        return 4

    if periods is None:
        logger.error("Must provide scrum guide legal number of periods for sprint!")
        return 5

    if points is None:
        logger.error("Must provide scrum guide legal capacity of development team!")
        return 6

    logger.info("The sprint length is '{:d}' days.".format(days))
    logger.info("The sprint has '{:d}' periods with '{:d}' working days.".format(periods, int(days/periods)))
    logger.info("The team has a capacity '{:d}' story points.".format(points))

    try:
        prs = Presentation(args.the_pptx)
    except NameError:
        logger.error("Presentation has illegal name.")
        return 6
    except PackageNotFoundError:
        logger.error("Presentation is not found.")
        return 7
    
    logger.info("The Backlog '{}' has '{:d}' slides."
                .format(os.path.basename(args.the_pptx), len(prs.slides)))

    """
    The first day (day 0) in the sprint is the sprint planing day. All other
    days may be used fro working.

    The last value entered for a slide is used for the values not provided
    until the end of the sprint. These are called the 'unedited'
    """
    total_work_edited = days
    total_work_todo = (days)*[0]
    for num, slide in enumerate(prs.slides):
        """ Calc work left for a slide in the sprint from sizes """
        slide_work_todo = extract_work(slide, fields_map)
        if slide_work_todo is None:
            logger.error("Slide '{:d}': Wrong syntax in size fields!".format(num+1))
            return 8

        slide_work_edited =len(slide_work_todo)
        if slide_work_edited == 0:
            logger.info("Slide '{:d}': Skipped since no size!".format(num+1))
            continue

        """
        A length of '1' means there is only an estimate: No editing has taken place. Ignore!
        """
        total_work_edited = 0 if slide_work_edited == 1 \
                            else min(total_work_edited, slide_work_edited) 
            

        """ Add entered values """
        edited_range = range(slide_work_edited)
        for index in edited_range:
            total_work_todo[index] += slide_work_todo[index]
        
        """ Add the last entered value """
        unedited_range = range(slide_work_edited, len(total_work_todo))
        for index in unedited_range:
            total_work_todo[index] += slide_work_todo[-1]
        
        logger.info("Slide '{:d}': Included in work to be done!".format(num+1))
        
    logger.info("Work left is consistently entered including sprint day {:d}."
                .format(total_work_edited))

    """ Output work to be done in period format """
    nperiods = periods+1
    for period in range(int(days / nperiods)):
        period_estimate = total_work_todo[(nperiods)*period:(nperiods)*(period+1)]
        logger.info("Work left estimate for period {:d}: {}".
                    format(period, str(period_estimate)))

    if points > total_work_todo[0]:
        logger.info("Devs offer more points than required ('{:d}' > '{:d}'). Sprint can work!"
                    .format(points, total_work_todo[0]))
        logger.info("'{:d}' points are available for analysis and spikes."
                    .format(points - total_work_todo[0]))
    else:
        logger.warn("Devs offers less points than required ('{:d}' < '{:d}'). Sprint cannot work!"
                    .format(points, total_work_todo[0]))
        logger.warn("Stories are to be reduced by '{:d}' points."
                    .format(total_work_todo[0] - points))
    
    if args.dry:
        logger.info("Dry run finished: ok.")
        return 0

    save_name = burndown_as_image(total_work_edited, total_work_todo)
    logger.info("Saved the burddown chart to '{}'".format(save_name))

    add_burndown_to_pptx(prs, save_name)
    logger.info("Added the burddown chart to the presentation '{}'".format(args.the_pptx))

    try:
        prs.save(args.the_pptx)
    except:
        logger.error("Cannot save the presentation. If it is open consider to close it!")
        return 11
    
    logger.info("Saved the presentation to '{}'".format(args.the_pptx))
    
    return 0

        
if __name__ == "__main__":
    sys.exit(main())

