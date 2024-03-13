"""
Library used for shared interfaces between agents and the server.
"""

from base64 import b64decode, b64encode
from typing import Any, Optional, Union, Literal
from pydantic import BaseModel, field_validator, field_serializer
import uuid

class EndpointMessagingData(BaseModel):
    """
    Model containing additional information pulled from an Endpoint model.
    """
    name: str
    hostname: str
    address: str

class ServerMessagingData(BaseModel):
    action: Union[Literal["send"], Literal["receive"]]
    listen_for_id: uuid.UUID

    server_private_key: Optional[bytes]
    preferred_protocol: Optional[str]

    @field_validator(
        "server_private_key", mode="before"
    )
    @classmethod
    def validate_base64(cls, v: Any) -> Union[bytes, None]:
        """
        If the value passed into the configuration object is not bytes,
        assume base64.
        """
        if v is None or isinstance(v, bytes):
            return v

        try:
            val = b64decode(v)
        except Exception as e:
            raise ValueError(f"Assumed b64decode of {v} failed.") from e

        return val

    @field_serializer(
        "",
        when_used="json-unless-none",
    )
    @classmethod
    def serialize_bytes(cls, v: bytes) -> str:
        """
        Turn bytes into their base64 representation before it pops out of a JSON file.
        """
        return b64encode(v).decode("utf-8")

class MessagingObject(BaseModel):
    """
    Generic object used when passing data between the server and the agent.
    """
    agent_config: dict[str, Any]
    protocol_config: dict[str, Any]
    protocol_state: Optional[dict[str, Any]]
    model_data: EndpointMessagingData
    server_config: ServerMessagingData

    
