"""
    sphinxcontrib.prettyspecialmethods
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Shows special methods as the python syntax that invokes them

    :copyright: Copyright 2018 by Thomas Smith
    :license: MIT, see LICENSE for details.
"""

import pbr.version
import sphinx.addnodes as SphinxNodes
from sphinx.transforms import SphinxTransform
from docutils.nodes import Text, emphasis, field, field_name, field_body, inline, pending

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from docutils.nodes import Node  # noqa
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
    def xf(name_node, parameters_node, self_param):
        return (
            patch_node(name_node, new_name, ()),
            patch_node(parameters_node, '', [
                SphinxNodes.desc_parameter('', self_param),
                *parameters_node.children,
            ])
        )

    return xf


def unary_op_transformer(op):
    def xf(name_node, parameters_node, self_param):
        return (
            patch_node(name_node, op, ()),
            emphasis('', self_param),
        )

    return xf


def binary_op_transformer(op):
    def xf(name_node, parameters_node, self_param):
        return inline(
            '', '',
            emphasis('', self_param),
            Text(' '),
            patch_node(name_node, op, ()),
            Text(' '),
            emphasis('', parameters_node.children[0].astext())
        )

    return xf


def brackets(parameters_node, self_param):
    return [
        emphasis('', self_param),
        SphinxNodes.desc_name('', '', Text('[')),
        emphasis('', parameters_node.children[0].astext()),
        SphinxNodes.desc_name('', '', Text(']')),
    ]


SPECIAL_METHODS = {
    '__getitem__': lambda name_node, parameters_node, self_param: inline(
        '', '', *brackets(parameters_node, self_param)
    ),
    '__setitem__': lambda name_node, parameters_node, self_param: inline(
        '', '',
        *brackets(parameters_node, self_param),
        Text(' '),
        SphinxNodes.desc_name('', '', Text('=')),
        Text(' '),
        emphasis('', (
            (parameters_node.children[1].astext())
            if len(parameters_node.children) > 1 else ''
        )),
    ),
    '__delitem__': lambda name_node, parameters_node, self_param: inline(
        '', '',
        SphinxNodes.desc_name('', '', Text('del')),
        Text(' '),
        *brackets(parameters_node, self_param),
    ),
    '__contains__': lambda name_node, parameters_node, self_param: inline(
        '', '',
        emphasis('', parameters_node.children[0].astext()),
        Text(' '),
        SphinxNodes.desc_name('', '', Text('in')),
        Text(' '),
        emphasis('', self_param),
    ),

    '__await__': lambda name_node, parameters_node, self_param: inline(
        '', '',
        SphinxNodes.desc_name('', '', Text('await')),
        Text(' '),
        emphasis('', self_param),
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

    '__call__': lambda name_node, parameters_node, self_param: (
        emphasis('', self_param),
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


class PendingSelfParamName(pending):
    def __init__(self, name):
        # type: (str) -> None
        super().__init__(
            transform=PrettifySpecialMethods,
            details={'self_param': name},
        )

    @property
    def name(self):
        # type: () -> str
        return self.details['self_param']


def is_meta_self_param_info_field(node):
    # type: (Node) -> bool
    if not isinstance(node, field):
        return False

    name = node.next_node(field_name).astext()
    return name == 'meta self-param'


def convert_meta_self_param(app, domain, objtype, contentnode):
    # type: (Sphinx, str, str, Node) -> None
    if not domain == 'py' or 'method' not in objtype:
        return

    # Note: Using next_node means we only find the first instance
    # of selfparam. Additional selfparam fields are ignored and eventually
    # deleted by the Python domain's meta filter.
    selfparam_field = contentnode.next_node(is_meta_self_param_info_field)

    if selfparam_field:
        selfparam: str = selfparam_field.next_node(field_body).astext()
        contentnode.append(PendingSelfParamName(selfparam))
        selfparam_field.replace_self(())


class PrettifySpecialMethods(SphinxTransform):
    default_priority = 800

    def apply(self):
        methods = (
            sig.parent for sig in self.document.traverse(SphinxNodes.desc_signature)
            if 'class' in sig
        )

        for ref in methods:
            name_node = ref.next_node(SphinxNodes.desc_name)
            method_name = name_node.astext()

            if method_name in SPECIAL_METHODS:
                # Determine name to use for self in new specification
                # using first child occurence
                pending_self_param = ref.next_node(PendingSelfParamName)
                self_param = pending_self_param.name if pending_self_param else 'self'

                parameters_node = ref.next_node(SphinxNodes.desc_parameterlist)

                new_sig = SPECIAL_METHODS[method_name](name_node, parameters_node, self_param)

                name_node.replace_self(new_sig)
                parameters_node.replace_self(())

        # Remove ALL occurrences of PendingSelfParamName
        for p in self.document.traverse(PendingSelfParamName):
            p.replace_self(())


def show_special_methods(app, what, name, obj, skip, options):
    if what == 'class' and name in SPECIAL_METHODS and getattr(obj, '__doc__', None):
        return False


def setup(app):
    # type: (Sphinx) -> Dict[str, Any]
    app.add_transform(PrettifySpecialMethods)
    app.connect('object-description-transform', convert_meta_self_param, priority=450)
    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-skip-member', show_special_methods)
    return {'version': __version__, 'parallel_read_safe': True}
