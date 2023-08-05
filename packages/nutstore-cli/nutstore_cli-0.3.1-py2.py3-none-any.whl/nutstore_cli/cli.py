# coding: utf-8
from __future__ import absolute_import

import click
import textwrap
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory

from nutstore_cli.client.client import NutStoreClient
from nutstore_cli.context import Context
from nutstore_cli.completer import completer
from nutstore_cli.execution import execute
from nutstore_cli.utils import info, error, to_file


def cli(username, key, working_dir):
    """
    NutStore Command Line Interface (0.3.1)

    NutStore WebDAV Settings: https://www.jianguoyun.com/d/account#safe

    Project Page: https://github.com/Kxrr/nutstore-cli
    """
    client = NutStoreClient(username=username, password=key, working_dir=working_dir, check_conn=False)
    try:
        client.check_conn()
    except Exception as e:
        import traceback
        error('Login failed, detail: {0}\n'
              'Usage: nutstore-cli --help'.format(to_file(traceback.format_exc())))
        import sys
        sys.exit(-1)
    info('Hello, {}'.format(username))
    info('Type "help" to see supported commands.')
    context = Context(client=client)
    history = InMemoryHistory()
    while True:
        try:
            text = prompt(
                message=u'[{path}] > '.format(path=context.path),
                completer=completer,
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
            )
        except EOFError:
            break
        else:
            execute(text, context)
            if context.should_exit:
                break
    info('Goodbye.')


@click.command(help=textwrap.dedent(cli.__doc__))
@click.option('--username', prompt='Username', help='Example: i@example.com')
@click.option('--key', prompt='App Key', help='Example: a2mqieixzkm5t5h4', hide_input=True)
@click.option('--working_dir', prompt='Working Dir', help='Example: /photos')
def launch_cli(*args, **kwargs):
    return cli(*args, **kwargs)


if __name__ == '__main__':
    launch_cli()
