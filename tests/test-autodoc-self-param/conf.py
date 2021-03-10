import sys
import os


doc_module_path = os.path.dirname(__file__)
if doc_module_path not in sys.path:
    sys.path.append(doc_module_path)


extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.prettyspecialmethods',
]


# The suffix of source filenames.
source_suffix = '.rst'


autodoc_default_options = {
    'member-order': 'bysource',
    'exclude-members': '__weakref__,__dict__,__module__',
}
