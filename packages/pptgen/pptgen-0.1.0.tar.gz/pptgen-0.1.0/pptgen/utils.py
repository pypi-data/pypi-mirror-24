import re
import six
import copy
import json
import yaml
import logging
import pandas as pd
from io import open
from copy import deepcopy
from orderedattrdict import AttrDict


def merge(old, new, mode='overwrite'):
    '''
    Update old dict with new dict recursively.

        >>> merge({'a': {'x': 1}}, {'a': {'y': 2}})
        {'a': {'x': 1, 'y': 2}}

    If ``mode='overwrite'``, the old dict is overwritten (default).
    If ``mode='setdefault'``, the old dict values are updated only if missing.

    Note: This is originally from gramex/config.py
    '''
    for key in new:
        if key in old and hasattr(old[key], 'items') and hasattr(new[key], 'items'):
            merge(old=old[key], new=new[key], mode=mode)
        else:
            if mode == 'overwrite' or key not in old:
                old[key] = deepcopy(new[key])
    return old


def parse_command_line(commands):
    '''
    Parse command line arguments. For example:

        gramex cmd1 cmd2 --a=1 2 -b x --c --p.q=4

    returns:

        {"_": ["cmd1", "cmd2"], "a": [1, 2], "b": "x", "c": True, "p": {"q": [4]}}

    Values are parsed as YAML. Arguments with '.' are split into subgroups. For
    example, ``gramex --listen.port 80`` returns ``{"listen": {"port": 80}}``.

    Note: This is originally from gramex/__init__.py
    '''
    group = '_'
    args = AttrDict({group: []})
    for arg in commands:
        if arg.startswith('-'):
            group, value = arg.lstrip('-'), 'True'
            if '=' in group:
                group, value = group.split('=', 1)
        else:
            value = arg

        value = yaml.load(value)
        base = args
        keys = group.split('.')
        for key in keys[:-1]:
            base = base.setdefault(key, AttrDict())

        # Add the key to the base.
        # If it's already a list, append to it.
        if keys[-1] not in base or base[keys[-1]] is True:
            base[keys[-1]] = value
        elif not isinstance(base[keys[-1]], list):
            base[keys[-1]] = [base[keys[-1]], value]
        else:
            base[keys[-1]].append(value)

    return args


def load_yaml(path, **kwargs):
    '''Load yaml file.'''
    encoding = kwargs.pop('encoding', 'utf-8')
    with open(path, encoding=encoding) as handle:
        return yaml.load(handle, **kwargs)


def load_json(path, **kwargs):
    kwargs.setdefault('encoding', 'utf-8')
    with open(path, encoding=kwargs['encoding']) as handle:
        return json.load(handle, **kwargs)


_data_loaders = {
    'csv': pd.read_csv,
    'xlsx': pd.read_excel,
    'json': load_json,
    'yaml': load_yaml,
    'values': dict,
}


def load_data(data_config):
    '''
    load_data({
      cities: {csv: help/cities.csv}    # Load CSV data into "cities" key
      sales: {xlsx: help/sales.xlsx, sheet: Sheet1}   # Load Sheet1 into "sales"
      tweets: {json: help/tweets.json}  # Load JSON data into "tweets" key
      config: {yaml: help/config.yaml}  # Load YAML data into "config"
      direct: {values: {x: 1, y: 2}}    # The "direct" key takes values directly
    })
    '''
    data = {}
    for key, conf in data_config.items():
        for fmt in _data_loaders:
            if fmt in conf:
                path = conf.pop(fmt)
                data[key] = _data_loaders[fmt](path, **conf)
                break
        else:
            logging.warn('data:%s needs a csv:, json:,...): %s', key, conf)
    return data


def is_slide_allowed(change, slide, number):
    '''
    Given a change like one of the below::

        slide-number: 1
        slide-number: [1, 2, 3]
        slide-title: 'company'
        slide-title: ['company', 'industry']

    ... return True if:

    1. ``number`` matches a slide-number
    2. ``slide`` title matches a slide-title regex (case-insensitive)

    If none of these are specified, return True.
    '''
    match = True
    # Restrict to specific slide titles, if specified
    if 'slide-number' in change:
        slide_number = change['slide-number']
        if isinstance(slide_number, (list, dict)):
            match = match and number in slide_number
        elif isinstance(slide_number, six.integer_types):
            match = match and number == slide_number

    # Restrict to specific slide titles, if specified
    if 'slide-title' in change:
        slide_title = change['slide-title']
        try:
            title = slide.shapes.title.text
        except AttributeError:
            title = ''
        if isinstance(slide_title, (list, dict)):
            match = match and any(
                re.search(expr, title, re.IGNORECASE) for expr in slide_title)
        elif isinstance(slide_title, six.string_types):
            match = match and re.search(slide_title, title, re.IGNORECASE)

    return match


def is_group(shape):
    # TODO: implement this
    return shape.element.tag.endswith('}grpSp')


def stack_elements(replica, shape, stack=False):
    '''
    Function to extend elements horizontally or vertically.
    '''
    config = {'vertical': {'axis': 'y', 'attr': 'height'},
              'horizontal': {'axis': 'x', 'attr': 'width'}}
    grp_sp = None
    if stack:
        grp_sp = shape.element
        # Adding a 15% margin between original and new object.
        met_margin = 0.15
        for index in range(replica - 1):
            # Adding a cloned object to shape
            extend_shape = copy.deepcopy(grp_sp)
            # Getting attributes and axis values from config based on stack.
            attr = config.get(stack, {}).get('attr', 0)
            axis = config.get(stack, {}).get('axis', 0)
            # Taking width or height based on stack value and setting a margin.
            metric_val = getattr(shape, attr)
            axis_val = getattr(extend_shape, axis)
            # Setting margin accordingly either vertically or horizontally.
            margin = round(metric_val * met_margin) + axis_val
            set_attr = (metric_val * (index + 1)) + margin
            # Setting graphic position of newly created object to slide.
            setattr(extend_shape, axis, int(set_attr))
            # Adding newly created object tomslide.
            grp_sp.addnext(extend_shape)

    return grp_sp
