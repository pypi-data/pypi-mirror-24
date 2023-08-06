# coding=utf-8
# Copyright 2017 Flowdas Inc. <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import importlib
import os

import yaml
from flowdas import meta

from .version import __version__

__all__ = [
    'AppError',
    'AppfileNotFoundError',
    'AppAlreadyExistsError',
    'AppNotReadyError',
    'AppfileError',
    'App',
    'define',
]


class AppError(Exception):
    pass


class AppfileNotFoundError(AppError):
    """appfile 을 발견할 수 없을 때 발생하는 예외.

    Since version 0.1.
    """
    pass


class AppAlreadyExistsError(AppError):
    """다른 root 를 갖는 두 개의 App 인스턴스를 만들려고 할 때 발생하는 예외.

    Since version 0.1.
    """
    pass


class AppNotReadyError(AppError):
    """Plugin 들이 import 될 때 App 인스턴스를 만들려고 할 때 발생하는 에러.

    Plugin 은 import 될 때 App 인스턴스를 만들 수 없다. 이 단계에서는 appfile 이 모두 로드되지 않은 상태이기 때문이다.
    Plugin 초기화에 :py:data:`App.config` 가 필요한 경우 :py:meth:`App.on_load` 데코레이터를 사용해야 한다.

    Since version 0.1.
    """
    pass


class AppfileError(AppError):
    """appfile 이 문법에 맞지 않을 때 발생하는 예외.

    Attributes:
        location (str):
            오류의 위치가 JSON Pointer 형식으로 제공된다.
        value (str):
            오류를 일으킨 값.

    Since version 0.1.
    """
    location = None
    value = None

    def __init__(self, context):
        if isinstance(context, meta.Context):
            if context.errors:
                self.location = context.errors[0].location
                self.value = context.errors[0].value
        elif isinstance(context, dict):
            self.location = context.get('location')
            self.value = context.get('value')


_defines = {}


def define(name, prop=None):
    """appfile 의 정의를 확장한다.

    name 은 최상단 파라미터의 이름.

    prop 는 파라미터의 형을 지정하는 :py:class:`flowdas.meta.Property` 인스턴스. 생략하면 :py:class:`flowdas.meta.String` ().

    이미 정의되어 있다면 오버라이드 한다.

    Since version 0.1.
    """
    if prop is None:
        prop = meta.String()
    _defines[name] = prop


class App(object):
    """appfile 로 정의되는 환경.

    :param root: 설정 파일이 들어있는 디렉토리 경로.

    Since version 0.1.
    """

    class Config(meta.Entity):
        """appfile schema"""
        plugins = meta.String[:](required=True)

    _on_loads = []
    _instance = None
    _loading = False

    __slots__ = ('_root', '_config')

    def __new__(cls, root=None):
        if App._loading:
            raise AppNotReadyError()
        if root is None:
            if App._instance is None:
                raise AppfileNotFoundError()
            elif isinstance(App._instance, cls):
                return App._instance
            else:
                raise AppAlreadyExistsError()
        else:
            root = App._norm_root(root)
            if App._instance is None:
                App._instance = super(App, cls).__new__(cls)
                return App._instance
            elif App._instance._root != root:
                raise AppAlreadyExistsError()
            elif isinstance(App._instance, cls):
                return App._instance
            else:
                raise AppAlreadyExistsError()

    def __init__(self, root=None):
        if root is None or hasattr(self, '_root'):
            return
        self._root = App._norm_root(root)
        try:
            if not os.path.exists(os.path.join(self._root, self.appfile())):
                raise AppfileNotFoundError()
            with open(os.path.join(self._root, self.appfile()), 'rb') as f:
                data = yaml.safe_load(f) or {}
            #
            # two-phase configuration loading
            #

            # first phase
            # 기본 설정만 로딩한 후 플러그인들을 임포트한다.
            App._loading = True
            try:
                for modname in self.builtins():
                    importlib.import_module(modname)
            finally:
                App._loading = False
            context = meta.Context()
            try:
                self._config = self.Config().load(data, context)
                self._config.validate()
            except ValueError:
                raise AppfileError(context)
            App._loading = True
            try:
                for modname in (self._config.plugins or []):
                    importlib.import_module(modname)
            finally:
                App._loading = False

            # second phase
            # 플러그인들의 설정을 반영해서 최종 로딩한다.
            CustomConfig = self.Config.define_subclass('Config', _defines)
            context = meta.Context()
            try:
                self._config = CustomConfig().load(data, context)
                self._config.validate()
            except ValueError:
                raise AppfileError(context)
            for hook in App._on_loads:
                hook(self)
        except:
            App._instance = None
            raise

    @staticmethod
    def _norm_root(root):
        root = os.path.abspath(os.path.expanduser(root))
        return root

    @property
    def root(self):
        """appfile 이 들어있는 디렉토리 경로.

        Since version 0.1.
        """
        return self._root

    @property
    def config(self):
        """appfile 에 기록한 설정이 저장되는 객체.

        Since version 0.1.
        """
        return self._config

    @classmethod
    def appfile(cls):
        """appfile 의 이름.

        Since version 0.1.
        """
        return 'app.yaml'

    @classmethod
    def builtins(cls):
        """내장 패키지들의 목록.

        Since version 0.1.
        """
        return []

    @classmethod
    def version(cls):
        """버전 문자열.

        Since version 0.1.
        """
        return __version__

    @classmethod
    def on_load(cls, func):
        """Plugin 이 import 될 때 :py:data:`App.config` 가 필요한 경우 사용되는 데코레이터.

        appfile 이 모두 로드되면, func(App()) 이 호출된다.

        Since version 0.1.
        """
        cls._on_loads.append(func)
        return func
