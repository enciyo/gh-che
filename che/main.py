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
    subprocess.Popen(f"kill -9 $(lsof -t -i:{port})", shell=True)


@cli1.command("configure-pac", help="Configure the pac file.")
@click.pass_context
def configure_pac(ctx):
    utils.create_pac_file()


@cli1.command("change-project", help="Set the project path.")
@click.argument('path', type=click.Path(exists=True, writable=True), required=False)
@click.pass_context
def project(ctx, path):
    config = utils.get_config()
    config["project_path"] = os.path.abspath(path) if path else os.getcwd()
    utils.save_config(config)


@cli1.command("show-config", help="Show the configuration.")
@click.pass_context
def show_config(ctx):
    config = utils.get_config()
    print(json.dumps(config, indent=2))


@cli1.command("show-pac", help="Show the pac file.")
@click.pass_context
def show_pac(ctx):
    pac_file = utils.get_pac_file()
    with open(pac_file) as f:
        print(f.read())


@cli1.command(help="Start the gh-che proxy server.")
@click.option('--port', default=9696, help='Running port')
@click.option('--debug', default=False, help='Debug mode')
@click.option("--auto-proxy", default=True, help="Auto proxy. (No need to set the proxy manually)")
@click.option("--force-kill", default=True, help="Force kill the previous process.")
@click.argument('path', type=click.Path(exists=True, writable=True), required=False, default=None)
@click.pass_context
def start(ctx, port, debug, auto_proxy, force_kill, path):
    config = utils.get_config()

    config["port"] = port
    config["debug"] = debug
    config["project_path"] = os.path.abspath(path) if path else os.getcwd()
    script_path = os.path.join(os.path.dirname(__file__), "binding.py")
    args = ["-p", f"{port}", "-s", script_path]
    if auto_proxy:
        ctx.invoke(configure_pac)

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
