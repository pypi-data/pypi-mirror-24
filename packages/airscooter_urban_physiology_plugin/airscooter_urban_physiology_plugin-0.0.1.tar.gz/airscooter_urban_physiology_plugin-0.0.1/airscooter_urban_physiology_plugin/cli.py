import click
# noinspection PyUnresolvedReferences
from urban_physiology_toolkit import workflow


@click.command()
@click.option('--max-filesize', help='The maximum size (in MB) of resources in the glossary that will be read into the '
                                     'catalog.')
@click.option('--max-columns', help='The maximum size (in number of columns of data) of resources in the glossary that '
                                    'will be read into the catalog.')
def init_catalog(max_filesize, max_columns):
    workflow.init_catalog("glossary.json", ".", max_filesize=max_filesize, max_columns=max_columns)
    workflow.update_dag(root=".")


@click.command()
def finalize_catalog():
    workflow.finalize_catalog(".")
    workflow.update_dag(root=".")
