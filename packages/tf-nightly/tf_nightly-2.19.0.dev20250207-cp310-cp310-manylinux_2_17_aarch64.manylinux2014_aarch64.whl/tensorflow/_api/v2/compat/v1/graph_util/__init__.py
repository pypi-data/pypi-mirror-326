# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.graph_util namespace
"""

import sys as _sys

from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants # line: 1301
from tensorflow.python.framework.graph_util_impl import extract_sub_graph # line: 221
from tensorflow.python.framework.graph_util_impl import must_run_on_cpu # line: 105
from tensorflow.python.framework.graph_util_impl import remove_training_nodes # line: 282
from tensorflow.python.framework.graph_util_impl import tensor_shape_from_node_def_name # line: 264
from tensorflow.python.framework.importer import import_graph_def # line: 358

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "graph_util", public_apis=None, deprecation=False,
      has_lite=False)
