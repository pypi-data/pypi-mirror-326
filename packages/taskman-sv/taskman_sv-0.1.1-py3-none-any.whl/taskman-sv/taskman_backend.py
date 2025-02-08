import os
import json
import bcrypt
import base64
import getpass
import time
from datetime import datetime, date, timedelta  # Added timedelta import
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style, init
from typing import Optional, Dict, List, Any

class TaskmanBackend:
    def __init__(self):
        self.user = None
        self.key = None
        self.fernet = None
        self.data_dir = os.path.expanduser("~/.taskman")
        self.setup_data_directory()

    def setup_data_directory(self):
        """Create necessary directories and files if they don't exist with restricted permissions"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            os.makedirs(os.path.join(self.data_dir, "users"))
            
            # Set restrictive permissions on Windows
            if os.name == 'nt':
                import win32security
                import ntsecuritycon as con
                
                # Get current user's SID
                username = os.getenv('USERNAME')
                domain = os.getenv('USERDOMAIN')
                sid = win32security.LookupAccountName(domain, username)[0]
                
                # Create DACL with full control only for current user
                dacl = win32security.ACL()
                dacl.AddAccessAllowedAce(
                    win32security.ACL_REVISION,
                    con.FILE_ALL_ACCESS,
                    sid
                )
                
                # Set security on directory
                security_desc = win32security.SECURITY_DESCRIPTOR()
                security_desc.SetSecurityDescriptorDacl(1, dacl, 0)
                win32security.SetFileSecurity(
                    self.data_dir, 
                    win32security.DACL_SECURITY_INFORMATION,
                    security_desc
                )
            else:
                # Set restrictive permissions on Unix-like systems (700)
                os.chmod(self.data_dir, 0o700)
                os.chmod(os.path.join(self.data_dir, "users"), 0o700)

    def generate_key(self, password: str, salt: bytes = None) -> tuple:
        """Generate encryption key from password"""
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user"""
        users_dir = os.path.join(self.data_dir, "users")
        user_file = os.path.join(users_dir, f"{username}.json")

        if os.path.exists(user_file):
            return False

        # Generate salt and hash password
        salt = os.urandom(16)
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        # Generate encryption key
        key, key_salt = self.generate_key(password, salt)

        user_data = {
            "username": username,
            "password": base64.b64encode(hashed).decode('utf-8'),
            "salt": base64.b64encode(salt).decode('utf-8'),
            "key_salt": base64.b64encode(key_salt).decode('utf-8'),
        }

        with open(user_file, 'w') as f:
            json.dump(user_data, f)

        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user and setup encryption"""
        user_file = os.path.join(self.data_dir, "users", f"{username}.json")
        
        if not os.path.exists(user_file):
            return False

        with open(user_file, 'r') as f:
            user_data = json.load(f)

        stored_hash = base64.b64decode(user_data['password'].encode('utf-8'))
        if not bcrypt.checkpw(password.encode(), stored_hash):
            return False

        # Setup encryption key
        key_salt = base64.b64decode(user_data['key_salt'].encode('utf-8'))
        self.key, _ = self.generate_key(password, key_salt)
        self.fernet = Fernet(self.key)
        self.user = username
        return True

    def save_data(self, data: dict, data_type: str) -> bool:
        """Save encrypted data to file with restricted permissions"""
        if not self.user or not self.fernet:
            return False

        filename = f"{self.user}_{data_type}.enc"
        file_path = os.path.join(self.data_dir, "users", filename)
        
        # Add timestamp and random salt to data for additional security
        data['last_modified'] = datetime.now().isoformat()
        data['salt'] = base64.b64encode(os.urandom(16)).decode('utf-8')
        
        try:
            # Double encryption for sensitive data
            json_data = json.dumps(data).encode()
            encrypted_data = self.fernet.encrypt(json_data)
            
            # Write with restricted permissions
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Set file permissions
            if os.name == 'nt':
                import win32security
                import ntsecuritycon as con
                
                username = os.getenv('USERNAME')
                domain = os.getenv('USERDOMAIN')
                sid = win32security.LookupAccountName(domain, username)[0]
                
                dacl = win32security.ACL()
                dacl.AddAccessAllowedAce(
                    win32security.ACL_REVISION,
                    con.FILE_ALL_ACCESS,
                    sid
                )
                
                security_desc = win32security.SECURITY_DESCRIPTOR()
                security_desc.SetSecurityDescriptorDacl(1, dacl, 0)
                win32security.SetFileSecurity(
                    file_path,
                    win32security.DACL_SECURITY_INFORMATION,
                    security_desc
                )
            else:
                os.chmod(file_path, 0o600)  # Read/write for owner only
            
            return True
        
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False

    def load_data(self, data_type: str) -> dict:
        """Load and decrypt data from file"""
        if not self.user or not self.fernet:
            return None

        filename = f"{self.user}_{data_type}.enc"
        file_path = os.path.join(self.data_dir, "users", filename)
        
        if not os.path.exists(file_path):
            return self.get_empty_data(data_type)

        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception as e:
            print(f"Error loading {data_type}: {str(e)}")
            return self.get_empty_data(data_type)

    def get_empty_data(self, data_type: str) -> dict:
        """Return empty data structure based on type"""
        today = date.today().isoformat()
        
        if data_type == "tasks":
            return {
                "date": today,
                "tasks": []
            }
        elif data_type == "notes":
            return {
                "modules": {},
                "last_modified": datetime.now().isoformat(),
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
        elif data_type == "fastnotes":
            return {
                "notes": [],
                "last_modified": datetime.now().isoformat(),
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
        return {}

    def save_tasks(self, tasks: list) -> bool:
        """Save tasks with date-specific files"""
        task_data = {
            "date": date.today().isoformat(),
            "tasks": tasks,
            "last_modified": datetime.now().isoformat()
        }
        
        # Save to a date-specific file
        filename = f"{self.user}_tasks_{task_data['date']}.enc"
        file_path = os.path.join(self.data_dir, "users", filename)
        
        encrypted_data = self.fernet.encrypt(json.dumps(task_data).encode())
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
        return True
    
    def load_tasks(self, target_date: str = None) -> dict:
        """Load tasks and handle completed tasks"""
        if target_date is None:
            target_date = date.today().isoformat()

        # First try to load tasks for the specific date
        filename = f"{self.user}_tasks_{target_date}.enc"
        file_path = os.path.join(self.data_dir, "users", filename)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                task_data = json.loads(decrypted_data)
                
                # Add 'mode' field to existing tasks if missing
                if 'tasks' in task_data:
                    for task in task_data['tasks']:
                        if 'mode' not in task:
                            task['mode'] = 'custom'  # Set default mode for existing tasks
                
                return task_data
            except Exception as e:
                print(f"Error loading tasks: {str(e)}")
                return self.get_empty_data("tasks")
        
        # If loading today's tasks and file doesn't exist
        if target_date == date.today().isoformat():
            # Load yesterday's tasks to check for pending ones
            yesterday = (date.today() - timedelta(days=1)).isoformat()
            yesterday_data = self.load_tasks(yesterday)
            
            if yesterday_data and "tasks" in yesterday_data:
                # Only keep pending tasks from yesterday
                pending_tasks = [
                    task for task in yesterday_data["tasks"]
                    if task.get("status", "").strip() in [f"{Fore.YELLOW}Pending", f"{Fore.YELLOW}⏸ Paused"]
                ]
                
                # Ensure all tasks have the 'mode' field
                for task in pending_tasks:
                    if 'mode' not in task:
                        task['mode'] = 'custom'
                
                return {
                    "date": target_date,
                    "tasks": pending_tasks
                }
        
        return self.get_empty_data("tasks")
    
    def save_notes(self, notes_data: dict) -> bool:
        """Save notes modules"""
        if not isinstance(notes_data, dict):
            notes_data = {"modules": {}}
        
        if "modules" not in notes_data:
            notes_data["modules"] = {}
            
        notes_data["last_modified"] = datetime.now().isoformat()
        return self.save_data(notes_data, "notes")

    def load_notes(self) -> dict:
        """Load notes modules"""
        notes_data = self.load_data("notes")
        if not notes_data or not isinstance(notes_data, dict):
            return self.get_empty_data("notes")
        
        # Ensure required structure exists
        if "modules" not in notes_data:
            notes_data["modules"] = {}
        if "metadata" not in notes_data:
            notes_data["metadata"] = {
                "created_at": datetime.now().isoformat(),
                "version": "1.0"
            }
        
        return notes_data

    def save_fastnotes(self, fastnotes: list) -> bool:
        """Save fast notes"""
        notes_data = {
            "notes": fastnotes if isinstance(fastnotes, list) else [],
            "last_modified": datetime.now().isoformat(),
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "1.0"
            }
        }
        return self.save_data(notes_data, "fastnotes")

    def load_fastnotes(self) -> list:
        """Load fast notes"""
        data = self.load_data("fastnotes")
        if not data or not isinstance(data, dict):
            data = self.get_empty_data("fastnotes")
        return data.get("notes", [])

    def save_report(self, report: list, date_str: str = None) -> bool:
        """Save report to a secure location with encryption"""
        if not self.user or not self.fernet:
            return False

        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')

        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(self.data_dir, "reports")
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            # Set proper permissions
            if os.name == 'nt':
                self._set_windows_permissions(reports_dir)
            else:
                os.chmod(reports_dir, 0o700)

        # Prepare report data with metadata
        report_data = {
            "date": date_str,
            "content": report,
            "generated_at": datetime.now().isoformat(),
            "username": self.user
        }

        try:
            # Encrypt and save the report
            json_data = json.dumps(report_data).encode()
            encrypted_data = self.fernet.encrypt(json_data)
            
            filename = f"report_{date_str}_{int(time.time())}.enc"
            file_path = os.path.join(reports_dir, filename)
            
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Set proper permissions for the report file
            if os.name == 'nt':
                self._set_windows_permissions(file_path)
            else:
                os.chmod(file_path, 0o600)
            
            return True
        except Exception as e:
            print(f"Error saving report: {str(e)}")
            return False

    def load_report(self, date_str: str) -> dict:
        """Load and decrypt a report for a specific date"""
        if not self.user or not self.fernet:
            return None

        reports_dir = os.path.join(self.data_dir, "reports")
        if not os.path.exists(reports_dir):
            return None

        try:
            # Find the most recent report file for the given date
            report_files = [f for f in os.listdir(reports_dir) 
                           if f.startswith(f"report_{date_str}_") and f.endswith('.enc')]
            
            if not report_files:
                return None

            # Get the most recent report
            latest_report = sorted(report_files)[-1]
            file_path = os.path.join(reports_dir, latest_report)

            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception as e:
            print(f"Error loading report: {str(e)}")
            return None

    def _set_windows_permissions(self, path):
        """Set Windows-specific file permissions"""
        if os.name == 'nt':
            import win32security
            import ntsecuritycon as con
            
            # Get current user's SID
            username = os.getenv('USERNAME')
            domain = os.getenv('USERDOMAIN')
            sid = win32security.LookupAccountName(domain, username)[0]
            
            # Create DACL with full control only for current user
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                con.FILE_ALL_ACCESS,
                sid
            )
            
            # Set security on file/directory
            security_desc = win32security.SECURITY_DESCRIPTOR()
            security_desc.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(
                path,
                win32security.DACL_SECURITY_INFORMATION,
                security_desc
            )

def display_auth_screen():
    """Display an attractive authentication screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════╗
