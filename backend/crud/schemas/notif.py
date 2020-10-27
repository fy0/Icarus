from typing import Optional, Any, List

from pycurd.types import RecordMapping


class UserNotifLastInfo(RecordMapping):
    id: bytes = None
    last_be_commented_id: bytes = b'\x00'
    last_be_replied_id: bytes = b'\x00'
    last_be_followed_id: bytes = b'\x00'
    last_be_mentioned_id: bytes = b'\x00'
    last_be_bookmarked_id: bytes = b'\x00'
    last_be_liked_id: bytes = b'\x00'
    last_be_sent_pm_id: bytes = b'\x00'
    last_received_sysmsg_id: bytes = b'\x00'
    last_manage_log_id: bytes = b'\x00'
    update_time: int = None


class Notification(RecordMapping):
    id: bytes = None
    type: int = None
    time: int = None

    loc_post_type: int = None
    loc_post_id: bytes = None
    loc_post_title: Optional[str]

    sender_ids: List[bytes] = None
    receiver_id: bytes = None

    from_post_type: Optional[int]
    from_post_id: Optional[bytes]

    related_type: Optional[int]
    related_id: Optional[bytes]

    brief: Optional[str]

    data: Optional[Any]
    is_read: bool = False
