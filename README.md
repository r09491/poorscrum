# poorscrum
Poor man's Scrum commandline tools

Once there was a Product Owner who wanted to use story cards to communicate with the development team and the customer. For whatever reason he decided to use Powerpoint as a story card editor. He put each story in a well-designed layout (as he said) on slide immitating a hardcopy format he had found after some googling on the web. One slide after the other he added to the presentation and generated an impressive Backlog with a lot of information valuable also other purposes. The only problem was how to extract.

The Product Owner was certified. He had learned that there is a Scrum Master who is responsible for resolving impedients. After some discussion and a communication training they understood there is nothing more valuable in the world than the team and  the good willing Scrum Master accepted.

The later also liked Python and googled for a python library in the context of Powerpoint. He found python-pttx which he used to write the following commandline:

poorscrum_learn.py
Associates the information of the fields in "~/.poor_scrum/poor_scrum_pickup.ini" with the placeholder indices of the last layout of the slide master of a powerpoint presentation. This layout defines the content of the story. The file is required by the other tools.  

poorscrum_export.py         
Exports the slides from PPTX file into regular ASCII text files in config format
  
poorscrum_import.py
Imports the ASCII text files in config format into a PPTX file
  
poorscrum_burndown.py
Generates a burndown chart from the size fields in the layout if present
  
How to use