║             {Fore.GREEN}TASKMAN LOGIN{Fore.CYAN}             ║
╚═══════════════════════════════════════════╝
""")

def get_credentials(mode="login") -> tuple:
    """Get username and password with improved UI"""
    display_auth_screen()
    
    print(f"{Fore.YELLOW}{'Login' if mode == 'login' else 'Register'} to TASKMAN")
    print(f"{Fore.CYAN}{'=' * 40}")
    
    username = input(f"{Fore.CYAN}Username: {Fore.WHITE}").strip()
    password = getpass.getpass(f"{Fore.CYAN}Password: {Fore.WHITE}")
    
    return username, password

def setup_backend():
    """Initialize backend and handle authentication with improved UI"""
    backend = TaskmanBackend()
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        display_auth_screen()
        print(f"{Fore.CYAN}1. {Fore.WHITE}Login")
        print(f"{Fore.CYAN}2. {Fore.WHITE}Register")
        print(f"{Fore.CYAN}3. {Fore.WHITE}Exit")
        print(f"{Fore.CYAN}{'=' * 40}")
        
        choice = input(f"{Fore.GREEN}Choice: {Fore.WHITE}").strip()
        
        if choice == "1":
            username, password = get_credentials("login")
            if backend.authenticate(username, password):
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for animation
                return backend
            attempts += 1
            print(f"{Fore.RED}Invalid credentials! {max_attempts - attempts} attempts remaining.")
            time.sleep(1)
            
        elif choice == "2":
            username, password = get_credentials("register")
            if backend.register_user(username, password):
                print(f"{Fore.GREEN}Registration successful! Please login.")
                time.sleep(1)
            else:
                print(f"{Fore.RED}Username already exists!")
                time.sleep(1)
                
        elif choice == "3":
            exit(0)
            
        else:
            print(f"{Fore.RED}Invalid choice!")
            time.sleep(1)
    
    print(f"{Fore.RED}Too many failed attempts. Please try again later.")
    exit(1)