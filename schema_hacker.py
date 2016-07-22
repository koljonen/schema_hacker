import sublime, sublime_plugin, logging, os

logger = logging.getLogger('schema_hacker')
class SchemaHackerOpenFile(sublime_plugin.TextCommand):
    def run(self, edit):
        """Open the file matching the object name under the cursor."""
        logger.debug('Schema Hacker: open file')
        view = self.view
        word = view.word(view.sel()[0])
        schema = None
        if view.substr(word.begin() - 1) == '.':
            schema = view.substr(view.word(word.begin() - 2)).lower()
        file_name = view.substr(word).lower() + '.sql'
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
