import click

from .lib import iter_tree, rename_files


@click.command()
@click.option('--dir',
              type=click.Path(exists=True, dir_okay=True),
              default='.',
              help="Directory to perform actions in (default: current working directory)"
              )
@click.option('--preview/--no-preview', 
              help='Show preview of renames with confirmation prompt.',
              default=False,
              is_flag=True
              )
@click.option('--recursive',
              '-r',
              default=False,
              is_flag=True,
              help='Search files to rename recursively'
              )
@click.argument('pattern')
@click.argument('replacement')
def main(pattern: str,
         replacement: str,
         dir: str = '.',
         recursive: bool = False,
         preview: bool = False,
         ):
    """Batch file rename tool with regex substitution.

    Example:\r

        barenames "myfile-(\\d+)" "yourfile-\\g<1>"\r
    """
    found_matches = False
    for success, old_file, new_file, e in rename_files(pattern,
                                                       replacement,
                                                       iter_tree(dir,recursive=recursive),
                                                       preview=preview):
        found_matches = True
        if success:
            click.echo(
                click.style('|  OK  |', fg='green') if not preview else click.style('| VIEW |', fg='blue') 
                + f' "{old_file}" -> "{new_file}"')
        else:
            click.echo(
                click.style('| FAIL |', fg='red')
                + f' "{old_file}" -> "{new_file}"'
                + 'cause:'
                + click.style(str(e), fg='red')
            )
    if preview and found_matches:
        click.confirm('Is that correct?', abort=True)
        for success, old_file, new_file, e in rename_files(pattern,
                                                           replacement,
                                                           iter_tree(dir,recursive=recursive)):
            if success:
                click.echo(
                    click.style('|  OK  |', fg='green')
                    + f' "{old_file}" -> "{new_file}"')
            else:
                click.echo(
                    click.style('| FAIL |', fg='red')
                    + f' "{old_file}" -> "{new_file}"'
                    + 'cause:'
                    + click.style(str(e), fg='red')
                )
    
    
    click.echo(click.style('Finished!', fg='green'))


if __name__ == '__main__':
    main()
