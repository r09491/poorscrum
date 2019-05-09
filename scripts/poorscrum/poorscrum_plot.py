# -*- coding: utf-8 -*-

from poorscrum import BURNDOWN_SAVE_NAME

from matplotlib import rcParams
import matplotlib.pyplot as plt

def burndown_as_image(work_edited, work_todo, save_name = BURNDOWN_SAVE_NAME):
    sprint_days = len(work_todo)

    rcParams['figure.figsize'] = (8, 6)

    plt.close("all")

    """ Draw the optimal line """
    plt.plot((0, sprint_days-1), (max(work_todo), 0), color="blue", label="optimal")

    """ Draw the committed story points after sprint planning """
    plt.bar(0, work_todo[0], color="green", label="start", width=0.5)

    """ Draw the actual work done """
    if (work_edited > 1) and (work_edited <= len(work_todo)):
        plt.bar(range(1,work_edited), \
                work_todo[1:work_edited], \
                color="red", label="actual", width=0.5)

    """ Draw the work still to be done """
    if (work_edited >= 1) and (work_edited < len(work_todo)):
        plt.bar(range(work_edited,len(work_todo)), \
                work_todo[work_edited:len(work_todo)], \
                color="grey", label="estimate", width=0.5)

    plt.ylim(0, work_todo[0])
    plt.yticks(range(0, work_todo[0]+1, max(1, int(work_todo[0] / 5))))

    plt.xlim(-1, sprint_days)
    plt.xticks(range(0, sprint_days+1, max(5, int(sprint_days / 5))))

    plt.grid()
    plt.legend()

    plt.xlabel('SPRINT DAYS [days]')
    plt.ylabel('TO BE DONE [story points]')

    plt.title("Sprint Burndown", fontsize=20)
    plt.savefig(save_name)

    return save_name

