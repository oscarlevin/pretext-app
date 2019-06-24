# Pretext-app

A python script to run everything related to pretext, from initializing a folder to setting up a config file (publisher.xml) to building latex/pdf and html from ptx source files.

## Implemented features

None.

## Planed features

Starting in a blank directory (or maybe inside a parent directory) run
`pretexer -init <project-name>`
to generate a directory structure and set of template ptx files.  

In a generated directory containing an outline.xml file, `pretexer -setup outline.xml` will create the ptx files for a book as specified in outline.xml.

`pretexer -setup` will install pretext (mathbook) if not already present and set paths in the config file.  Perhaps this is called by `pretexer -init` automatically.

`pretexer -build html` will, using publisher.xml or another config file, process the main ptx file (or a specified on with `-i <file>.ptx`?) into html.  Optional `-diagrams` regenerates diagrams using the mbx script (done automatically if images are found in ptx files but not in output directory?).

`pretexer -build latex` as above.

`pretexer -build pdf` builds latex and pdf in one step.

`pretexer -build epub` and etc.

Each of the above accept `-ww` to indicate whether the project contains ww elements?  Or just scan the ptx for <webwork> elements and do automatically.  Probably this, eventually.

`pretexer -validate` creates a jing error file

`pretexer -clean` to clean up ignored files or some list of temporary files.
