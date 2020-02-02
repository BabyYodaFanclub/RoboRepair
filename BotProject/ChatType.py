
from enum import Enum, unique


@unique
class ChatType(Enum):
    TEXT = 'text'
    VOICE = 'voice'
