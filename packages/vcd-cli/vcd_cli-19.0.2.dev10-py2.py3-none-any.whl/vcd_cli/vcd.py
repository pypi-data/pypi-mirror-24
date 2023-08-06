# vCloud CLI 0.1
#
# Copyright (c) 2014 VMware, Inc. All Rights Reserved.
#
# This product is licensed to you under the
# Apache License, Version 2.0 (the "License").
# You may not use this product except in compliance with the License.
#
# This product may include a number of subcomponents with
# separate copyright notices and license terms. Your use of the source
# code for the these subcomponents is subject to the terms and
# conditions of the subcomponent's license, as noted in the LICENSE file.
#

import click
import pkg_resources
from vcd_cli.plugin import load_user_plugins
from vcd_cli.utils import stdout


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group(context_settings=CONTEXT_SETTINGS,
             invoke_without_command=True)
@click.pass_context
@click.option('-d',
              '--debug',
              is_flag=True,
              default=False,
              help='Enable debug')
@click.option('-j',
              '--json',
              'json_output',
              is_flag=True,
              default=False,
              help='Results as JSON object')
@click.option('-n',
              '--no-wait',
              is_flag=True,
              default=False,
              help='Don''t wait for task')
def cli(ctx,
        debug,
        json_output,
        no_wait):
    """VMware vCloud Director Command Line Interface."""
    if ctx.invoked_subcommand is None:
        click.secho(ctx.get_help())
        return


@cli.command(short_help='show version')
@click.pass_context
def version(ctx):
    """Show vcd-cli version"""
    ver = pkg_resources.require("vcd-cli")[0].version
    ver_obj = {'product': 'vcd-cli',
               'description': 'VMware vCloud Director Command Line Interface',
               'version': ver}
    ver_str = '%s, %s, %s' % (ver_obj['product'],
                              ver_obj['description'],
                              ver_obj['version'])
    stdout(ver_obj, ctx, ver_str)


if __name__ == '__main__':
    cli()
else:
    import catalog  # NOQA
    import cluster  # NOQA
    import info  # NOQA
    import login  # NOQA
    import org  # NOQA
    import profile  # NOQA
    import search  # NOQA
    import system  # NOQA
    import task  # NOQA
    import vapp  # NOQA
    import vdc  # NOQA
    load_user_plugins()
