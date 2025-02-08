"""
TASKMAN - A secure task management and note-taking application
"""

__version__ = "0.1.1"

from .taskman_backend import TaskmanBackend
from .interface import (
    add_task,
    edit_task,
    delete_task,
    start_task,
    resume_task,
    notes_interface,
    fast_notes_interface,
    generate_daily_report
)

__all__ = [
    'TaskmanBackend',
    'add_task',
    'edit_task',
    'delete_task',
    'start_task',
    'resume_task',
    'notes_interface',
    'fast_notes_interface',
    'generate_daily_report'
]