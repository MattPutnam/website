from os import path, listdir

import yaml

from htmpl import compile_template

root = path.dirname(path.dirname(path.abspath(__file__)))


def load_or_die(*paths):
    filename = path.join(root, *paths)
    ext = path.splitext(filename)[1][1:]
    if ext == 'yaml':
        with open(filename) as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as e:
                print(e)
                exit(-1)
    else:
        with open(filename) as stream:
            return stream.read()


compiled_page_template = compile_template(load_or_die('templates', 'page.htmpl'))


def write(template_data, title, content, *paths):
    template_data.bind('local', {'title': title, 'content': content})
    page = compiled_page_template.evaluate(template_data)

    with open(path.join(root, *paths), 'w') as stream:
        stream.write(page)
