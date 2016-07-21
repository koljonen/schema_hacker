import sublime, sublime_plugin, logging, os

logger = logging.getLogger('schema_hacker')
class SchemaHackerOpenFile(sublime_plugin.TextCommand):
    def run(self, edit):
        logger.debug('Schema Hacker: open file')
        view = self.view
        file_name = view.substr(view.word(view.sel()[0])).lower() + '.sql'
        for path in find_file(view.window().folders(), 2, file_name):
            view.window().open_file(path)

def find_file(paths, depth, file_name):
    if depth == 0:
        return [os.path.join(path, f)
            for path in paths
            for f in os.listdir(path)
            if f.lower() == file_name.lower()]
    else:
        return find_file(
            [subdir for path in paths for subdir in subdirs(path)],
            depth - 1,
            file_name)

def subdirs(path):
    return [file_path
        for file_name in os.listdir(path)
        if not file_name.startswith('.')
        for file_path in (os.path.join(path, file_name),)
        if os.path.isdir(file_path)]
