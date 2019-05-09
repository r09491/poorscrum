# -*- coding: utf-8 -*-

from poorscrum import BURNDOWN_SAVE_NAME

from matplotlib import rcParams
import matplotlib.pyplot as plt

def burndown_as_image(work_left, last_edited, save_name = BURNDOWN_SAVE_NAME):
    sprint_days = len(work_left)

    rcParams['figure.figsize'] = (8, 6)

    plt.close("all")

    """ Draw the optimal line """
    plt.plot((0, sprint_days-1), (max(work_left), 0), color="blue", label="optimal")

    """ Draw the committed story points after sprint planning """
    plt.bar(0, work_left[0], color="green", label="start", width=0.5)

    """ Draw the actual work done """
    if (last_edited > 1) and (last_edited <= len(work_left)):
        plt.bar(range(1,last_edited), \
                work_left[1:last_edited], \
                color="red", label="actual", width=0.5)

    """ Draw the work still to be done """
    if (last_edited >= 1) and (last_edited < len(work_left)):
        plt.bar(range(last_edited,len(work_left)), \
                work_left[last_edited:len(work_left)], \
                color="grey", label="estimate", width=0.5)

    plt.ylim(0, work_left[0])
    plt.yticks(range(0, work_left[0]+1, max(1, int(work_left[0] / 5))))

    plt.xlim(-1, sprint_days)
    plt.xticks(range(0, sprint_days+1, max(5, int(sprint_days / 5))))

    plt.grid()
    plt.legend()

    plt.xlabel('SPRINT DAYS [days]')
    plt.ylabel('TO BE DONE [story points]')

    plt.title("Sprint Burndown", fontsize=20)
    plt.savefig(save_name)

    return save_name

