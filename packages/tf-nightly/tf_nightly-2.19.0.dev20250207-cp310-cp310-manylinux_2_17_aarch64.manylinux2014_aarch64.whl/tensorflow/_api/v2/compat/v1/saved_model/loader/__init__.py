# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.saved_model.loader namespace
"""

import sys as _sys

from tensorflow.python.saved_model.loader_impl import load # line: 278
from tensorflow.python.saved_model.loader_impl import maybe_saved_model_directory # line: 225

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "saved_model.loader", public_apis=None, deprecation=False,
      has_lite=False)
