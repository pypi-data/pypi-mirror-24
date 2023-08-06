# coding=utf-8
# Copyright 2017 Flowdas Inc. <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

import click
import yaml

from .app import App

__all__ = [
    'command',
    'main',
]

#
# command line interface
#

_AppType = App


class Cli(click.Group):
    def invoke(self, ctx):
        root = os.getcwd()
        while True:
            if os.path.exists(os.path.join(root, _AppType.appfile())):
                _AppType(root)
                break
            next_root = os.path.dirname(root)
            if root == next_root:
                click.echo("%s not found" % _AppType.appfile())
                ctx.exit(-1)
            else:
                root = next_root
        super(Cli, self).invoke(ctx)


@click.command(cls=Cli, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help(), color=ctx.color)
        ctx.exit()


def command(*args, **kwargs):
    """명령행 인터페이스에 명령을 추가하는 데코레이터.

    인자는 :py:func:`click.command` 의 정의를 따른다.

    Example:

        >>> import launch
        >>>
        >>> @launch.command(help='Print version')
        ... def version():
        ...     print(launch.App().version())

    Since version 0.1.
    """

    def deco(func):
        return cli.command(*args, **kwargs)(func)

    return deco


@command(help='Print version string.')
def version():
    click.echo(App().version())


@command(help='Verify configuration.')
@click.pass_context
def verify(ctx):
    app = App()
    with open(os.path.join(app.root, app.appfile()), 'rb') as f:
        filedata = yaml.safe_load(f) or {}
    confdata = app.config.dump()
    for key in confdata:
        filedata.pop(key, None)
    if filedata:
        click.echo(yaml.dump(filedata, default_flow_style=False), nl=False)
        ctx.exit(-1)


def main(app_type=App):
    """명령 실행의 진입 지점.

    명령행 명령 `launch` 를 다른 이름으로 변경하거나, :py:class:`App` 을 확장하고자 할 때 사용된다.

    app_type 으로 :py:class:`App` 를 계승하는 클래스를 전달한다.

    Since version 0.1.
    """
    global _AppType
    backup = _AppType
    _AppType = app_type
    try:
        cli()
    finally:
        _AppType = backup
