# Poor Man's Scrum Commandline Tools

Once upon a time there was a Scrum Product Owner who wanted to use
story cards to communicate even better with his team and his
customer. He decided to use Powerpoint as card editor for impressive
presentations (with lady decorators) and easy printout. Immitating a
template found on the web he put each story in a well-designed layout
on a slide. He added one after the other and generated an impressive
Product Backlog with a lot of valuable information also for other
purposes. The only problem was to access and extract it.

The Product Owner was **certified**. He was taught that a Scrum Master is
responsible for resolving any impedients. The good willing man accepted since
he liked scripting. He also liked Python and after some googling he found the
library [python-pptx](github.com/scanny/python-pptx) to write a few
commandline tools:

#### poorscrum_learn.py

_Associates the fields defined in the pickup file with the placeholder
indices of the last(!) layout of the slide master of a powerpoint
presentation. The layout shall define the content of the story. The
pickup file ('poorscrum_pickup.ini' in the '.poorscrum' home
directory) is required by the other tools._

#### poorscrum_export.py

_Exports the slides from PPTX file into regular ASCII text files in
config format_

#### poorscrum_import.py

_Imports the ASCII text files in config format into a PPTX file_
  
#### poorscrum_burndown.py

_Generates a burndown chart from the size fields in the layout if
present. Requires the sprint defintion file 'poorscrum_sprint.ini' in
the '.poorscrum' home directory._

#### poorscrum_modify.py

_Modifies a single field in a text story after it has been updated in the PPTX
file._


## Installation

1. Clone poorscrum

   $ git clone https://github.com/r09491/poorscrum.git

2. Enter the cloned directory

   $ cd poorscrum

3. Install the python3 virtualenv with python3 in the clone

   $ virtualenv -p python3 .vpoorscrum

   You may want to add .vpoorscrum to .gitignore

4. Activate the python3 virtualenv

   $ . .vpoorscrum/bin/activate

5. Install the required python libraries

   $ pip install -r requirements.txt

## Usage

1. Clone the poorscrum initialisation directory into the home directory

   $ cp -r home/.poorscrum ~/

2. Update ~/.poorscrum/poorscrum_pickup.ini

   $ ./scripts/poorscrum_learn.py ~/.poorscrum/poorscrum_pickupbacklog.pptx 1

3. Test export

   $ ./scripts/poorscrum_export.py tests/hello_pptx.pptx tests/test

4. Test import

   $ ./scripts/poorscrum_import.py --empty tests/test.pptx tests/test/*.story

5. Test burndown

    $ ./poorscrum_burndown.py tests/test.pptx


## About [python-pptx](github.com/scanny/python-pptx)

The library [python-pptx](github.com/scanny/python-pptx) supports to modify an
existing slide, to append a new slide to an existing presentation. Especially
there is no obvious support to delete a slide, to move a slide, to insert a
new slide before or after another slide, to sort the slides as per their
content which prevents from changing the slide sequence "en situ". Export and
import is needed for this purpose.


## About Config Files

The tools use the python standard library
[configparser](https://docs.python.org/3/library/configparser.html) to store
the slides in ASCII text file in order to edit them conveniently. There are
some simple conventions to be followed in order to comment or to make a
paragraph. There is plenty of information on the web.


## Caveats

The Scrum Masters had access to a shared server

    from linux: to run his tools
    
    from windows: to work with Powerpoint


The tools do not work with pptx files from _libre office_!

The tools is tested under Linux only!

The Scrum Master is not a tester, the tools are not tested.


## TODO

* Add a tool for adding burnup charts
* Add additional layout for scrum
* Run under windows

