from IPython.core.display import Javascript, display, HTML
import re

class D3Notebook(object):
    def __init__(self, ver="3.5.17"):
        self._vars = {}
        self._js = {}
        self._ver = ver

        self._included_js = False

    def render(self, name, *data):
        """
        Renders js according to name. Binds data as data-element
        :param name:
        :return:
        """
        self._include_d3()
        self._render(name=name, *data)

    def _include_d3(self):
        if not self._included_js:
            js = """
            requirejs.config({
                paths: {
                    d3: "//cdnjs.cloudflare.com/ajax/libs/d3/""" + str(self._ver) + """/d3"
                }
            });
            require(['d3'], function(d3) {
                window.d3 = d3;
            });
            """
            display(Javascript(js))
            self._included_js = True

    def _render(self, name, *data):

        js = self._js[name]
        html = "<g></g>"
        data = data[0]
        js = self._bind_js(js, "g", data)

        html = "{} <script>{}</script>".format(html, js)
        display(HTML(html))

    def _bind_js(self, js, selector, data):

        selector_regex = r'(d3\.select\()(.*)(\))'
        data_regex = r'(\.data\()(.*)(\))'

        js = re.sub(selector_regex, r'\1{}\3'.format(selector), js)
        js = re.sub(data_regex, r'\1{}\3'.format(data), js)

        return js

    def register_vars(self, **vars):
        """
        Provides Python => Javascript communication.
        :param data:
        :return:
        """
        for name, variable in vars.iteritems():
            self._vars[name] = variable

    def register_js(self, **js):
        """
        Registers js code under a name
        :param js:
        :return:
        """
        for name, javascript in js.iteritems():
            self._js[name] = javascript
