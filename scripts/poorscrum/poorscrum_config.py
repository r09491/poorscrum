# -*- coding: utf-8 -*-

import os


""" Maps the story items to powerpoint placeholder index"""
PICKUP_FILE = os.path.join(os.environ["HOME"], ".poorscrum", "poorscrum_pickup.ini")

""" Maps the story items to powerpoint placeholder index"""
EMPTY_PPTX = os.path.join(os.environ["HOME"], ".poorscrum", "poorscrum_emptybacklog.pptx")

""" Contains data describing the sprint """
SPRINT_FILE = os.path.join(os.environ["HOME"], ".poorscrum", "poorscrum_sprint.ini")

""" The storage path for the temporary burndown chart """
BURNDOWN_SAVE_NAME = os.path.join(os.environ["HOME"], ".poorscrum", "poorscrum_burndown.png")
