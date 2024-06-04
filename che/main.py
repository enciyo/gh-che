import os

import click
from mitmproxy.tools.main import mitmdump, mitmweb

from che import utils


@click.command()
@click.option('--port', default=9696, help='Running port')
@click.option('--debug', default=False, help='Debug mode')
@click.argument('project', type=click.Path(exists=True, writable=True), required=False)
def main(port, debug, project):
    project = os.path.abspath(project) if project else os.getcwd()
    utils.SharedValues.change_workspace(project)
    script = os.path.join(os.path.dirname(__file__), "binding.py")
    shell_args = ["-p", f"{port}", "-s", script]
    if debug:
        mitmweb(shell_args)
    else:
        mitmdump(shell_args)


if __name__ == '__main__':
    main()


