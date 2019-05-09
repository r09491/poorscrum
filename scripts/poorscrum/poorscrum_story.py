# -*- coding: utf-8 -*-

import os

import configparser

from enum import Enum

from poorscrum import PICKUP_FILE

class Status(Enum):
    """ Defines the current status in the life cycle of a story.

    The PO identifies a topic with value for the product, starts with its
    analysis and creates a story in the Product Backlog. He may delegate to
    an expert. If he is ready (the story meets INVEST) it is a candidate for a
    sprint and the PO presents it to the team in the sprint planning. The
    complete team accepts it if every Dev unterstands it. The complete team
    estimates the effort and each Dev commits himself to its implementation in
    the sprint within the estimate. The team can reject the story if it does
    not understand it or if cannot estimate the work involved.

    It is the sole responibility of the Devs to organise the sprint and to
    allocate tasks on the individual members' skills. The team verifies the
    results against acceptance criteria before the sprint reviewe.

    The story is done if the PO accepts the results.
    
    Used to represent a KANBAN like structure:

             |none     |undone   |rejected |ANALYSING|planned  |SPRINTING|verified |done     |out      |
    =========+=========+=========+=========+=========+=========+=========+=========+=========+=========+
     <dev 1> |<story i>|         |         |         |         |         |         |         |         |
    ---------+<story k>|         |         +---------+         +---------+         +         +         |
     <dev 2> |         |         |         |         |         |<story 1>|         |         |         |
             |         |         |         |         |         |<story 2>|         |         |         |
    ---------+         |         |         +---------+         +---------+         +         +         |
     <dev 3> |         |         |         |<story 3>|         |         |         |         |         |
    ---------+         |         |         +---------+         +---------+         +         +         |
            ...                                                                             ...
            
    ---------+         |         |         +---------+         +---------+         +         +         |
     <dev n> |         |         |         |         |         |         |         |         |         |
    =========+=========+=========+=========+=========+=========+=========+=========+=========+=========+
     
    """
    none = 'none'
    undone = 'undone'
    rejected = 'rejected'
    analysing = 'ANALYSING'   # Story allocated to a team member with skills
    ready = 'ready'           # belongs to planned
    accepted = 'accepted'     # belongs to planned 
    committed = 'committed'   # belongs to planned
    sprinting = 'SPRINTING'   # Story allocated to a team member with skills
    verified = 'verified'
    done = 'done'
    out = 'out'

    def __str__(self):
        return self.value

    def __lt__(self, other):
        return self.pos < other.pos

    def __gt__(self, other):
        return self.pos > other.pos

    @property
    def pos(self):
        return list(self.__class__).index(self)


def read_fields(pickup_file = PICKUP_FILE):
    """ Read the mappings of the story fields to powerpoint placeholder indices
    """
    pickup = configparser.ConfigParser()
    pickup.read(pickup_file)

    try:
        return dict(pickup.items("STORY"))
    except configparser.NoSectionError:
        return None # Illegal file content


def write_fields(pickup, pickup_file = PICKUP_FILE):
    """ Write the index mappings of the story items
    """
    config = configparser.ConfigParser()
    config.add_section("STORY")
    for k, v  in pickup.items():
        config.set("STORY", k, v)
    with open(pickup_file, "w") as config_file:
        config.write(config_file)

    return pickup_file
    

          
