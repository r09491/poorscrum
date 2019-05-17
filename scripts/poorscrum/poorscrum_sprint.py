# -*- coding: utf-8 -*-

import configparser

from poorscrum import SPRINT_FILE

MIN_DAYS, MAX_DAYS = 0, 20
MIN_PERIODS, MAX_PERIODS = 0, 4
MIN_POINTS, MAX_POINTS = 0, 340 # 
          
def read_sprint_properties(sprint_file = SPRINT_FILE):
    """ Read the scrum sprint file
    """
    sprint = configparser.ConfigParser()
    sprint.read(sprint_file)

    try:
        days = int(sprint.get("TIME", "days"))
    except configparser.NoSectionError:
        return None, None, None  # Illegal file content

    if days < MIN_DAYS or days > MAX_DAYS:
        return None, None # Illegal value

    try:
        periods = int(sprint.get("TIME", "periods"))
    except configparser.NoSectionError:
        return days, None, None  # Illegal file content

    if periods < MIN_PERIODS or periods > MAX_PERIODS:
        return days, None, None  # Illegal value

    try:
        points = 0
        for dev, point in sprint.items("TEAM"):
            if int(point) < MIN_POINTS or int(point) > MAX_POINTS:
                return days, periods, None 
            points += int(point)
    except:
        return days, periods, None # Illegal file content

    return days, periods, points
