# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.tpu namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.tpu import experimental
from tensorflow.python.tpu.bfloat16 import bfloat16_scope # line: 69
from tensorflow.python.tpu.ops.tpu_ops import cross_replica_sum # line: 91
from tensorflow.python.tpu.tpu import PaddingSpec # line: 220
from tensorflow.python.tpu.tpu import XLAOptions # line: 230
from tensorflow.python.tpu.tpu import batch_parallel # line: 1365
from tensorflow.python.tpu.tpu import initialize_system # line: 82
from tensorflow.python.tpu.tpu import replicate # line: 257
from tensorflow.python.tpu.tpu import rewrite # line: 1428
from tensorflow.python.tpu.tpu import shard # line: 1278
from tensorflow.python.tpu.tpu import shutdown_system # line: 169
from tensorflow.python.tpu.tpu_name_util import core # line: 21
from tensorflow.python.tpu.tpu_optimizer import CrossShardOptimizer # line: 28
from tensorflow.python.tpu.tpu_replication import outside_compilation # line: 654

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "tpu", public_apis=None, deprecation=False,
      has_lite=False)
