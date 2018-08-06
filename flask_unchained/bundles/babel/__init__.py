"""
    Babel Bundle
    ------------

    Adds support for translations to Flask Unchained
"""

import pkg_resources
import re

from flask import Flask, Blueprint, current_app, g, request
from flask_babelex import Domain, gettext as _gettext, ngettext as _ngettext
from flask_unchained import Bundle
from speaklater import make_lazy_string
from typing import *
from werkzeug.local import LocalProxy

from .extensions import babel


TRANSLATION_KEY_RE = re.compile(r'^(?P<domain>[a-z_]+)\.[a-z_.]+$')
PLURAL_TRANSLATION_KEY_RE = re.compile(r'^(?P<domain>[a-z_]+)\.[a-z_.]+\.plural$')


class BabelBundle(Bundle):
    command_group_names = ('babel',)
    language_code_key = 'lang_code'

    def before_init_app(self, app: Flask):
        app.jinja_env.add_extension('jinja2.ext.i18n')
        babel.locale_selector_func = self.get_locale
        if app.config.get('ENABLE_URL_LANG_CODE_PREFIX'):
            app.url_value_preprocessor(self.lang_code_url_value_preprocessor)
            app.url_defaults(self.set_url_defaults)

    def after_init_app(self, app: Flask):
        if not app.config.get('LAZY_TRANSLATIONS'):
            app.jinja_env.install_gettext_callables(gettext, ngettext, newstyle=True)
        else:
            app.jinja_env.install_gettext_callables(lazy_gettext, lazy_ngettext,
                                                    newstyle=True)

    def get_url_rule(self, rule: Optional[str]):
        if not rule:
            return f'/<{self.language_code_key}>'
        return f'/<{self.language_code_key}>' + rule

    def register_blueprint(self, app: Flask, blueprint: Blueprint, **options):
        if app.config.get('ENABLE_URL_LANG_CODE_PREFIX'):
            url_prefix = (options.get('url_prefix', (blueprint.url_prefix or ''))
                                 .rstrip('/'))
            options = dict(**options,
                           url_prefix=self.get_url_rule(url_prefix),
                           register_with_babel=False)
            app.register_blueprint(blueprint, **options)

    def add_url_rule(self, app: Flask, rule: str, **kwargs):
        if app.config.get('ENABLE_URL_LANG_CODE_PREFIX'):
            app.add_url_rule(self.get_url_rule(rule), register_with_babel=False, **kwargs)

    def get_locale(self):
        languages = current_app.config['LANGUAGES']
        return g.get(self.language_code_key,
                     request.accept_languages.best_match(languages))

    def set_url_defaults(self, endpoint: str, values: Dict[str, Any]):
        if self.language_code_key in values or not g.get(self.language_code_key, None):
            return

        if current_app.url_map.is_endpoint_expecting(endpoint, self.language_code_key):
            values[self.language_code_key] = g.lang_code

    def lang_code_url_value_preprocessor(self, endpoint: str, values: Dict[str, Any]):
        if values is not None:
            g.lang_code = values.pop(self.language_code_key, None)


def gettext(*args, **kwargs):
    key = args[0]
    key_match = TRANSLATION_KEY_RE.match(key)
    translation = _gettext(*args, **kwargs)
    if not key_match or translation != key:
        return translation

    return _get_domain(key_match).gettext(*args, **kwargs)


def lazy_gettext(*args, **kwargs):
    return make_lazy_string(gettext, *args, **kwargs)


def ngettext(*args, **kwargs):
    is_plural = args[2] > 1
    if not is_plural:
        key = args[0]
        key_match = TRANSLATION_KEY_RE.match(key)
    else:
        key = args[1]
        key_match = PLURAL_TRANSLATION_KEY_RE.match(key)

    translation = _ngettext(*args, **kwargs)
    if not key_match or translation != key:
        return translation

    return _get_domain(key_match).ngettext(*args, **kwargs)


def lazy_ngettext(*args, **kwargs):
    return make_lazy_string(ngettext, *args, **kwargs)


def _get_domain(match):
    domain_name = match.groupdict()['domain']
    try:
        domain_resources = pkg_resources.resource_filename(domain_name, 'translations')
    except ImportError:
        return current_app.extensions['babel']._default_domain

    return Domain(domain_resources, domain=domain_name)


# FIXME this doesn't quite work (app context not always available)....
_ = LocalProxy(
    lambda: lazy_gettext if current_app.config.get('LAZY_TRANSLATIONS') else gettext)
