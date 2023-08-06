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
from pyvcloud.vcd.cluster import Cluster
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import cli


@cli.group(short_help='manage clusters')
@click.pass_context
def cluster(ctx):
    """Work with kubernetes clusters in vCloud Director.

\b
    Examples
        vcd cluster list
            Get list of kubernetes clusters in current virtual datacenter.
\b
        vcd cluster create k8s-cluster --nodes 2
            Create a kubernetes cluster in current virtual datacenter.
\b
        vcd cluster delete 692a7b81-bb75-44cf-9070-523a4b304733
            Deletes a kubernetes cluster by id.
    """  # NOQA
    if ctx.invoked_subcommand is not None:
        try:
            restore_session(ctx)
            if not ctx.obj['profiles'].get('vdc_in_use') or \
               not ctx.obj['profiles'].get('vdc_href'):
                raise Exception('select a virtual datacenter')
        except Exception as e:
            stderr(e, ctx)


@cluster.command(short_help='list clusters')
@click.pass_context
def list(ctx):
    try:
        client = ctx.obj['client']
        cluster = Cluster(client)
        result = []
        clusters = cluster.get_clusters()
        for c in clusters:
            result.append({'name': c['name'],
                           'id': c['cluster_id'],
                           'status': c['status'],
                           'leader_endpoint': c['leader_endpoint'],
                           'leaders': len(c['master_nodes']),
                           'nodes': len(c['nodes'])
                           })
        stdout(result, ctx, show_id=True)
    except Exception as e:
        stderr(e, ctx)


@cluster.command(short_help='create cluster')
@click.pass_context
@click.argument('name',
                metavar='<name>',
                required=True)
@click.option('-N',
              '--nodes',
              'node_count',
              required=False,
              default=2,
              metavar='<nodes>',
              help='Number of nodes to create')
@click.option('-n',
              '--network',
              'network_name',
              default=None,
              required=False,
              metavar='<network>',
              help='Network name')
@click.option('-w',
              '--wait',
              'wait',
              is_flag=True,
              default=False,
              required=False,
              help='Wait until finish')
def create(ctx, name, node_count, network_name, wait):
    try:
        client = ctx.obj['client']
        cluster = Cluster(client)
        result = cluster.create_cluster(
                    ctx.obj['profiles'].get('vdc_in_use'),
                    network_name,
                    name,
                    node_count)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@cluster.command(short_help='delete cluster')
@click.pass_context
@click.argument('cluster_id',
                metavar='<cluster-id>',
                required=True)
@click.option('-w',
              '--wait',
              'wait',
              is_flag=True,
              default=False,
              required=False,
              help='Wait until finish')
def delete(ctx, cluster_id, wait):
    try:
        client = ctx.obj['client']
        cluster = Cluster(client)
        result = cluster.delete_cluster(cluster_id)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
