from typing import Optional, Any

from pycurd.types import RecordMapping


class PostStats(RecordMapping):
    id: bytes = None
    post_type: int = None

    last_comment_id: Optional[bytes]
    last_edit_user_id: Optional[bytes]
    last_edit_time: Optional[int]
    update_time: Optional[int]

    click_count: int = 0
    edit_count: int = 0
    comment_count: int = 0
    topic_count: int = 0
    follow_count: int = 0
    bookmark_count: int = 0
    upvote_count: int = 0
    downvote_count: int = 0
    thank_count: int = 0
    vote_weight: int = 0


class StatsLog(RecordMapping):
    id: bytes = None
    time: int = None
    data: Any = None
