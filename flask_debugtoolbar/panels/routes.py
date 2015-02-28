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
        raw_endpoints = {}
        for endpoint, _rules in current_app.url_map._rules_by_endpoint.iteritems():
            if any(item in endpoint for item in ['_debug_toolbar', 'debugtoolbar', 'static']):
                continue

            for rule in _rules:
                rule.methods = sorted(filter(lambda x: x not in ['HEAD', 'OPTIONS'], rule.methods))

            if '.' in endpoint:
                blueprint_name = endpoint.split('.')[0]
                if not blueprint_name in blueprints:
                    blueprints[blueprint_name] = {}
                blueprints[blueprint_name][endpoint] = _rules
            else:
                raw_endpoints[endpoint] = _rules
        # Reorder
        blueprints = OrderedDict(sorted(blueprints.iteritems()))
        for key in blueprints.keys():
            blueprints[key] = OrderedDict(sorted(blueprints[key].iteritems()))
        raw_endpoints = OrderedDict(sorted(raw_endpoints.iteritems()))
        context.update({
            'blueprints': blueprints,
            'raw_endpoints': raw_endpoints
        })
        return self.render('panels/routes.html', context)


def remove_http_methods(rules):
    """Do not show HEAD, OPTION methods."""
    for rule in rules:
        rule.methods = sorted(filter(lambda x: x not in ['HEAD', 'OPTIONS'], rule.methods))
