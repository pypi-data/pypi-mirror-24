"""PytSite Plugin Manager Settings Form.
"""
from pytsite import settings as _settings, widget as _widget, lang as _lang, html as _html, assetman as _assetman, \
    router as _router
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_DEV_MODE = _router.server_name() == 'local.plugins.pytsite.xyz'


class Form(_settings.Form):
    def _on_setup_form(self, **kwargs):
        """Hook.
        """
        super()._on_setup_form(**kwargs)

        _assetman.preload('pytsite.plugman@css/settings-form.css')
        _assetman.preload('pytsite.plugman@js/settings-form.js')

    def _on_setup_widgets(self):
        """Hook.
        """
        if _DEV_MODE:
            self.add_widget(_widget.static.Text(
                uid='dev_mode_notify',
                title=_lang.t('pytsite.plugman@cannot_manage_plugins_in_dev_mode'),
            ))

            self.remove_widget('action-submit')

            return

        lng = _lang.get_current()
        table = _widget.static.Table(uid='plugins', weight=10)

        # Table header
        table.add_row((
            _lang.t('pytsite.plugman@description'),
            _lang.t('pytsite.plugman@version'),
            {'content': _lang.t('pytsite.plugman@actions'), 'style': 'width: 1%;'},
        ), part='thead')

        for name, info in sorted(_api.get_plugin_info().items()):
            description = str(_html.Span(info['description'].get(lng)))

            actions = ''
            if not _api.is_installed(name):
                btn = _html.A(css='btn btn-xs btn-default action-btn', child_sep='&nbsp;',
                              href='#', data_name=name, data_ep='plugman/install')
                btn.append(_html.I(css='fa fa-download'))
                btn.append(_html.Span(_lang.t('pytsite.plugman@install'), css='text'))
                actions += str(btn)
            else:
                # Upgrade button
                if info['upgradable']:
                    btn = _html.A(css='btn btn-xs btn-default action-btn', child_sep='&nbsp;',
                                  href='#', data_name=name, data_ep='plugman/upgrade')
                    btn.append(_html.I(css='fa fa-arrow-up'))
                    btn.append(_html.Span(_lang.t('pytsite.plugman@upgrade'), css='text'))
                    actions += str(btn)

                # Uninstall button
                if not info['required']:
                    btn = _html.A(css='btn btn-xs btn-default action-btn', child_sep='&nbsp;',
                                  href='#', data_name=name, data_ep='plugman/uninstall')
                    btn.append(_html.I(css='fa fa-trash'))
                    btn.append(_html.Span(_lang.t('pytsite.plugman@uninstall'), css='text'))
                    actions += str(btn)

            if info['installed_version']:
                version = info['installed_version']
                if info['upgradable']:
                    version += ' ({})'.format(info['latest_version'])
            else:
                version = info['latest_version']

            table.add_row((
                description,
                {'content': version, 'css': 'cell-version'},
                {'content': actions, 'css': 'cell-actions'},
            ))

        self.add_widget(table)

        super()._on_setup_widgets()
