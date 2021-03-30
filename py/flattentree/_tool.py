"""CLI for flattentree"""

import click


from . import _flattentree


@click.command(name='flattentree')
@click.argument('root_dir', required=True)
def main(root_dir):
    """CLI for flattentree
    
    Args:\n
        root_dir (str): Valid directory to flatten all subdirectories within.\n
    
    """
    _flattentree.flatten_tree(root_dir)


if __name__ == "__main__":
    main()
