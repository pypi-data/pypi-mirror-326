import os
import time
import msvcrt
import tempfile
import subprocess
from tqdm import tqdm
from colorama import Fore, Style, init
from datetime import datetime, date, timedelta
import sys
import time
import itertools
from taskman_backend import setup_backend, TaskmanBackend
import json

# Create a global backend instance
backend = TaskmanBackend()

# Initialize colorama
init(autoreset=True)

try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
except ImportError:
    engine = None

tasks = []  # List to store tasks
notes = {}  # Dictionary to store modular notes
quick_notes = []  # List to store quick notes
paused_task = None
current_progress = 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

init(autoreset=True)

def loading_animation():
    """Display a professional loading animation with a Matrix-style effect"""

    logo = f"""{Fore.GREEN}
  ████████╗ █████╗ ███████╗██╗  ██╗███╗   ███╗ █████╗ ███╗   ██╗
  ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝████╗ ████║██╔══██╗████╗  ██║
     ██║   ███████║███████╗█████╔╝ ██╔████╔██║███████║██╔██╗ ██║
     ██║   ██╔══██║╚════██║██╔═██╗ ██║╚██╔╝██║██╔══██║██║╚██╗██║
     ██║   ██║  ██║███████║██║  ██╗██║ ╚═╝ ██║██║  ██║██║ ╚████║
     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Fore.WHITE}                                                       by Shreedhar
    """
    
    print(logo)
    time.sleep(1.5)  # Show the logo briefly


def display_header(title="TASKMAN", module=None):
    """Clears the screen and displays the title at the top before the date."""
    clear_screen()
    
    # Get current hour to determine greeting
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    # Display greeting with username if available
    if hasattr(backend, 'user') and backend.user:
        print(f"\n{Fore.GREEN}{greeting}, {backend.user}! 👋")
    
    if module:
        print(f"\n{Fore.CYAN}🌟 {title} - {Fore.GREEN}{module} 🌟\n")
    else:
        print(f"\n{Fore.CYAN}🌟 {title} 🌟")
    
    today = datetime.now().strftime("%A, %d %B %Y")
    print(f"{Fore.CYAN}📅 {today}\n")

def get_valid_time_input(prompt):
    """Helper function to get valid numeric input for time"""
    while True:
        try:
            value = input(f"{Fore.CYAN}{prompt}")
            if not value.strip():  # Check for empty input
                print(f"{Fore.YELLOW}Please enter a number.")
                continue
            num = int(value)
            if num < 0:
                print(f"{Fore.YELLOW}Please enter a non-negative number.")
                continue
            return num
        except ValueError:
            print(f"{Fore.YELLOW}Please enter a valid number.")
            continue

def display_tasks():
    """Display all tasks including paused ones"""
    if tasks:
        print(f"{Fore.BLUE}📝 Active Tasks:")
        for i, task in enumerate(tasks, 1):
            hrs = task['duration'] // 3600 if 'duration' in task else 0
            mins = (task['duration'] % 3600) // 60 if 'duration' in task else 0
            status = task['status']
            
            # Add task type badge with updated colors
            if task['mode'] == 'custom':
                badge = f"{Fore.CYAN}[🛠️]"
            else:  # pomodoro
                badge = f"{Fore.LIGHTRED_EX}[🍅 POMO]"
            
            # Check if task has a creation date and it's from a previous day
            creation_date = task.get('creation_date', datetime.now().strftime('%Y-%m-%d'))
            today = datetime.now().strftime('%Y-%m-%d')
            carryforward_info = ""
            if creation_date != today:
                carryforward_info = f"{Fore.YELLOW}[↻ from {creation_date}] "
            
            # Display task with badge, number, name, duration, status and carryforward info
            if task['mode'] == 'custom':
                print(f"{badge} {i}. {carryforward_info}{task['name']} [{hrs}h {mins}m] - {status}")
            else:
                settings = task['pomodoro_settings']
                completed = settings.get('current_pomodoro', 0)
                total = settings.get('num_pomodoros', 0)
                print(f"{badge} {i}. {carryforward_info}{task['name']} [{completed}/{total} Pomodoros] - {status}")
            
            if task['description']:
                print(f"   Description: {task['description']}")
            print("   ────────────────────────────────────────")
    else:
        print(f"{Fore.YELLOW}No active tasks! Add some first.")
    print()

def speak(text):
    """Simple voice announcement"""
    if not engine:
        return
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"{Fore.RED}Voice error: {str(e)}")

def add_task():
    """Add a new task with Pomodoro or Custom timing options"""
    while True:
        # First ask for task type
        print(f"\n{Fore.CYAN}Task Type:")
        print(f"{Fore.YELLOW}1. Custom Task")
        print(f"{Fore.YELLOW}2. Pomodoro Task")
        
        task_type = input(f"\n{Fore.CYAN}Choose task type (1/2): ").strip()
        
        # Get common task details
        name = input(f"\n{Fore.CYAN}Enter task name: ").strip()
        while not name:
            print(f"{Fore.YELLOW}Task name cannot be empty.")
            name = input(f"{Fore.CYAN}Enter task name: ").strip()
        
        description = input(f"{Fore.CYAN}Enter a brief description: ").strip()
        while not description:
            print(f"{Fore.YELLOW}Description cannot be empty.")
            description = input(f"{Fore.CYAN}Enter a brief description: ").strip()
        
        # Handle different task types
        if task_type == "1":  # Custom Task
            # Get duration
            while True:
                try:
                    hours = int(input(f"{Fore.CYAN}Estimated hours: "))
                    if hours < 0:
                        print(f"{Fore.YELLOW}Hours cannot be negative.")
                        continue
                    if hours > 24:
                        print(f"{Fore.YELLOW}Warning: That's a long task! Are you sure?")
                    
                    minutes = int(input(f"{Fore.CYAN}Estimated minutes: "))
                    if minutes < 0 or minutes >= 60:
                        print(f"{Fore.YELLOW}Minutes must be between 0 and 59.")
                        continue
                    break
                except ValueError:
                    print(f"{Fore.YELLOW}Please enter valid numbers.")
            
            total_seconds = hours * 3600 + minutes * 60
            task_mode = "custom"
            
        elif task_type == "2":  # Pomodoro Task
            print(f"\n{Fore.CYAN}Pomodoro Settings:")
            print(f"{Fore.YELLOW}1. Standard (25min work, 5min break, 15min long break)")
            print(f"{Fore.YELLOW}2. Long (45min work, 15min break, 30min long break)")
            print(f"{Fore.YELLOW}3. Custom Pomodoro")
            
            pomo_type = input(f"\n{Fore.CYAN}Choose Pomodoro type (1/2/3): ").strip()
            
            if pomo_type == "1":
                work_duration = 25
                break_duration = 5
                long_break_duration = 15
            elif pomo_type == "2":
                work_duration = 45
                break_duration = 15
                long_break_duration = 30
            elif pomo_type == "3":
                work_duration = get_valid_time_input("Work duration (minutes): ")
                break_duration = get_valid_time_input("Break duration (minutes): ")
                long_break_duration = get_valid_time_input("Long break duration (minutes): ")
            else:
                print(f"{Fore.RED}Invalid choice. Using standard Pomodoro settings.")
                work_duration = 25
                break_duration = 5
                long_break_duration = 15
            
            num_pomodoros = get_valid_time_input("Number of Pomodoros: ")
            total_seconds = (work_duration * 60 * num_pomodoros) + \
                           (break_duration * 60 * (num_pomodoros - 1)) + \
                           (long_break_duration * 60)  # One long break at the end
            
            task_mode = "pomodoro"
        else:
            print(f"{Fore.RED}Invalid task type! Please try again.")
            continue
        
        # Show summary and get confirmation
        print(f"\n{Fore.GREEN}Task Summary:")
        print(f"{Fore.CYAN}Name: {Fore.WHITE}{name}")
        print(f"{Fore.CYAN}Description: {Fore.WHITE}{description}")
        
        if task_type == "1":
            hrs = total_seconds // 3600
            mins = (total_seconds % 3600) // 60
            print(f"{Fore.CYAN}Duration: {Fore.WHITE}{hrs}h {mins}m")
        else:
            print(f"{Fore.CYAN}Pomodoro Settings:")
            print(f"{Fore.WHITE}  Work Duration: {work_duration}min")
            print(f"{Fore.WHITE}  Break Duration: {break_duration}min")
            print(f"{Fore.WHITE}  Long Break Duration: {long_break_duration}min")
            print(f"{Fore.WHITE}  Number of Pomodoros: {num_pomodoros}")
            print(f"{Fore.WHITE}  Total Duration: {total_seconds//3600}h {(total_seconds%3600)//60}m")
        
        confirm = input(f"\n{Fore.YELLOW}Is this correct? (y/n): ").lower()
        if confirm == 'y':
            break
        print(f"\n{Fore.CYAN}Let's try again.")
    
    task_data = {
        "name": name,
        "description": description,
        "duration": total_seconds,
        "status": f"{Fore.YELLOW}Pending",
        "mode": task_mode,
        "creation_date": datetime.now().strftime('%Y-%m-%d')
    }
    
    # Add Pomodoro-specific data if applicable
    if task_mode == "pomodoro":
        task_data.update({
            "pomodoro_settings": {
                "work_duration": work_duration,
                "break_duration": break_duration,
                "long_break_duration": long_break_duration,
                "num_pomodoros": num_pomodoros,
                "current_pomodoro": 0
            }
        })
    
    tasks.append(task_data)
    print(f"{Fore.GREEN}» Task added! ✅")

