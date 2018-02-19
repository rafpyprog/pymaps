from css_html_js_minify.js_minifier import js_minify_keep_comments
from jinja2 import Template


class MapElement():
    def __init__(self, element_name):
        self.element_name = element_name
        self.template = ''

    def render(self, minify=True):
        context = self.__dict__.copy()
        context.pop('element_name')
        context.pop('template')
        html = Template(self.template).render(**context)
        if minify:
            html = js_minify_keep_comments(html)
        return html

    @property
    def html(self):
        return self.render()

    def add_to(self, parent):
        parent.add_child(self)
