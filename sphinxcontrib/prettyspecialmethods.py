"""
    sphinxcontrib.prettyspecialmethods
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Shows special methods as the python syntax that invokes them

    :copyright: Copyright 2018 by Thomas Smith
    :license: MIT, see LICENSE for details.
"""

import pbr.version
import sphinx.addnodes as SphinxNodes
from docutils.nodes import Text, emphasis, inline
from sphinx.transforms import SphinxTransform

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa

__version__ = pbr.version.VersionInfo(
    'prettyspecialmethods').version_string()


def patch_node(node, text=None, children=None, *, constructor=None):
    if constructor is None:
        constructor = node.__class__

    if text is None:
        text = node.text

    if children is None:
        children = node.children

    return constructor(
        node.source,
        text,
        *children,
        **node.attributes,
    )


def function_transformer(new_name):
    def xf(name_node, parameters_node):
        return (
            patch_node(name_node, new_name, ()),
            patch_node(parameters_node, '', [
                SphinxNodes.desc_parameter('', 'self'),
                *parameters_node.children,
            ])
        )

    return xf


def unary_op_transformer(op):
    def xf(name_node, parameters_node):
        return (
            patch_node(name_node, op, ()),
            emphasis('', 'self'),
        )

    return xf


def binary_op_transformer(op):
    def xf(name_node, parameters_node):
        return inline(
            '', '',
            emphasis('', 'self'),
            Text(' '),
            patch_node(name_node, op, ()),
            Text(' '),
            emphasis('', parameters_node.children[0].astext())
        )

    return xf


def brackets(parameters_node):
    return [
        emphasis('', 'self'),
        SphinxNodes.desc_name('', '', Text('[')),
        emphasis('', parameters_node.children[0].astext()),
        SphinxNodes.desc_name('', '', Text(']')),
    ]


SPECIAL_METHODS = {
    '__getitem__': lambda name_node, parameters_node: inline(
        '', '', *brackets(parameters_node)
    ),
    '__setitem__': lambda name_node, parameters_node: inline(
        '', '',
        *brackets(parameters_node),
        Text(' '),
        SphinxNodes.desc_name('', '', Text('=')),
        Text(' '),
        emphasis('', (
            (parameters_node.children[1].astext())
            if len(parameters_node.children) > 1 else ''
        )),
    ),
    '__delitem__': lambda name_node, parameters_node: inline(
        '', '',
        SphinxNodes.desc_name('', '', Text('del')),
        Text(' '),
        *brackets(parameters_node),
    ),
    '__contains__': lambda name_node, parameters_node: inline(
        '', '',
        emphasis('', parameters_node.children[0].astext()),
        Text(' '),
        SphinxNodes.desc_name('', '', Text('in')),
        Text(' '),
        emphasis('', 'self'),
    ),

    '__await__': lambda name_node, parameters_node: inline(
        '', '',
        SphinxNodes.desc_name('', '', Text('await')),
        Text(' '),
        emphasis('', 'self'),
    ),

    '__lt__': binary_op_transformer('<'),
    '__le__': binary_op_transformer('<='),
    '__eq__': binary_op_transformer('=='),
    '__ne__': binary_op_transformer('!='),
    '__gt__': binary_op_transformer('>'),
    '__ge__': binary_op_transformer('>='),

    '__hash__': function_transformer('hash'),
    '__len__': function_transformer('len'),
    '__iter__': function_transformer('iter'),
    '__str__': function_transformer('str'),
    '__repr__': function_transformer('repr'),

    '__add__': binary_op_transformer('+'),
    '__sub__': binary_op_transformer('-'),
    '__mul__': binary_op_transformer('*'),
    '__matmul__': binary_op_transformer('@'),
    '__truediv__': binary_op_transformer('/'),
    '__floordiv__': binary_op_transformer('//'),
    '__mod__': binary_op_transformer('%'),
    '__divmod__': function_transformer('divmod'),
    '__pow__': binary_op_transformer('**'),
    '__lshift__': binary_op_transformer('<<'),
    '__rshift__': binary_op_transformer('>>'),
    '__and__': binary_op_transformer('&'),
    '__xor__': binary_op_transformer('^'),
    '__or__': binary_op_transformer('|'),

    '__neg__': unary_op_transformer('-'),
    '__pos__': unary_op_transformer('+'),
    '__abs__': function_transformer('abs'),
    '__invert__': unary_op_transformer('~'),

    '__call__': lambda name_node, parameters_node: (
        emphasis('', 'self'),
        patch_node(parameters_node, '', parameters_node.children)
    ),
    '__getattr__': function_transformer('getattr'),
    '__setattr__': function_transformer('setattr'),
    '__delattr__': function_transformer('delattr'),

    '__bool__': function_transformer('bool'),
    '__int__': function_transformer('int'),
    '__float__': function_transformer('float'),
    '__complex__': function_transformer('complex'),
    '__bytes__': function_transformer('bytes'),

    # could show this as "{:...}".format(self) if we wanted
    '__format__': function_transformer('format'),

    '__index__': function_transformer('operator.index'),
    '__length_hint__': function_transformer('operator.length_hint'),
    '__ceil__': function_transformer('math.ceil'),
    '__floor__': function_transformer('math.floor'),
    '__trunc__': function_transformer('math.trunc'),
    '__round__': function_transformer('round'),

    '__sizeof__': function_transformer('sys.getsizeof'),
    '__dir__': function_transformer('dir'),
    '__reversed__': function_transformer('reversed'),
}


class PrettifySpecialMethods(SphinxTransform):
    default_priority = 800

    def apply(self):
        methods = (
            sig for sig in self.document.traverse(SphinxNodes.desc_signature)
            if 'class' in sig
        )

        for ref in methods:
            name_node = ref.next_node(SphinxNodes.desc_name)
            method_name = name_node.astext()

            if method_name in SPECIAL_METHODS:
                parameters_node = ref.next_node(SphinxNodes.desc_parameterlist)

                name_node.replace_self(SPECIAL_METHODS[method_name](name_node, parameters_node))
                parameters_node.replace_self(())


def show_special_methods(app, what, name, obj, skip, options):
    if what == 'class' and name in SPECIAL_METHODS and getattr(obj, '__doc__', None):
        return False


def setup(app):
    # type: (Sphinx) -> Dict[str, Any]
    app.add_transform(PrettifySpecialMethods)
    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-skip-member', show_special_methods)
    return {'version': __version__, 'parallel_read_safe': True}