def edit_task(task_index):
    """Edit an existing task's details"""
    try:
        task = tasks[task_index-1]
    except IndexError:
        print(f"{Fore.RED}Invalid task number!")
        return

    while True:
        clear_screen()
        print(f"\n{Fore.GREEN}Current Task Details:")
        print(f"{Fore.CYAN}1. Name: {Fore.WHITE}{task['name']}")
        print(f"{Fore.CYAN}2. Description: {Fore.WHITE}{task['description']}")
        
        hours = task['duration'] // 3600
        minutes = (task['duration'] % 3600) // 60
        print(f"{Fore.CYAN}3. Duration: {Fore.WHITE}{hours}h {minutes}m")
        print(f"{Fore.CYAN}4. Status: {task['status']}")
        
        print(f"\n{Fore.YELLOW}What would you like to edit?")
        
        # Show different options based on task status
        if "Completed" in task['status']:
            print(f"{Fore.YELLOW}1. Name")
            print(f"{Fore.YELLOW}2. Description")
            print(f"{Fore.YELLOW}3. Save and Exit")
            valid_choices = ['1', '2', '3']
        else:
            print(f"{Fore.YELLOW}1. Name")
            print(f"{Fore.YELLOW}2. Description")
            print(f"{Fore.YELLOW}3. Duration")
            print(f"{Fore.YELLOW}4. Save and Exit")
            valid_choices = ['1', '2', '3', '4']
        
        choice = input(f"\n{Fore.GREEN}Choice (1-{len(valid_choices)}): ").strip()
        
        if choice not in valid_choices:
            print(f"{Fore.RED}Invalid choice!")
            time.sleep(1)
            continue
        
        if choice == '1':
            new_name = input(f"{Fore.CYAN}Enter new name: ").strip()
            while not new_name:
                print(f"{Fore.YELLOW}Name cannot be empty.")
                new_name = input(f"{Fore.CYAN}Enter new name: ").strip()
            task['name'] = new_name
            print(f"{Fore.GREEN}» Name updated!")
            time.sleep(1)
        
        elif choice == '2':
            new_desc = input(f"{Fore.CYAN}Enter new description: ").strip()
            while not new_desc:
                print(f"{Fore.YELLOW}Description cannot be empty.")
                new_desc = input(f"{Fore.CYAN}Enter new description: ").strip()
            task['description'] = new_desc
            print(f"{Fore.GREEN}» Description updated!")
            time.sleep(1)
        
        elif choice == '3' and "Completed" not in task['status']:
            try:
                print(f"{Fore.CYAN}Current duration: {hours}h {minutes}m")
                while True:
                    try:
                        new_hours = int(input(f"{Fore.CYAN}Enter new hours: "))
                        if new_hours < 0:
                            print(f"{Fore.YELLOW}Hours cannot be negative.")
                            continue
                        if new_hours > 24:
                            confirm = input(f"{Fore.YELLOW}Are you sure you want to set {new_hours} hours? (y/n): ").lower()
                            if confirm != 'y':
                                continue
                        
                        new_minutes = int(input(f"{Fore.CYAN}Enter new minutes: "))
                        if new_minutes < 0 or new_minutes >= 60:
                            print(f"{Fore.YELLOW}Minutes must be between 0 and 59.")
                            continue
                        break
                    except ValueError:
                        print(f"{Fore.YELLOW}Please enter valid numbers.")
                
                task['duration'] = new_hours * 3600 + new_minutes * 60
                
                # Update remaining time if task is paused
                if "Paused" in task['status'] and 'remaining' in task:
                    task['remaining'] = task['duration']
                
                print(f"{Fore.GREEN}» Duration updated!")
                time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Please enter valid numbers!")
                time.sleep(1)
        
        elif (choice == '4' and "Completed" not in task['status']) or \
             (choice == '3' and "Completed" in task['status']):
            break
    
    backend.save_tasks(tasks)
    print(f"{Fore.GREEN}» Task updated successfully! ✅")
    time.sleep(1)

