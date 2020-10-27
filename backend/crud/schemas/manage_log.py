from typing import Optional, Any

from pycurd.types import RecordMapping


class ManageLog(RecordMapping):
    id: bytes = None
    user_id: Optional[bytes]
    role: Optional[str]
    time: int = None
    related_type: int = None
    related_id: bytes = None
    related_user_id: Optional[bytes]
    operation: int = None
    value: Optional[Any]
    note: Optional[str]
