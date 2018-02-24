import glob
import json
import os

from jinja2 import Template, Environment, FileSystemLoader


THIS_DIR, _ = os.path.split(__file__)
TEMPLATES_DIR = os.path.join(THIS_DIR, 'templates')

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def load_notebook_as_template(template_name):
    fname = 'tpl-' + template_name + '.ipynb'
    template = open(os.path.join(TEMPLATES_DIR, fname)).read()
    return template


def load_HTML_template(html_file, context):
    with open(html_file) as f:
        content = f.read()
    template = [i + '\n' for i in Template(content).render(context).splitlines()]
    return json.dumps(template)


def make_doc(template_name, **kwargs):
    template = load_notebook_as_template(template_name)

    # load html templates and fill context
    context = {}
    for key, value in kwargs.items():
        context[key] = value
    custom_css = os.path.join(TEMPLATES_DIR, 'custom-css.py')
    header = os.path.join(TEMPLATES_DIR, 'header.html')
    context['custom-css'] = load_HTML_template(custom_css, context)
    context['header'] = load_HTML_template(header, context)

    template = template.replace('[\n    "{%header%}"\n   ]', context['header'])
    template = template.replace('[\n    "{%custom-css%}"\n   ]', context['custom-css'])

    # once the template has been rendered remove jinja2 scape code from
    # cell code
    template = template.replace('{% raw %}', '')
    template = template.replace('{% endraw %}', '')

    doc_name = '{}.ipynb'.format(template_name)
    with open(doc_name, 'w') as ipynb:
        ipynb.write(template)


# Creates the .ipynb doc files
templates = {'map-styles': {'title': 'Styles'},
             'markers': {'title': 'Markers'}}

for name in templates:
    make_doc(name, title=templates[name]['title'])


for notebook in glob.glob('*.ipynb'):
    print('Running {}'.format(notebook))
    cmd = 'jupyter nbconvert --execute --to notebook --inplace {}'.format(notebook)
    os.system(cmd)
