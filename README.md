# poorscrum
Poor man's Scrum commandline tools

Once there was a Product Owner writing story cards to communicate with the development team and the customer. He decided to use Powerpoint as a story card editor. Immitating a hardcopy format he had found on the web he put each story in a well-designed layout on a slide. One after the other he added to the presentation and generated an impressive Product Backlog with a lot of  valuable information for other purposes. The only problem was how to extract.

The Product Owner was certified. He was taught that a Scrum Master is responsible for resolving impedients. The good willing man accepted. He also liked Python and after some googling he found the library python-pttx to write a few following commandline tools:

poorscrum_learn.py
Associates the fields defined in the config file "~/.poor_scrum/poor_scrum_pickup.ini" with the placeholder indices of the last layout of the slide master of a powerpoint presentation. The layout defines the content and appearance of the story. The file is required by the other tools.  

poorscrum_export.py         
Exports the slides from PPTX file into regular ASCII text files in config format

poorscrum_import.py
Imports the ASCII text files in config format into a PPTX file
  
poorscrum_burndown.py
Generates a burndown chart from the size fields in the layout if present
