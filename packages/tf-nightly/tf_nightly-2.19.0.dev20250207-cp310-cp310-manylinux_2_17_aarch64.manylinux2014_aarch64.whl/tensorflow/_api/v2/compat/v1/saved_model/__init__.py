# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.saved_model namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.saved_model import builder
from tensorflow._api.v2.compat.v1.saved_model import constants
from tensorflow._api.v2.compat.v1.saved_model import experimental
from tensorflow._api.v2.compat.v1.saved_model import loader
from tensorflow._api.v2.compat.v1.saved_model import main_op
from tensorflow._api.v2.compat.v1.saved_model import signature_constants
from tensorflow._api.v2.compat.v1.saved_model import signature_def_utils
from tensorflow._api.v2.compat.v1.saved_model import tag_constants
from tensorflow._api.v2.compat.v1.saved_model import utils
from tensorflow.python.saved_model.builder_impl import SavedModelBuilder as Builder # line: 474
from tensorflow.python.saved_model.constants import ASSETS_DIRECTORY # line: 26
from tensorflow.python.saved_model.constants import ASSETS_KEY # line: 37
from tensorflow.python.saved_model.constants import DEBUG_DIRECTORY # line: 97
from tensorflow.python.saved_model.constants import DEBUG_INFO_FILENAME_PB # line: 107
from tensorflow.python.saved_model.constants import LEGACY_INIT_OP_KEY # line: 45
from tensorflow.python.saved_model.constants import MAIN_OP_KEY # line: 53
from tensorflow.python.saved_model.constants import SAVED_MODEL_FILENAME_PB # line: 76
from tensorflow.python.saved_model.constants import SAVED_MODEL_FILENAME_PBTXT # line: 88
from tensorflow.python.saved_model.constants import SAVED_MODEL_SCHEMA_VERSION # line: 64
from tensorflow.python.saved_model.constants import VARIABLES_DIRECTORY # line: 116
from tensorflow.python.saved_model.constants import VARIABLES_FILENAME # line: 125
from tensorflow.python.saved_model.load import load as load_v2 # line: 820
from tensorflow.python.saved_model.loader_impl import maybe_saved_model_directory as contains_saved_model # line: 225
from tensorflow.python.saved_model.loader_impl import load # line: 278
from tensorflow.python.saved_model.loader_impl import maybe_saved_model_directory # line: 225
from tensorflow.python.saved_model.main_op_impl import main_op_with_restore # line: 48
from tensorflow.python.saved_model.save import save # line: 1241
from tensorflow.python.saved_model.save_options import SaveOptions # line: 93
from tensorflow.python.saved_model.signature_constants import CLASSIFY_INPUTS # line: 38
from tensorflow.python.saved_model.signature_constants import CLASSIFY_METHOD_NAME # line: 47
from tensorflow.python.saved_model.signature_constants import CLASSIFY_OUTPUT_CLASSES # line: 56
from tensorflow.python.saved_model.signature_constants import CLASSIFY_OUTPUT_SCORES # line: 65
from tensorflow.python.saved_model.signature_constants import DEFAULT_SERVING_SIGNATURE_DEF_KEY # line: 25
from tensorflow.python.saved_model.signature_constants import PREDICT_INPUTS # line: 77
from tensorflow.python.saved_model.signature_constants import PREDICT_METHOD_NAME # line: 86
from tensorflow.python.saved_model.signature_constants import PREDICT_OUTPUTS # line: 95
from tensorflow.python.saved_model.signature_constants import REGRESS_INPUTS # line: 107
from tensorflow.python.saved_model.signature_constants import REGRESS_METHOD_NAME # line: 116
from tensorflow.python.saved_model.signature_constants import REGRESS_OUTPUTS # line: 125
from tensorflow.python.saved_model.signature_def_utils_impl import build_signature_def # line: 30
from tensorflow.python.saved_model.signature_def_utils_impl import classification_signature_def # line: 133
from tensorflow.python.saved_model.signature_def_utils_impl import is_valid_signature # line: 293
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def # line: 196
from tensorflow.python.saved_model.signature_def_utils_impl import regression_signature_def # line: 82
from tensorflow.python.saved_model.simple_save import simple_save # line: 26
from tensorflow.python.saved_model.tag_constants import GPU # line: 44
from tensorflow.python.saved_model.tag_constants import SERVING # line: 23
from tensorflow.python.saved_model.tag_constants import TPU # line: 51
from tensorflow.python.saved_model.tag_constants import TRAINING # line: 31
from tensorflow.python.saved_model.utils_impl import build_tensor_info # line: 41
from tensorflow.python.saved_model.utils_impl import get_tensor_from_tensor_info # line: 143
from tensorflow.python.trackable.asset import Asset # line: 30

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "saved_model", public_apis=None, deprecation=False,
      has_lite=False)
