# poorscrum
Poor man's Scrum commandline tools

Once upon a time there was a Product Owner writing story cards to communicate with
his team and his customer. He decided to use Powerpoint as card editor. Immitating
a hardcopy found on the web he put each story in a well-designed layout on a
slide. One after the other he added to the presentation and generated an
impressive Product Backlog with a lot of valuable information also for other
purposes. The only problem was to use it if not for reading.

The Product Owner was certified. He was taught that a Scrum Master is
responsible for resolving any impedients. The good willing man accepted. He
also liked Python and after some googling he found the library python-pttx to
write a few following commandline tools:

*poorscrum_learn.py
-------------------
Associates the fields defined in the pickup file with the placeholder indices
of the last(!) layout of the slide master of a powerpoint presentation. The
layout shall define the content of the story. The file is required by the
other tools.

*poorscrum_export.py
--------------------
Exports the slides from PPTX file into regular ASCII text files in config
format

*poorscrum_import.py
--------------------
Imports the ASCII text files in config format into a PPTX file
  
*poorscrum_burndown.py
----------------------
Generates a burndown chart from the size fields in the layout if present



Installation
------------

(1) Clone poorscrum
$ git clone https://github.com/r09491/poorscrum.git

(2) Enter the cloned directory
$ cd poorscrum

(3) Install the python3 virtualenv with python3 in the clone
$ virtualenv -p python3 .vpoorscrum

  You may want to add .vpoorscrum to .gitignore

(4) Activate the python3 virtualenv
$ . .vpoorscrum/bin/activate

(5) Install the required python libraries
$ pip install -r requirements.txt

(6) Clone the poorscrum initialisation directory into the home directory
Execute cp -r home/.poorscrum ~/

(7) Update ~/.poorscrum/poorscrum_pickup.ini 
$ ./scripts/poorscrum_learn.py ~/.poorscrum/poorscrum_pickupbacklog.pptx 1


(8) Test export
$ ./scripts/poorscrum_export.py ../tests/test.pptx /tmp/test

(9) Test import
$ ./scripts/poorscrum_import.py --empty /tmp/test.pptx /tmp/test/*.story

(10) Test burndown
$ ./poorscrum_import.py --empty /tmp/test.pptx /tmp/test/*.story


Caveats
-------
The tools do not work with pptx files from libre office!
