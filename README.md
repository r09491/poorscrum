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
Associates the fields defined in the pickup file with the placeholder indices
of the last(!) layout of the slide master of a powerpoint presentation. The
layout shall define the content of the story. The file is required by the
other tools.

*poorscrum_export.py         
Exports the slides from PPTX file into regular ASCII text files in config
format

*poorscrum_import.py
Imports the ASCII text files in config format into a PPTX file
  
*poorscrum_burndown.py
Generates a burndown chart from the size fields in the layout if present



Installation

(1) Install virtualenv 
virtualenv -p python2 vpoorscrum

(2) Activate the virtualenv

(3) pip install requirements.txt


(4) Clone the initialisation directory
Execute cp -r home/.poorscrum ~/

(5) Update ~/.poorscrum/poorscrum_pickup.ini 
Execute  ./scripts/poorscrum_learn.py ~/.poorscrum/poorscrum_pickupbacklog.pptx 1

(6) Update the empty presentation ~/.poorscrum/poorscrum_emptybacklog.pptx 
Open ~/.poorscrum/poorscrum_pickupbacklog.pptx with Powerpoint
Remove the slide so that only the slide master is left
Save as ~/.poorscrum/poorscrum_emptybacklog.pptx

(7) Test export
 ./poorscrum_export.py ../starters/starter.pptx /tmp/starter

(8) Test import
./poorscrum_import.py --empty /tmp/starter.pptx /tmp/starter/*.story

(9) Test burndown
./poorscrum_import.py --empty /tmp/starter.pptx /tmp/starter/*.story

This README is work in progress!
