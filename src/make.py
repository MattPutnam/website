import collections
import shutil
import os
from os import path

from htmpl import TemplateData, evaluate_template
from utils import root, load_or_die, write

import yaml


# Setup yaml importer to use OrderedDict
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())


def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))

yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)


def main():
    clean()

    main_data = load_or_die('src', 'main.yaml')

    template_data = TemplateData(main_data, '', [])

    for page in main_data['Pages']:
        template = load_or_die('templates', page['template'])
        write(template_data, page['Title'], evaluate_template(template, template_data), 'rendered', page['URL'])

    shutil.copytree(path.join(root, 'style'), path.join(root, 'rendered', 'style'))


def clean():
    rendered_dir = path.join(root, 'rendered')
    shutil.rmtree(rendered_dir, ignore_errors=True)
    os.makedirs(rendered_dir)


if __name__ == '__main__':
    main()
