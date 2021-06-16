from pathlib import Path
from typing import Iterator, Union, Optional, Tuple
from pathlib import Path
import re


def iter_tree(path: Union[str, Path],
              files_only: bool=False,
              recursive: bool=False,
              follow_symlinks: bool = False
              ) -> Iterator[Path]:
    """Iterate directory tree
    
    if files_only is True, only files will be yielded.
    if recursive is True, will also return contents of subdirectories
    
    if files_only is False and recusive is True,
    subdirectories are yielded after their contents
    
    If follow_symlinks is True, iterator will resolve all symlinks
    
    :param path: A path to iterate
    :param fiels_only: whether to yield only files (default: False)
    :param recursive: whether to yield contents of subdirectories (default: False)
    :param follow_symlinks: if false all symlinks will be ignored (completely excluded from output)
    """
    visited_folders = set()

    if isinstance(path, str):
        path = Path(path)
    
    if path.is_file():
        yield path
    else:
        for i in path.iterdir():
            if i.is_symlink():
                if not follow_symlinks:
                    continue
                else:
                    i = i.readlink()
            if i.is_file():
                yield i
            else:
                if recursive:
                    ap = str(i.absolute())
                    if ap in visited_folders:
                        continue
                    visited_folders.add(ap)
                    yield from iter_tree(i, files_only, recursive)
                if not files_only:
                    yield i



def rename_files(pattern: str,
                 to: str,
                 paths: Iterator[Path],
                 preview: bool = False
                 ) -> Iterator[Tuple[bool, Path, Path, Optional[Exception]]]:
    """User given regex pattern to rename files in given iterator.
    
    :param pattern: regex pattern to match file names
    :param to: what to replace the pattern with
    :param paths: iterator over pathlib.Path objects
    :param preview: if true, don't actually rename files
    """
    regex = re.compile(pattern)
    for path in paths:
        filename = path.name
        if not regex.match(filename): continue
        if (new_name := re.sub(regex, to, filename)) != filename:
            new_path = path.with_name(new_name)
            try:
                if not preview:
                    path.rename(new_path)
                yield True, path, new_path, None
            except OSError as e:
                yield False, path, new_path, e

