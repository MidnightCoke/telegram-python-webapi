from dataclasses import dataclass
from typing import List

@dataclass
class MessageRequest:
    phone_number: str
    id: int
    status: int
    message_id: int


@dataclass
class ResponseData:
    Status: int
    Description: str
    Result: List[MessageRequest]