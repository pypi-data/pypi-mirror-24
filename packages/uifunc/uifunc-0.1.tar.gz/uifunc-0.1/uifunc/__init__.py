# provide decorators for functions that reads a folder/file name/list as the only argument
import sys
from typing import Callable, Any, Optional

try:
    from .wxopen import *
except ImportError:
    from .tkopen import *


class FolderSelector(object):
    def __init__(self, func: Callable[[str], Any]):
        self.func = func

    def __call__(self)-> Callable[[], Any]:
        if len(sys.argv) == 2:
            folder = sys.argv[1]
        else:
            folder = folder_to_open()
        return self.func(folder)


class FoldersSelector(object):
    def __init__(self, func: Callable[[List[str]], Any]):
        print(type(func), func)
        self.func = func

    def __call__(self) -> Callable[[], Any]:
        if len(sys.argv) > 1:
            folders = sys.argv[1:]
        else:
            folders = folders_to_open()
        return self.func(folders)


class FilesSelector(object):
    def __init__(self, files: Optional[List[str]]=None):
        self.files = files

    def __call__(self, func: Callable[[List[str]], Any]) -> Callable[[], Any]:
        files = self.files
        if len(sys.argv) > 1:
            files = sys.argv[1:]
        elif files and files[0].startswith('.'):
            files = files_to_open(files)
        elif files is None:
            raise ValueError("supply a list of files or file filters in argument or command line arguments")
        return func(files)


class FileSelector(object):
    def __init__(self, file: Optional[List[str]]=None):
        self.file = file

    def __call__(self, func: Callable[[str], Any]) -> Callable[[], Any]:
        file = self.file
        if len(sys.argv) == 2:
            file = sys.argv[1]
        elif file and file[0].startswith('.'):
            file = file_to_open(file)
        elif file is None:
            raise ValueError("supply a list of files or file filters in argument or command line arguments")
        return func(file)
