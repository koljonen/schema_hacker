# schema_hacker
Sublime plugin for opening the .sql file corresponding to a database object by pressing F2

![PRESS F2](https://github.com/koljonen/doc/blob/master/schema_hacker/PRESS%20F2.gif?raw=true)

**Prerequisites**  
This assumes you have a file structure `<project_folder>/<schema>/<type>/<objectname>.sql`, e.g. `<project_folder>/public/TABLES/foo.sql.`

**Installation**  
Clone the repo to ~/Library/Application Support/Sublime Text 3/Packages/.
You may or may not need to add `{"keys": ["f2"], "command": "schema_hacker_open_file"}` to your .sublime-keymap file.

**Usage**  
Just place the cursor on an object name and press F2.