def hyperfocus_mode(task, current_progress=0):
    """Display task in HyperFocus mode with enhanced visuals"""
    global current_mode
    current_mode = "hyperfocus"
    
    # Define cool nerd emojis for transition
    focus_emojis = ["🧠", "⚡", "🎯", "💡", "🚀", "🔬", "💪", "🎮", "⌨️", "🖥️"]
    emoji_index = 0
    
    clear_screen()
    print(f"\n{Fore.LIGHTMAGENTA_EX}🌟 HYPERFOCUS MODE ACTIVATED 🌟\n")
    print(f"{Fore.LIGHTCYAN_EX}Task: {Fore.LIGHTGREEN_EX}{task['name']}")
    print(f"{Fore.LIGHTCYAN_EX}Description: {Fore.WHITE}{task['description']}\n")
    
    total = task['duration']
    original_duration = total  # Store original duration
    
    # Calculate actual progress for paused tasks
    if 'remaining' in task:
        current_progress = original_duration - task['remaining']
        total = task['remaining']
    
    print(f"{Fore.YELLOW}Commands: [N]otes | [F]astNotes | [B]ack to Normal Mode | [P]ause\n")
    
    try:
        with tqdm(total=original_duration, desc=f"{Fore.LIGHTCYAN_EX}Progress", 
                bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] " + focus_emojis[emoji_index],
                ascii="▰▱") as pbar:
            
            pbar.update(current_progress)
            start_time = time.time() - current_progress
            elapsed_start = time.time()
            spoken_halfway = current_progress >= (original_duration // 2)
            last_emoji_update = time.time()
            
            while pbar.n < original_duration:
                try:
                    # Update emoji every 0.4 seconds instead of 3
                    current_time = time.time()
                    if current_time - last_emoji_update >= 0.1:  # Changed from 0.4 to 0.1
                        emoji_index = (emoji_index + 1) % len(focus_emojis)
                        # Remove the vertical line by using a space before the emoji
                        pbar.bar_format = "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] " + focus_emojis[emoji_index]
                        last_emoji_update = current_time
                    
                    if msvcrt.kbhit():
                        key = msvcrt.getch().lower()
                        if key == b'p':  # Pause
                            remaining = original_duration - pbar.n
                            task['remaining'] = remaining
                            task['status'] = f"{Fore.YELLOW}⏸ Paused"
                            speak("Task paused")
                            return "paused", pbar.n
                        elif key == b'b':  # Back to normal mode
                            return "normal", pbar.n
                        elif key == b'n':  # Notes
                            temp_progress = pbar.n
                            notes_interface(backend)
                            clear_screen()
                            print(f"\n{Fore.LIGHTMAGENTA_EX}🌟 HYPERFOCUS MODE ACTIVATED 🌟\n")
                            print(f"{Fore.LIGHTCYAN_EX}Task: {Fore.LIGHTGREEN_EX}{task['name']}")
                            print(f"{Fore.YELLOW}Commands: [N]otes | [F]astNotes | [B]ack to Normal Mode | [P]ause\n")
                        elif key == b'f':  # FastNotes
                            temp_progress = pbar.n
                            fast_notes_interface(backend)
                            clear_screen()
                            print(f"\n{Fore.LIGHTMAGENTA_EX}🌟 HYPERFOCUS MODE ACTIVATED 🌟\n")
                            print(f"{Fore.LIGHTCYAN_EX}Task: {Fore.LIGHTGREEN_EX}{task['name']}")
                            print(f"{Fore.YELLOW}Commands: [N]otes | [F]astNotes | [B]ack to Normal Mode | [P]ause\n")
                except:
                    pass

                current_time = time.time()
                pbar.n = int(current_time - start_time)
                pbar.last_print_n = pbar.n - 1
                pbar.refresh()
                
                if pbar.n >= original_duration // 2 and not spoken_halfway:
                    print(f"\n{Fore.LIGHTCYAN_EX}🎉 Halfway Completed! 💪")
                    speak("Halfway Completed!")
                    spoken_halfway = True

        task['status'] = f"{Fore.GREEN}Completed ✅"
        print(f"\n{Fore.LIGHTGREEN_EX}✨ Task Completed Successfully! ✨")
        speak("Task Completed Successfully!")
        return "completed", original_duration
            
    except KeyboardInterrupt:
        task['status'] = f"{Fore.RED}Interrupted ⚠️"
        print(f"\n{Fore.RED}Task interrupted!")
        speak("Task interrupted")
        return "interrupted", pbar.n

def normal_task_mode(task, current_progress=0):
    """Original task mode with progress bar"""
    global current_mode
    current_mode = "normal"
    
    clear_screen()
    display_header()
    display_tasks()
    
    total = task['duration']
    original_duration = total  # Store original duration
    task['status'] = f"{Fore.BLUE}In Progress"
    
    # Calculate actual progress for paused tasks
    if 'remaining' in task:
        current_progress = original_duration - task['remaining']
        total = task['remaining']
    
    spoken_halfway = current_progress >= (original_duration // 2)
    
    print(f"\n{Fore.GREEN}🚀 Starting: {task['name']} ({total//3600}h {total%3600//60}m)")
    print(f"{Fore.YELLOW}Press 'N' for Notes, 'F' for FastNotes, 'P' to Pause, 'H' for HyperFocus\n")

    try:
        with tqdm(total=original_duration, desc=f"{Fore.CYAN}Countdown", 
                bar_format="{l_bar}%s{bar}%s| {n_fmt}/{total_fmt}" % (Fore.GREEN, Fore.RESET)) as pbar:
            
            pbar.update(current_progress)
            start_time = time.time() - current_progress
            initial_elapsed = current_progress
            elapsed_start = time.time() - initial_elapsed
            
            while pbar.n < original_duration:
                try:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().lower()
                        if key == b'p':  # Pause
                            remaining = original_duration - pbar.n
                            task['remaining'] = remaining
                            task['status'] = f"{Fore.YELLOW}⏸ Paused"
                            speak("Task paused")
                            return "paused", pbar.n
                        elif key == b'h':  # Switch to HyperFocus
                            return "hyper", pbar.n
                        elif key == b'n':  # Notes
                            temp_progress = pbar.n
                            notes_interface(backend)
                            clear_screen()
                            display_header()
                            display_tasks()
                            print(f"\n{Fore.GREEN}🚀 Resuming: {task['name']}")
                            print(f"{Fore.YELLOW}Press 'N' for Notes, 'F' for FastNotes, 'P' to Pause, 'H' for HyperFocus\n")
                        elif key == b'f':  # FastNotes
                            temp_progress = pbar.n
                            fast_notes_interface(backend)
                            clear_screen()
                            display_header()
                            display_tasks()
                            print(f"\n{Fore.GREEN}🚀 Resuming: {task['name']}")
                            print(f"{Fore.YELLOW}Press 'N' for Notes, 'F' for FastNotes, 'P' to Pause, 'H' for HyperFocus\n")
                except:
                    pass

                current_time = time.time()
                pbar.n = int(current_time - start_time)
                pbar.last_print_n = pbar.n - 1
                pbar.refresh()
                
                # Add halfway completion announcement
                if pbar.n >= original_duration // 2 and not spoken_halfway:
                    print(f"\n{Fore.CYAN}🎉 Halfway Completed! 💪")
                    speak("Halfway Completed!")
                    spoken_halfway = True
                
                elapsed = int(current_time - elapsed_start)
                elapsed_mins, elapsed_secs = divmod(elapsed, 60)
                remaining = original_duration - pbar.n
                mins, secs = divmod(remaining, 60)
                pbar.set_description(f"{Fore.CYAN}Remaining: {mins:02d}:{secs:02d} [{elapsed_mins:02d}:{elapsed_secs:02d}]")
                time.sleep(0.1)

        task['status'] = f"{Fore.GREEN}Completed ✅"
        print(f"\n{Fore.GREEN}✨ Task Completed Successfully! ✨")
        speak("Task Completed Successfully!")
        return "completed", original_duration
            
    except KeyboardInterrupt:
        task['status'] = f"{Fore.RED}Interrupted ⚠️"
        print(f"\n{Fore.RED}Task interrupted!")
        speak("Task interrupted")
        return "interrupted", pbar.n

def pomodoro_mode(task):
    """Dedicated Pomodoro mode with specialized UI and functionality"""
    clear_screen()
    settings = task['pomodoro_settings']
    current_pomodoro = settings['current_pomodoro']
    total_pomodoros = settings['num_pomodoros']
    
    # Initialize start time if not exists
    if 'start_time' not in task:
        task['start_time'] = datetime.now().strftime('%H:%M:%S')
    
    # Initialize pomodoro history if not exists
    if 'pomodoro_history' not in task:
        task['pomodoro_history'] = []
    
    # Initialize pause state if not exists
    if 'paused_state' not in task:
        task['paused_state'] = {
            'phase': 'work',
            'time_left': 0,
            'current_pomodoro': current_pomodoro
        }
    
    def display_pomodoro_header():
        clear_screen()
        print(f"\n{Fore.MAGENTA}🍅 POMODORO MODE 🍅\n")
        print(f"{Fore.CYAN}Task: {Fore.GREEN}{task['name']}")
        print(f"{Fore.CYAN}Description: {Fore.WHITE}{task['description']}")
        print(f"{Fore.CYAN}Started at: {Fore.WHITE}{task['start_time']}\n")
        
        # Display completed Pomodoros history with progress bars
        if task['pomodoro_history']:
            print(f"{Fore.YELLOW}Completed Pomodoros:")
            for i, pomo in enumerate(task['pomodoro_history'], 1):
                print(f"{Fore.WHITE}  #{i}: {pomo['timestamp']} - Work: {pomo['work_duration']}min")
                # Show completed work session bar
                print(f"{Fore.GREEN}  Work Time: 100%|{'▰' * 50}| {settings['work_duration']*60}/{settings['work_duration']*60}")
                # Show completed break bar if it's not the last Pomodoro
                if i < total_pomodoros:
                    print(f"{Fore.BLUE}  Break Time: 100%|{'▰' * 50}| {settings['break_duration']*60}/{settings['break_duration']*60}\n")
        print()
        
        print(f"{Fore.YELLOW}Session Settings:")
        print(f"Work Duration: {settings['work_duration']} minutes")
        print(f"Break Duration: {settings['break_duration']} minutes")
        print(f"Long Break Duration: {settings['long_break_duration']} minutes")
        print(f"Progress: {current_pomodoro}/{total_pomodoros} Pomodoros\n")
        print(f"{Fore.YELLOW}Commands: [P]ause | [Q]uit\n")
    
    def display_current_session(phase, progress_bars):
        """Display current session with history"""
        clear_screen()
        display_pomodoro_header()
        
        # Display completed progress bars
        for bar in progress_bars:
            print(bar)
        
        if phase == 'work':
            print(f"\n{Fore.GREEN}🍅 Starting Pomodoro {current_pomodoro + 1}/{total_pomodoros}")
        elif phase == 'break':
            print(f"\n{Fore.BLUE}☕ Starting Break ({settings['break_duration']} minutes)")
    
    def handle_pause_state():
        """Handle paused state and return whether to continue"""
        while True:
            print(f"\n{Fore.YELLOW}⏸ Pomodoro Paused!")
            print(f"{Fore.CYAN}Commands: [R]esume | [Q]uit to main menu")
            key = msvcrt.getch().lower()
            if key == b'r':  # Resume
                # Store the current progress bars
                progress_bars = []
                if task['pomodoro_history']:
                    for i, pomo in enumerate(task['pomodoro_history'], 1):
                        progress_bars.append(f"{Fore.GREEN}Work Time: 100%|{'▰' * 50}| {settings['work_duration']*60}/{settings['work_duration']*60}")
                        if i < total_pomodoros:
                            progress_bars.append(f"{Fore.BLUE}Break Time: 100%|{'▰' * 50}| {settings['break_duration']*60}/{settings['break_duration']*60}\n")
                
                # Redisplay with clean screen
                display_current_session(task['paused_state']['phase'], progress_bars)
                return True
            elif key == b'q':  # Quit to main menu
                task['status'] = f"{Fore.YELLOW}⏸ Paused"
                return False

    try:
        while current_pomodoro < total_pomodoros:
            display_pomodoro_header()
            
            # Work Session
            print(f"\n{Fore.GREEN}🍅 Starting Pomodoro {current_pomodoro + 1}/{total_pomodoros}")
            work_seconds = settings['work_duration'] * 60
            
            # Resume from pause if applicable
            paused_state = task.get('paused_state', {})
            if paused_state.get('phase') == 'work' and paused_state.get('time_left', 0) > 0:
                work_seconds = paused_state.get('time_left', work_seconds)
                print(f"{Fore.YELLOW}Resuming work session...")
            
            with tqdm(total=settings['work_duration'] * 60, 
                     initial=settings['work_duration'] * 60 - work_seconds,
                     desc=f"{Fore.GREEN}Work Time", 
                     bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                     ascii="▰▱") as pbar:
                
                start_time = time.time()
                end_time = start_time + work_seconds
                
                while time.time() < end_time:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().lower()
                        if key == b'p':  # Pause
                            remaining = end_time - time.time()
                            task['paused_state'] = {
                                'phase': 'work',
                                'time_left': remaining,
                                'current_pomodoro': current_pomodoro
                            }
                            if not handle_pause_state():
                                return "paused"
                            # If we continue, update the end time
                            end_time = time.time() + remaining
                        elif key == b'q':  # Quit
                            task['pomodoro_settings']['current_pomodoro'] = current_pomodoro
                            return "quit"
                    
                    pbar.n = settings['work_duration'] * 60 - int(end_time - time.time())
                    pbar.refresh()
                    time.sleep(0.1)
            
            # After work session completes
            current_pomodoro += 1
            task['pomodoro_settings']['current_pomodoro'] = current_pomodoro
            
            # Record completed Pomodoro
            task['pomodoro_history'].append({
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'work_duration': settings['work_duration']
            })
            
            speak("Work session complete")
            print(f"\n{Fore.GREEN}✨ Work session complete!")
            time.sleep(1)
            
            # Break session
            if current_pomodoro < total_pomodoros:
                break_duration = settings['break_duration']
                break_type = "Break"
            else:
                break_duration = settings['long_break_duration']
                break_type = "Long Break"
            
            print(f"\n{Fore.BLUE}☕ Starting {break_type} ({break_duration} minutes)")
            break_seconds = break_duration * 60
            
            # Reset pause state for break
            task['paused_state'] = {
                'phase': 'break',
                'time_left': break_seconds,
                'current_pomodoro': current_pomodoro
            }
            
            # Check if resuming from break pause
            if task['paused_state'].get('phase') == 'break':
                break_seconds = task['paused_state'].get('time_left', break_seconds)
                if break_seconds != break_duration * 60:
                    print(f"{Fore.YELLOW}Resuming break...")
            
            with tqdm(total=break_duration * 60,
                     initial=break_duration * 60 - break_seconds,
                     desc=f"{Fore.BLUE}{break_type}", 
                     bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                     ascii="▰▱") as pbar:
                
                start_time = time.time()
                end_time = start_time + break_seconds
                
                while time.time() < end_time:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().lower()
                        if key == b'p':  # Pause
                            remaining = end_time - time.time()
                            task['paused_state'] = {
                                'phase': 'break',
                                'time_left': remaining,
                                'current_pomodoro': current_pomodoro
                            }
                            if not handle_pause_state():
                                return "paused"
                            # If we continue, update the end time
                            end_time = time.time() + remaining
                        elif key == b'q':  # Quit
                            task['pomodoro_settings']['current_pomodoro'] = current_pomodoro
                            return "quit"
                    
                    pbar.n = break_duration * 60 - int(end_time - time.time())
                    pbar.refresh()
                    time.sleep(0.1)
            
            # Reset pause state for next work session
            task['paused_state'] = {
                'phase': 'work',
                'time_left': settings['work_duration'] * 60,
                'current_pomodoro': current_pomodoro
            }
            
            speak("Break complete")
            print(f"\n{Fore.GREEN}✨ Break complete!")
            time.sleep(1)
        
        # All Pomodoros completed
        task['status'] = f"{Fore.GREEN}Completed ✅"
        task['end_time'] = datetime.now().strftime('%H:%M:%S')
        task['paused_state'] = None  # Clear pause state when completed
        print(f"\n{Fore.GREEN}🎉 All Pomodoros completed successfully!")
        speak("All Pomodoros completed successfully")
        return "completed"
            
    except KeyboardInterrupt:
        task['status'] = f"{Fore.RED}Interrupted ⚠️"
        print(f"\n{Fore.RED}Pomodoro interrupted!")
        speak("Pomodoro interrupted")
        return "interrupted"

def start_task(task_index):
    """Enhanced start_task function with HyperFocus mode support"""
    global current_progress, current_mode
    
    try:
        task = tasks[task_index-1]
    except IndexError:
        print(f"{Fore.RED}Invalid task number!")
        return

    if "Completed" in task['status']:
        print(f"{Fore.YELLOW}This task is already completed! 🎉")
        return

    # Initialize current_progress based on whether it's a resumed task
    if 'remaining' in task:
        current_progress = task['duration'] - task['remaining']
    else:
        current_progress = 0

    if task['mode'] == 'pomodoro':
        status = pomodoro_mode(task)
        backend.save_tasks(tasks)
        return

    # Ask for mode selection
    print(f"\n{Fore.CYAN}Select Mode:")
    print(f"{Fore.YELLOW}1. Normal Mode")
    print(f"{Fore.MAGENTA}2. HyperFocus Mode")
    mode = input(f"\n{Fore.GREEN}Choose mode (1/2): ").strip()

    while True:  # Continue running until task is completed or interrupted
        if mode == "2":
            status, progress = hyperfocus_mode(task, current_progress)
        else:
            status, progress = normal_task_mode(task, current_progress)
        
        # Update current_progress based on the returned progress
        current_progress = progress
        
        # Handle different status returns
        if status == "completed" or status == "interrupted" or status == "paused":
            # Reset current_progress after task completion/interruption
            current_progress = 0
            # Clear the remaining time if task is completed
            if status == "completed" and 'remaining' in task:
                del task['remaining']
            break
        elif status == "normal":
            mode = "1"  # Switch to normal mode
            # Update remaining time based on current progress
            task['remaining'] = task['duration'] - current_progress
            continue
        elif status == "hyper":
            mode = "2"  # Switch to hyperfocus mode
            # Update remaining time based on current progress
            task['remaining'] = task['duration'] - current_progress
            continue

def resume_task():
    """Prompts user for task number and resumes the paused task"""
    paused_tasks = [(i, task) for i, task in enumerate(tasks, 1) if "Paused" in task['status']]
    
    if not paused_tasks:
        print(f"{Fore.YELLOW}No paused tasks to resume!")
        return
    
    print(f"\n{Fore.CYAN}Paused tasks:")
    for i, task in paused_tasks:
        remaining_mins = task.get('remaining', 0) // 60
        remaining_secs = task.get('remaining', 0) % 60
        print(f"{Fore.MAGENTA}{i}. {task['name']} ({remaining_mins:02d}:{remaining_secs:02d} remaining)")
    
    try:
        task_num = int(input(f"\n{Fore.CYAN}Enter task number to resume: "))
        start_task(task_num)
    except (ValueError, IndexError):
        print(f"{Fore.RED}Invalid task number!")


def delete_task(cmd):
    """Deletes a task based on user input (e.g., d1, d2)."""
    if len(tasks) == 0:
        print(f"{Fore.RED}No tasks to delete!")
        return
    
    try:
        task_index = int(cmd[1:]) - 1  # Extract number from command (e.g., d2 → 2-1 = index 1)
        
        if task_index < 0 or task_index >= len(tasks):
            print(f"{Fore.RED}Invalid task number!")
            return
        
        deleted_task = tasks.pop(task_index)
        print(f"{Fore.GREEN}✅ Task '{deleted_task['name']}' deleted successfully!")

    except ValueError:
        print(f"{Fore.RED}Invalid format! Use 'dX' (e.g., d1, d2) to delete a task.")
        

def edit_content(content):
    """Open system editor to modify content"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix=".txt", delete=False, encoding='utf-8') as tf:
        tf.write(content)
        temp_name = tf.name

    # Open editor based on OS
    if os.name == 'nt':
        os.system(f'notepad.exe "{temp_name}"')
    else:
        editor = os.environ.get('EDITOR', 'vi')
        subprocess.call([editor, temp_name])

    # Read edited content
    with open(temp_name, 'r', encoding='utf-8') as f:
        new_content = f.read().strip()

    os.remove(temp_name)
    return new_content

def format_note_content(note_text):
    """Format note content with colored first line and indented body"""
    lines = note_text.split('\n')
    if not lines:
        return ""
    
    # First line in magenta, rest in white with indentation
    formatted = f"{Fore.MAGENTA}{lines[0]}{Style.RESET_ALL}"
    if len(lines) > 1:
        body = '\n'.join(f"    {line}" for line in lines[1:])
        formatted += f"\n{Fore.WHITE}{body}"
    
    return formatted
    
def notes_interface(backend):
    """Main interface for the notes system with persistence"""
    while True:
        display_header("NOTES")
        
        if notes:
            print(f"{Fore.BLUE}📒 Note Modules:")
            for i, module in enumerate(notes.keys(), 1):
                note_count = len(notes[module])
                print(f"{Fore.MAGENTA}{i}. {module} ({note_count} notes)")
        else:
            print(f"{Fore.YELLOW}No note modules! Add some first.")
        print()
        
        print(f"{Fore.CYAN}Commands: {Fore.YELLOW}[A]dd Module  [O]pen Module  [D]elete Module  [B]ack")
        cmd = input(f"{Fore.MAGENTA}» ").strip().lower()
        
        if cmd == 'a':
            module_name = input(f"{Fore.CYAN}Enter module name (e.g., Work, Personal): ")
            if module_name not in notes:
                notes[module_name] = []
                print(f"{Fore.GREEN}» Module '{module_name}' created! ✅")
                backend.save_notes({"modules": notes})
            else:
                print(f"{Fore.RED}Module already exists!")
        
        elif cmd == 'o':
            if not notes:
                print(f"{Fore.RED}No modules to open!")
                continue
                
            print(f"{Fore.CYAN}Enter module number:")
            try:
                module_num = int(input(f"{Fore.MAGENTA}» ")) - 1
                module_name = list(notes.keys())[module_num]
                module_interface(backend, module_name)
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid module number!")
        
        elif cmd == 'd':
            if not notes:
                print(f"{Fore.RED}No modules to delete!")
                continue
                
            print(f"{Fore.CYAN}Enter module number to delete:")
            try:
                module_num = int(input(f"{Fore.MAGENTA}» ")) - 1
                module_name = list(notes.keys())[module_num]
                del notes[module_name]
                print(f"{Fore.GREEN}» Module '{module_name}' deleted! ✅")
                backend.save_notes({"modules": notes})
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid module number!")
        
        elif cmd == 'b':
            break
        
        time.sleep(1)

def module_interface(backend, module_name):
    """Interface for interacting with a specific module"""
    while True:
        display_header(f"{module_name} MODULE")
        
        if notes[module_name]:
            print(f"{Fore.BLUE}📃 Notes:")
            for i, note in enumerate(notes[module_name], 1):
                print(f"{Fore.CYAN}{i}. {format_note_content(note)}")
                if i < len(notes[module_name]):  # Add separator between notes
                    print(f"{Fore.BLUE}   {'─' * 40}")
        else:
            print(f"{Fore.YELLOW}No notes in this module.")
        print()
        
        print(f"{Fore.CYAN}Commands: {Fore.YELLOW}[A]dd Note  [E]dit Note  [D]elete Note  [B]ack")
        cmd = input(f"{Fore.MAGENTA}» ").strip().lower()
        
        if cmd == 'a':
            # Open notepad for new note
            initial_content = "Write your note here and Ctrl+S to save it and close Notepad..."
            note_text = edit_content(initial_content)
            if note_text and note_text != "Write your note here...":
                notes[module_name].append(note_text)
                print(f"{Fore.GREEN}» Note added! ✅")
                backend.save_notes({"modules": notes})
            else:
                print(f"{Fore.YELLOW}Note was empty or unchanged. Not saving.")
        
        elif cmd == 'e':
            if not notes[module_name]:
                print(f"{Fore.RED}No notes to edit!")
                continue
            
            try:
                note_num = int(input(f"{Fore.CYAN}Enter note number to edit: ")) - 1
                if 0 <= note_num < len(notes[module_name]):
                    # Open existing note in notepad
                    edited_content = edit_content(notes[module_name][note_num])
                    if edited_content:
                        notes[module_name][note_num] = edited_content
                        print(f"{Fore.GREEN}» Note updated! ✅")
                        backend.save_notes({"modules": notes})
                    else:
                        print(f"{Fore.YELLOW}Note was empty. Not updating.")
                else:
                    print(f"{Fore.RED}Invalid note number!")
            except ValueError:
                print(f"{Fore.RED}Invalid note number!")
        
        elif cmd == 'd':
            if not notes[module_name]:
                print(f"{Fore.RED}No notes to delete!")
                continue
            
            print(f"{Fore.CYAN}Enter note number to delete:")
            try:
                note_num = int(input(f"{Fore.MAGENTA}» ")) - 1
                del notes[module_name][note_num]
                print(f"{Fore.GREEN}» Note deleted! ✅")
                backend.save_notes({"modules": notes})
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid note number!")
        
        elif cmd == 'b':
            break
        
        time.sleep(1)

def fast_notes_interface(backend):
    """Interface for quick notes management"""
    while True:
        display_header("FAST NOTES")
        
        if quick_notes:
            print(f"{Fore.BLUE}📝 Quick Notes:")
            for i, note in enumerate(quick_notes, 1):
                print(f"{Fore.CYAN}{i}. {format_note_content(note)}")
                if i < len(quick_notes):  # Add separator between notes
                    print(f"{Fore.BLUE}   {'─' * 40}")
        else:
            print(f"{Fore.YELLOW}No quick notes available.")
        print()
        
        print(f"{Fore.CYAN}Commands: {Fore.YELLOW}[A]dd Note  [E]dit Note  [D]elete Note  [B]ack")
        cmd = input(f"{Fore.MAGENTA}» ").strip().lower()
        
        if cmd == 'a':
            # Open notepad for new note
            initial_content = "Write your quick note here..."
            note_text = edit_content(initial_content)
            if note_text and note_text != "Write your quick note here...":
                quick_notes.append(note_text)
                print(f"{Fore.GREEN}» Quick note added! ✅")
                backend.save_fastnotes(quick_notes)
            else:
                print(f"{Fore.YELLOW}Note was empty or unchanged. Not saving.")
        
        elif cmd == 'e':
            if not quick_notes:
                print(f"{Fore.RED}No quick notes to edit!")
                continue
            
            try:
                note_num = int(input(f"{Fore.CYAN}Enter note number to edit: ")) - 1
                if 0 <= note_num < len(quick_notes):
                    # Open existing note in notepad
                    edited_content = edit_content(quick_notes[note_num])
                    if edited_content:
                        quick_notes[note_num] = edited_content
                        print(f"{Fore.GREEN}» Quick note updated! ✅")
                        backend.save_fastnotes(quick_notes)
                    else:
                        print(f"{Fore.YELLOW}Note was empty. Not updating.")
                else:
                    print(f"{Fore.RED}Invalid note number!")
            except ValueError:
                print(f"{Fore.RED}Invalid note number!")
        
        elif cmd == 'd':
            if not quick_notes:
                print(f"{Fore.RED}No quick notes to delete!")
                continue
            
            print(f"{Fore.CYAN}Enter note number to delete:")
            try:
                note_num = int(input(f"{Fore.MAGENTA}» ")) - 1
                del quick_notes[note_num]
                print(f"{Fore.GREEN}» Quick note deleted! ✅")
                backend.save_fastnotes(quick_notes)
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid note number!")
        
        elif cmd == 'b':
            break
        
        time.sleep(1)

def generate_daily_report(date_str=None):
    """Generate a detailed daily report with charts and statistics"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Load tasks for the specified date
    historical_data = backend.load_tasks(date_str)
    if not historical_data:
        print(f"{Fore.YELLOW}No tasks found for {date_str}")
        return None

    tasks_list = historical_data.get('tasks', [])
    if not tasks_list:
        print(f"{Fore.YELLOW}No tasks found for {date_str}")
        return None

    # Calculate statistics
    total_time = 0
    completed_time = 0
    longest_session = 0
    longest_task_name = ""
    completed_tasks = 0
    pending_tasks = 0
    paused_tasks = 0

    task_details = []
    
    for task in tasks_list:
        duration = task['duration']
        status = task['status'].replace(Fore.GREEN, '').replace(Fore.YELLOW, '').replace(Fore.BLUE, '')
        
        task_details.append({
            'name': task['name'],
            'duration': duration,
            'status': status,
            'description': task['description']
        })

        total_time += duration
        
        if "Completed" in status:
            completed_time += duration
            completed_tasks += 1
            # Check if this was the longest session
            if duration > longest_session:
                longest_session = duration
                longest_task_name = task['name']
        elif "Paused" in status:
            paused_tasks += 1
        else:
            pending_tasks += 1

    # Generate report content
    report = [
        f"📊 TASKMAN DAILY REPORT - {date_str} 📊",
        "=" * 50,
        "\n📈 SUMMARY STATISTICS",
        "-" * 20,
        f"Total Time Allocated: {total_time//3600}h {(total_time%3600)//60}m",
        f"Time Spent on Completed Tasks: {completed_time//3600}h {(completed_time%3600)//60}m",
        f"Longest Single Session: {longest_session//3600}h {(longest_session%3600)//60}m ({longest_task_name})",
        f"Completion Rate: {(completed_tasks/len(tasks_list))*100:.1f}%",
        f"\nTask Status Distribution:",
        f"✅ Completed: {completed_tasks}",
        f"⏸ Paused: {paused_tasks}",
        f"⏳ Pending: {pending_tasks}",
        "\n📋 DETAILED TASK BREAKDOWN",
        "-" * 20
    ]

    # Add individual task details
    for idx, task in enumerate(task_details, 1):
        duration = task['duration']
        report.extend([
            f"\nTask {idx}: {task['name']}",
            f"Description: {task['description']}",
            f"Duration: {duration//3600}h {(duration%3600)//60}m",
            f"Status: {task['status']}"
        ])

    return report

def display_report(report):
    """Display the report with colored formatting"""
    clear_screen()
    
    # Print header
    print(f"\n{Fore.CYAN}{report[0]}")
    print(f"{Fore.CYAN}{report[1]}\n")
    
    # Print statistics section
    print(f"{Fore.GREEN}{report[2]}")
    print(f"{Fore.GREEN}{report[3]}")
    
    # Print summary stats with colors
    for line in report[4:8]:
        print(f"{Fore.YELLOW}{line}")
    
    # Print status distribution
    print(f"\n{Fore.YELLOW}{report[8]}")
    print(f"{Fore.GREEN}{report[9]}")  # Completed
    print(f"{Fore.YELLOW}{report[10]}")  # Paused
    print(f"{Fore.RED}{report[11]}")  # Pending
    
    # Print detailed breakdown
    print(f"\n{Fore.GREEN}{report[12]}")
    print(f"{Fore.GREEN}{report[13]}")
    
    # Print task details
    for i in range(14, len(report)):
        if report[i].startswith('\nTask'):
            print(f"\n{Fore.CYAN}{report[i]}")
        else:
            print(f"{Fore.WHITE}{report[i]}")

def export_report(report, date_str=None):
    """Export the report to a text file"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(backend.data_dir, "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    filename = os.path.join(reports_dir, f"taskman_report_{date_str}.txt")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for line in report:
                f.write(line + '\n')
        return filename
    except Exception as e:
        print(f"{Fore.RED}Error exporting report: {str(e)}")
        return None

def report_interface():
    """Interface for viewing and exporting reports"""
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}📊 TASKMAN REPORTS 📊\n")
        print(f"{Fore.YELLOW}1. View Today's Report")
        print(f"{Fore.YELLOW}2. View Report for Specific Date")
        print(f"{Fore.YELLOW}3. Export Report")
        print(f"{Fore.YELLOW}4. Back to Main Menu")
        
        choice = input(f"\n{Fore.GREEN}Choice (1-4): ").strip()
        
        if choice == '1':
            report = generate_daily_report()
            if report:
                display_report(report)
                input(f"\n{Fore.CYAN}Press Enter to continue...")
        
        elif choice == '2':
            date_str = input(f"{Fore.CYAN}Enter date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                report = generate_daily_report(date_str)
                if report:
                    display_report(report)
                    input(f"\n{Fore.CYAN}Press Enter to continue...")
            except ValueError:
                print(f"{Fore.RED}Invalid date format!")
                time.sleep(1)
        
        elif choice == '3':
            date_str = input(f"{Fore.CYAN}Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date_str:
                date_str = datetime.now().strftime('%Y-%m-%d')
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                report = generate_daily_report(date_str)
                if report:
                    filename = export_report(report, date_str)
                    if filename:
                        print(f"{Fore.GREEN}Report exported to: {filename}")
                        time.sleep(2)
            except ValueError:
                print(f"{Fore.RED}Invalid date format!")
                time.sleep(1)
        
        elif choice == '4':
            break
        
        else:
            print(f"{Fore.RED}Invalid choice!")
            time.sleep(1)

def view_task_details(task):
    """Display details for a single task"""
    clear_screen()
    print(f"\n{Fore.CYAN}Task Details:\n")
    print(f"{Fore.CYAN}Task: {Fore.GREEN}{task['name']}")
    print(f"{Fore.CYAN}Description: {Fore.WHITE}{task['description']}")
    print(f"{Fore.CYAN}Status: {task['status']}")
    print(f"{Fore.CYAN}Started at: {Fore.WHITE}{task.get('start_time', 'Not started')}")
    
    if task['status'] == f"{Fore.GREEN}Completed ✅":
        print(f"{Fore.CYAN}Ended at: {Fore.WHITE}{task.get('end_time', 'N/A')}")
    
    if task['mode'] == 'pomodoro':
        settings = task['pomodoro_settings']
        completed = settings.get('current_pomodoro', 0)
        total = settings.get('num_pomodoros', 0)
        print(f"\n{Fore.YELLOW}Pomodoro Details:")
        print(f"Progress: {completed}/{total} Pomodoros")
        print(f"Work Duration: {settings['work_duration']} minutes")
        print(f"Break Duration: {settings['break_duration']} minutes")
        print(f"Long Break Duration: {settings['long_break_duration']} minutes")
        
        if task.get('pomodoro_history'):
            print(f"\n{Fore.YELLOW}Session History:")
            for i, pomo in enumerate(task['pomodoro_history'], 1):
                print(f"  #{i}: {pomo['timestamp']} - Work: {pomo['work_duration']}min")
    else:
        hrs = task['duration'] // 3600
        mins = (task['duration'] % 3600) // 60
        print(f"\n{Fore.YELLOW}Duration: {hrs}h {mins}m")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...")

def view_tasks():
    """Interface for viewing task details"""
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}📋 TASK DETAILS 📋\n")
        
        # Display all tasks with numbers
        for i, task in enumerate(tasks, 1):
            badge = f"{Fore.RED}[🛠️]" if task['mode'] == 'custom' else f"{Fore.MAGENTA}[🍅 POMO]"
            status = task['status'] if isinstance(task['status'], str) else "Pending"
            print(f"{badge} {i}. {task['name']} - {status}")
        
        print(f"\n{Fore.YELLOW}Enter task number to view details (or 'b' to go back)")
        choice = input(f"{Fore.GREEN}Choice: ").strip().lower()
        
        if choice == 'b':
            break
        
        try:
            task_num = int(choice)
            if 1 <= task_num <= len(tasks):
                view_task_details(tasks[task_num-1])
            else:
                print(f"{Fore.RED}Invalid task number!")
                time.sleep(1)
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
            time.sleep(1)

def main_interface():
    """Main interface with flexible command input handling"""
    global backend  # Add this line to make backend global
    session_count = 0  # Track number of completed sessions
    last_auto_save = datetime.now().date()
    
    try:
        # Initialize backend and authenticate
        backend = setup_backend()
        if not backend:
            print(f"{Fore.RED}Authentication failed!")
            return

        # Load existing tasks for today
        today = date.today().isoformat()
        task_data = backend.load_tasks(today)
        if task_data:
            global tasks
            tasks = task_data["tasks"]

        # Show loading animation only once at startup
        loading_animation()
        
        while True:
            # Check if we need to auto-save the report
            current_date = datetime.now().date()
            
            # Auto-save report if date changed
            if current_date != last_auto_save:
                report = generate_daily_report(last_auto_save.isoformat())
                if report:
                    backend.save_report(report, last_auto_save.isoformat())
                last_auto_save = current_date
                session_count = 0  # Reset session count for new day
            
            # Auto-save report after every 5 sessions
            if session_count >= 5:
                report = generate_daily_report()
                if report:
                    backend.save_report(report)
                session_count = 0  # Reset session counter
            
            display_header()
            display_tasks()
            
            print(f"{Fore.CYAN}Commands: {Fore.YELLOW}[A]dd  [L]ist  [S]tartX  [P]auseX/Resume  [E]ditX  [D]eleteX  [V]iewX  [N]otes  [F]astNotes  [H]istory  [R]eports  [Q]uit")
            
            try:
                cmd = input(f"{Fore.MAGENTA}» ").strip().lower()
                
                # Handle view command with optional task number
                if cmd.startswith('v'):
                    task_num = None
                    # Check if command includes a task number (e.g., "v2")
                    if len(cmd) > 1 and cmd[1:].isdigit():
                        task_num = int(cmd[1:])
                        if 1 <= task_num <= len(tasks):
                            view_task_details(tasks[task_num-1])
                            continue
                        else:
                            print(f"{Fore.RED}Invalid task number!")
                            time.sleep(1)
                            continue
                    view_tasks()
                    backend.save_tasks(tasks)
                
                elif cmd == 'a':
                    add_task()
                    backend.save_tasks(tasks)
                
                elif cmd == 'l':
                    continue  # List is always visible
                
                elif cmd.startswith('s'):
                    try:
                        # Try to get number from command
                        num = int(cmd[1:])
                    except ValueError:
                        # If no number in command, ask for it
                        try:
                            num = int(input(f"{Fore.CYAN}Enter task number: "))
                        except ValueError:
                            print(f"{Fore.YELLOW}Please enter a valid task number.")
                            time.sleep(1)
                            continue
                    start_task(num)
                    backend.save_tasks(tasks)
                
                elif cmd.startswith('d'):
                    try:
                        # Try to get number from command
                        num = int(cmd[1:])
                    except ValueError:
                        # If no number in command, ask for it
                        try:
                            num = int(input(f"{Fore.CYAN}Enter task number to delete: "))
                        except ValueError:
                            print(f"{Fore.YELLOW}Please enter a valid task number.")
                            time.sleep(1)
                            continue
                    delete_task(num)
                    backend.save_tasks(tasks)
                
                elif cmd.startswith('e'):
                    try:
                        # Try to get number from command
                        num = int(cmd[1:])
                    except ValueError:
                        # If no number in command, ask for it
                        try:
                            num = int(input(f"{Fore.CYAN}Enter task number to edit: "))
                        except ValueError:
                            print(f"{Fore.YELLOW}Please enter a valid task number.")
                            time.sleep(1)
                            continue
                    edit_task(num)
                
                elif cmd == 'p':
                    resume_task()
                    backend.save_tasks(tasks)
                
                elif cmd == 'n':
                    notes_interface(backend)
                
                elif cmd == 'f':
                    fast_notes_interface(backend)
                
                elif cmd == 'h':
                    # New history viewing feature
                    date_input = input(f"{Fore.CYAN}Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                    if not date_input:
                        date_input = today
                    try:
                        # Validate date format
                        datetime.strptime(date_input, '%Y-%m-%d')
                        historical_data = backend.load_tasks(date_input)
                        if historical_data:
                            print(f"\n{Fore.GREEN}Tasks for {date_input}:")
                            for i, task in enumerate(historical_data['tasks'], 1):
                                hrs = task['duration'] // 3600
                                mins = (task['duration'] % 3600) // 60
                                print(f"{Fore.MAGENTA}{i}. {task['name']} [{hrs}h {mins}m] - {task['status']}")
                        else:
                            print(f"{Fore.YELLOW}No tasks found for {date_input}")
                        input(f"\n{Fore.CYAN}Press Enter to continue...")
                    except ValueError:
                        print(f"{Fore.RED}Invalid date format! Use YYYY-MM-DD")
                        time.sleep(1)
                
                elif cmd == 'r':
                    report_interface()
                
                elif cmd == 'q':
                    # Save final state before quitting
                    backend.save_tasks(tasks)
                    clear_screen()
                    print(f"\n{Fore.BLUE}🚪 Goodbye! Keep being awesome! 💪\n")
                    break
                
                else:
                    print(f"{Fore.YELLOW}Unknown command. See options above")
                    time.sleep(1)
                    
                # Update session count when a task is completed
                if cmd.startswith('s'):
                    session_count += 1

            except KeyboardInterrupt:
                # Save final report before exiting
                report = generate_daily_report()
                if report:
                    backend.save_report(report)
                backend.save_tasks(tasks)
                clear_screen()
                print(f"\n{Fore.BLUE}🚪 Goodbye! Keep being awesome! 💪\n")
                break
            
            except Exception as e:
                print(f"{Fore.RED}An error occurred: {str(e)}")
                time.sleep(1)
                continue

    except Exception as e:
        print(f"{Fore.RED}Critical error: {str(e)}")
        print(f"{Fore.YELLOW}Please try restarting TASKMAN")

if __name__ == "__main__":
    main_interface()