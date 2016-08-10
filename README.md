# schema_hacker
Sublime plugin for simplifying schema hacking.



![PRESS F2](https://github.com/koljonen/doc/blob/master/schema_hacker/PRESS%20F2.gif?raw=true)



![Generate insert](https://github.com/koljonen/doc/blob/master/schema_hacker/generate%20insert.gif?raw=true)


**Prerequisites**  
The F2 function assumes you have a file structure `<project_folder>/<schema>/<type>/<objectname>.sql`, e.g. `<project_folder>/public/TABLES/foo.sql.`

**Installation**  
Clone the repo to ~/Library/Application Support/Sublime Text 3/Packages/.
You may or may not need to add `{"keys": ["f2"], "command": "schema_hacker_open_file"}` to your .sublime-keymap file.  
To get the insert-function function to work I needed to create a file called `~/Library/Application Support/Sublime Text 3/Packages/User/schema_hacker.sublime_settings` containing the following:
```
{
    "env_var": {
    	// You may or may not need to set PGHOST here, and maybe some other variables?
    	"PGHOST": "ubuntu"
    } 
}
```

**Usage**  
Just place the cursor on an object name and press F2.  
Or place the cursor on a table table and choose `Schema Hacker - Generate insert function` in the command palette.
