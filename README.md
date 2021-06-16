# Barenames

Commandline tool for batch renaming files using regular expressions.

## Usage

```
Usage: barenames [OPTIONS] PATTERN REPLACEMENT

  Batch file rename tool with regex substitution.

  Example:

      barenames "myfile-(\d+)" "yourfile-\g<1>"

Options:
  --dir PATH                Directory to perform actions in (default: current
                            working directory)
  --preview / --no-preview  Show preview of renames with confirmation prompt.
  -r, --recursive           Search files to rename recursively
  --help                    Show this message and exit
```

Barenames uses regex to change file names, which is very powerful tool.
But power comes with responsibility, **it is adviced to use `--preview` option to
view what program is gonna do, before it does it, cause with regex you never truly know....**

### Change file extension:

This example changes extension of all `.md` files in
current working directory to `.rst`

```sh
barenames --preview "(?P<filename>.+)\.md" "\g<filename>.rst"
```

If your files are not in current working directory just pass
`--dir` option to override dir.

```sh
barenames --dir ~/my-notes/ --preview "(?P<filename>.+)\.md" "\g<filename>.rst"
```

If you wish to rename files in subdirectories too, use `--recursive` or `-r` for short.

```sh
barenames --recursive --preview "(?P<filename>.+)\.md" "\g<filename>.rst"
```

Use this option with caution though.
