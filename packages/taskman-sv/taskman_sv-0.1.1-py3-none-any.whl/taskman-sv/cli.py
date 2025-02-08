"""Command-line interface for TASKMAN"""
import sys
import argparse
from . import __version__
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

def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="TASKMAN - A secure task management and note-taking application"
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'TASKMAN {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add task
    add_parser = subparsers.add_parser('add', help='Add a new task')
    
    # Edit task
    edit_parser = subparsers.add_parser('edit', help='Edit an existing task')
    edit_parser.add_argument('task_id', type=int, help='Task ID to edit')
    
    # Delete task
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='Task ID to delete')
    
    # Start task
    start_parser = subparsers.add_parser('start', help='Start a task')
    start_parser.add_argument('task_id', type=int, help='Task ID to start')
    
    # Resume task
    resume_parser = subparsers.add_parser('resume', help='Resume a paused task')
    resume_parser.add_argument('task_id', type=int, help='Task ID to resume')
    
    # Notes
    notes_parser = subparsers.add_parser('notes', help='Open notes interface')
    
    # Fast notes
    fastnotes_parser = subparsers.add_parser('fastnotes', help='Open fast notes interface')
    
    # Report
    report_parser = subparsers.add_parser('report', help='Generate daily report')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_task()
    elif args.command == 'edit':
        edit_task(args.task_id)
    elif args.command == 'delete':
        delete_task(f"d{args.task_id}")
    elif args.command == 'start':
        start_task(args.task_id)
    elif args.command == 'resume':
        resume_task(args.task_id)
    elif args.command == 'notes':
        notes_interface()
    elif args.command == 'fastnotes':
        fast_notes_interface()
    elif args.command == 'report':
        generate_daily_report()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()