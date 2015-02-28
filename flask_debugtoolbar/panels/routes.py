from collections import OrderedDict
from flask_debugtoolbar.panels import DebugPanel
from flask import current_app

_ = lambda x: x


class RoutesDebugPanel(DebugPanel):
    """
    A panel to display Flask app routes.
    """
    name = 'Routes'
    has_content = True

    def nav_title(self):
        return _('Routes')

    def title(self):
        return _('Routes')

    def url(self):
        return ''

    def process_request(self, request):
        pass

    def content(self):
        context = self.context.copy()
        blueprints = {}
        for endpoint, _rules in current_app.url_map._rules_by_endpoint.iteritems():
            if any(item in endpoint for item in ['_debug_toolbar', 'debugtoolbar', 'static']):
                continue
            blueprint_name = endpoint.split('.')[0]
            if not blueprint_name in blueprints:
                blueprints[blueprint_name] = {}
            for rule in _rules:
                rule.methods = sorted(filter(lambda x: x not in ['HEAD', 'OPTIONS'], rule.methods))
            blueprints[blueprint_name][endpoint] = _rules
        # Reorder
        blueprints = OrderedDict(sorted(blueprints.iteritems()))
        for key in blueprints.keys():
            blueprints[key] = OrderedDict(sorted(blueprints[key].iteritems()))
        context.update({
            'blueprints': blueprints
        })
        return self.render('panels/routes.html', context)
