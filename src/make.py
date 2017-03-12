import collections

from htmpl import TemplateData, evaluate_template
from utils import load_or_die, write

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
    main_data = load_or_die('src', 'main.yaml')
    pages = main_data['Pages']

    template_data = TemplateData({'pages': pages}, '', [])

    for page in pages:
        template = load_or_die('templates', page['template'])
        write(template_data, page['Title'], evaluate_template(template, template_data), 'rendered', page['URL'])


if __name__ == '__main__':
    main()
