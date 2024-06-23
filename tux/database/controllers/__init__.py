from .cases import CaseController
from .notes import NoteController
from .reminders import ReminderController
from .snippets import SnippetController
from .users import UserController


class DatabaseController:
    def __init__(self):
        self.users = UserController()
        self.cases = CaseController()
        self.notes = NoteController()
        self.snippets = SnippetController()
        self.reminders = ReminderController()
