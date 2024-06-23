from enum import Enum


class CaseType(Enum):
    BAN = "BAN"
    HACK_BAN = "HACK_BAN"
    TEMP_BAN = "TEMP_BAN"
    UNBAN = "UNBAN"
    WARN = "WARN"
    KICK = "KICK"
    TIMEOUT_ADD = "TIMEOUT_ADD"
    TIMEOUT_REMOVE = "TIMEOUT_REMOVE"
