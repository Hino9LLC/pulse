"""WebSocket message schemas"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class WebSocketMessage(BaseModel):
    """Base WebSocket message schema"""

    type: str
    data: dict[str, Any] | None = None
    timestamp: datetime = datetime.now()


class WebSocketWelcome(WebSocketMessage):
    """Welcome message sent when client connects"""

    type: str = "welcome"


class WebSocketPing(WebSocketMessage):
    """Ping message for heartbeat"""

    type: str = "ping"


class WebSocketPong(WebSocketMessage):
    """Pong response to ping"""

    type: str = "pong"


class WebSocketItemCreated(WebSocketMessage):
    """Message sent when an item is created"""

    type: str = "item_created"


class WebSocketItemUpdated(WebSocketMessage):
    """Message sent when an item is updated"""

    type: str = "item_updated"


class WebSocketItemDeleted(WebSocketMessage):
    """Message sent when an item is deleted"""

    type: str = "item_deleted"


class WebSocketError(WebSocketMessage):
    """Error message"""

    type: str = "error"
