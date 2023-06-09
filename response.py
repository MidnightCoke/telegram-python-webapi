from dataclasses import dataclass
from typing import List

@dataclass
class MessageRequestResponse:
    phone_number: str
    id: int
    status: int
    description: str
    message_id: int


@dataclass
class ResponseData:
    Status: int
    Description: str
    Result: List[MessageRequestResponse]