import sublime, sublime_plugin, logging, os, subprocess

logger = logging.getLogger('schema_hacker')
settings = sublime.load_settings('schema_hacker.sublime_settings')

class SchemaHackerGenerateInsert(sublime_plugin.TextCommand):
    def run(self, edit):
        """Generate insert function for object under cursor."""
        logger.debug('Schema Hacker: open file')
        for sel in self.view.sel():
            schema, tbl = get_names(self.view, sel)
            schema = schema or 'public'
            folders = self.view.window().folders()
            script_path = ['misc', 'create_insert_function.pl']
            script = find_file(folders, script_path)[0]
            env = os.environ.copy()
            for key, val in (settings.get('env_var') or {}).items():
                env[key] = val
            fnc = subprocess.check_output(
                ['/usr/bin/perl', script, schema, tbl], env=env
            ).decode('utf8')
            file_name = fnc[
                fnc.index('CREATE OR REPLACE FUNCTION ') + 27 : fnc.index('(')
            ].lower() + '.sql'
            main_dir = os.path.dirname(os.path.dirname(script))
            fnc_path = os.path.join(main_dir, schema, 'FUNCTIONS', file_name)
            # Else: Create the file and open it
            if os.path.isfile(fnc_path):
                # Open existing file and put generated func in output panel
                view = self.view.window().open_file(fnc_path)
                panel = self.view.window().create_output_panel('schema_hacker')
                panel.run_command('append', {'characters': fnc, 'pos': 0})
                self.view.window().run_command(
                    'show_panel', {'panel': 'output.schema_hacker'})
            else: # Create function file and then open it
                with open(fnc_path, mode='w') as file:
                    file.write(fnc)
                view = self.view.window().open_file(fnc_path)


class SchemaHackerOpenFile(sublime_plugin.TextCommand):
    def run(self, edit):
        """Open the files matching the object names under the cursors."""
        logger.debug('Schema Hacker: open file')
        for sel in self.view.sel():
            _open_files(self.view, sel)

def get_names(view, sel):
    """ Return schema, name for object under cursor"""
    word = view.word(sel)
    schema = None
    if view.substr(word.begin() - 1) == '.':
        schema = view.substr(view.word(word.begin() - 2)).lower()
    return schema, view.substr(word).lower()

def _open_files(view, sel):
    """"Open .sql file matching object name under cursor"""
    schema, word = get_names(view, sel)
    file_name =  word + '.sql'
    path = [schema, None, file_name]
    files = find_file(view.window().folders(), path)
    if len(files) > 5:
        print('something is wrong; too many files; aborting')
        return
    for f in files:
        view.window().open_file(f)


def find_file(folders, path):
    """Return files matching `path`, starting in any folder in `folders`."""
    for name in path[:-1]:
        folders = [sub for folder in folders for sub in subdirs(folder, name)]
    return [
        os.path.join(folder, f)
        for folder in folders
        for f in os.listdir(folder)
        if f.lower() == path[-1]
    ]


def subdirs(path, name):
    """Return subdirs of `path.
    Filter case-insensitively against `name` if `name` is not None.
    """
    f = lambda x: name is None or x.lower() == name.lower()
    return [file_path
        for file_name in os.listdir(path)
        if f(file_name) and not file_name.startswith('.')
        for file_path in (os.path.join(path, file_name),)
        if os.path.isdir(file_path)]
