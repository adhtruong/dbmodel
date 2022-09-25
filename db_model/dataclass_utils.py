import sys
from typing import Dict

KW_ONLY: Dict[str, bool]

if sys.version_info < (3, 10):
    KW_ONLY = {}
else:
    KW_ONLY = {"kw_only": True}
