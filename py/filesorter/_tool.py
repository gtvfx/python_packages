"""CLI for filesorter"""

import click


from . import _filesorter


@click.command(name='sortfiles')
@click.argument('root_dir', required=True)
@click.option('--sort_by', default="month", required=False, show_default=True)
def main(root_dir, sort_by):
    """CLI for filesorter
    
    Args:\n
        root_dir (str): The directory containing files you want to sort.\n
        sort_by (str, optional): The enumeration key to sort the files by\n 
            ('hour', 'day', 'month', 'year')
    
    """
    _sort_by = _filesorter.DATE_ENUM[sort_by.upper()]
    file_info_dict = _filesorter.collect_file_info(root_dir)
    _filesorter.organize_files_by_creation_date(file_info_dict, sort_by=_sort_by)


if __name__ == "__main__":
    main()
