from IPython.core.display import Javascript, display, HTML
import re

class D3Notebook(object):

    render_id = 0

    @classmethod
    def _get_id(cls):

        cls.render_id += 1
        return cls.render_id

    def __init__(self, ver="3.5.17"):
        self._vars = {}
        self._js = {}
        self._ver = ver

        self._included_js = False

        # Automatically Add D3 Here
        self._include_d3()

    def render(self, name, *data):
        """
        Renders js according to name. Binds data as data-element
        :param name:
        :return:
        """
        self._include_d3()
        self._render(name, *data)

    def _include_d3(self):
        if not self._included_js:
            js = """
            requirejs.config({
                paths: {
                    d3: "//cdnjs.cloudflare.com/ajax/libs/d3/""" + str(self._ver) + """/d3.min"
                }
            });
            require(['d3'], function(d3) {
                window.d3 = d3;
            });
            """
            display(Javascript(js))
            self._included_js = True

    def _render(self, name, *data):

        js, css = self._js[name]
        data = [self._vars[d] for d in data]
        html = "<g></g>"
        data = data[0]
        js = self._bind_js(js, "\"" + "g#{}".format(self._get_id()) + "\"", data)

        html_string = "<g>{}\n <style>{}</style>\n <script>{}</script></g>".format(html, css, js)
        display(HTML(html_string))

    def _bind_js(self, js, selector, data):

        selector_regex = r'(d3\.select\()([0-9a-zA-Z#\.]*)(\))'
        data_regex = r'(\.data\()([0-9a-zA-Z#\.]*)(\))'

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
            if not isinstance(javascript, basestring):
                self._js[name] = javascript
            else:
                self._js[name] = (javascript, "")
