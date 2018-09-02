"""
    flask_unchained
    ---------------

    The better way to build large Flask apps

    :copyright: Copyright © 2018 Brian Cappello
    :license: MIT, see LICENSE for more details
"""

__version__ = '0.5.1'


from .app_factory import AppFactory
from .app_factory_hook import AppFactoryHook
from .app_config import AppConfig
from .bundle import AppBundle, Bundle
from .constants import DEV, PROD, STAGING, TEST
from .decorators import param_converter
from .di import BaseService, injectable
from .flask_unchained import FlaskUnchained
from .forms import FlaskForm
from .unchained import Unchained, unchained
from .utils import OptionalClass, OptionalMetaclass, get_boolean_env

from .bundles.babel import gettext, ngettext, lazy_gettext, lazy_ngettext
from .bundles.controller.constants import (ALL_METHODS, INDEX_METHODS, MEMBER_METHODS,
                                           CREATE, DELETE, GET, LIST, PATCH, PUT)
from .bundles.controller.controller import Controller
from .bundles.controller.decorators import route, no_route
from .bundles.controller.resource import Resource
from .bundles.controller.routes import (
    controller, func, get, include, patch, post, prefix, put, resource, rule)
from .bundles.controller.utils import redirect, url_for


# aliases
from flask import current_app, g, request, session, _app_ctx_stack, _request_ctx_stack
