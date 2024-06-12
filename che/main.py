import json
import os
import subprocess

import click
from mitmproxy.tools.main import mitmdump, mitmweb

from che import utils


@click.group()
def cli1():
    pass


@cli1.command("stop", help="Stop the gh-che proxy server.")
@click.pass_context
def stop(ctx):
    port = utils.get_config()["port"]
    subprocess.run(f"kill -9 $(lsof -t -i:{port})", shell=True)



@cli1.command("project", help="Set the project path.")
@click.argument('path', type=click.Path(exists=True, writable=True), required=False)
@click.pass_context
def project(ctx, path):
    config = utils.get_config()
    config["project_path"] = os.path.abspath(path) if path else os.getcwd()
    utils.save_config(config)
    print(f"Project path changed to {config['project_path']}")


@cli1.command("show-config", help="Show the configuration.")
@click.pass_context
def show_config(ctx):
    config = utils.get_config()
    print(json.dumps(config, indent=2))


@cli1.command("author", help="Set the author name")
@click.argument('name')
def change_author(name):
    config = utils.get_config()
    config["author"] = name
    utils.save_config(config)
    print(f"Author name changed to {name}")


@cli1.command("version", help="Get the version")
def version():
    properties = os.path.join(os.path.dirname(__file__), 'che.properties')
    with open(properties) as f:
        properties = f.readlines()
    prop_version = [line for line in properties if line.startswith("version")][0].split("=")[1].strip()
    print(prop_version)


@click.command("branch",help = "Change the branch name")
@click.argument('name')
def change_branch(name):
    config = utils.get_config()
    config["branch"] = name
    utils.save_config(config)
    print(f"Branch name changed to {name}")

@cli1.command(help="Start the gh-che proxy server.")
@click.option('--port', default=9696, help='Running port')
@click.option('--debug', default=False, help='Debug mode')
@click.option("--force-kill", default=True, help="Force kill the previous process.")
@click.argument('path', type=click.Path(exists=True, writable=True), required=False, default=None)
@click.pass_context
def start(ctx, port, debug, force_kill, path):
    config = utils.get_config()

    config["port"] = port
    config["debug"] = debug
    config["project_path"] = os.path.abspath(path) if path else os.getcwd()
    script_path = os.path.join(os.path.dirname(__file__), "binding.py")
    args = ["-p", f"{port}", "-s", script_path, "--set",
            "allow_hosts=githubcopilot.com", "--view-filter '~d githubcopilot.com'"]

    if force_kill:
        ctx.invoke(stop)

    if debug:
        mitmweb(args)
    else:
        mitmdump(args)


def main():
    cli1()


if __name__ == '__main__':
    main()
