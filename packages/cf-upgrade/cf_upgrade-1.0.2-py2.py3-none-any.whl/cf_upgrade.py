import re
import sys
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import WaiterError
import click
from tabulate import tabulate


class VariableType(click.ParamType):
    name = 'parameter'

    def convert(self, value, param, ctx):
        m = re.match(r'([^=]+)=([^=]+)$', value)
        if m is not None:
            return m.groups()
        return ('Version', value)


VARIABLE = VariableType()


@click.group()
@click.option('--profile', help='AWS profile')
@click.option('--region', help='AWS region')
@click.pass_context
def cli(ctx, profile, region):
    ctx.obj = {
        'session': boto3.session.Session(
            profile_name=profile,
            region_name=region),
    }


@cli.command()
@click.pass_context
def list(ctx):
    """List all known stacks.
    """
    cf = ctx.obj['session'].client('cloudformation')
    stacks = []
    paginator = cf.get_paginator('list_stacks')
    for page in paginator.paginate():
        stacks.extend(
            s for s in page['StackSummaries']
            if not s['StackStatus'].startswith('DELETE'))
    table = [
        (stack['StackName'], stack['StackStatus'])
        for stack in stacks
    ]
    print(tabulate(table, headers=['Stack', 'Status']))


@cli.command()
@click.option('--wait/--no-wait', default=True, help='Wait for update to finish')
@click.argument('stack')
@click.argument('setting', nargs=-1, required=True, type=VARIABLE)
@click.pass_context
def upgrade(ctx, stack, setting, wait):
    """Upgrade a stack to a new version.
    """
    new_settings = dict(setting)
    cf = ctx.obj['session'].client('cloudformation')
    summary = cf.get_template_summary(StackName=stack)
    parameters = [p['ParameterKey'] for p in summary['Parameters']]
    missing = set(new_settings) - set(parameters)
    if missing:
        click.echo('You specified unknown parameter(s): %s' % ' '.join(sorted(missing)), err=True)
        sys.exit(1)

    parameters = [
        {
            'ParameterKey': p,
            'UsePreviousValue': True
        }
        for p in parameters
        if p not in new_settings
    ]
    parameters.extend([
        {'ParameterKey': s[0], 'ParameterValue': s[1]}
        for s in new_settings.items()
    ])
    template = cf.get_template(StackName=stack)
    try:
        r = cf.update_stack(
            StackName=stack,
            Capabilities=summary['Capabilities'],
            TemplateBody=template['TemplateBody'],
            Parameters=parameters,
        )
    except ClientError as e:
        click.echo(str(e), err=True)
        sys.exit(2)

    if wait:
        click.echo('Stack updating, waiting to complete...', nl=False)
        waiter = cf.get_waiter('stack_update_complete')
        try:
            r = waiter.wait(
                StackName=r['StackId'],
                WaiterConfig={
                    'Delay': 10,
                    'MaxAttempts': 360,
                })
            click.echo(' done')
        except WaiterError as e:
            click.echo(str(e), err=True)
            sys.exit(2)
        except KeyboardInterrupt:
            click.echo()
            if click.confirm('Do you want to cancel the update?'):
                click.echo('Ok, cancelling')
                cf.cancel_update_stack(StackName=stack)
            else:
                click.echo('Ok, update will proceed in the background.')
    else:
        click.echo('Stack updating')


if __name__ == '__main__':
    cli()
