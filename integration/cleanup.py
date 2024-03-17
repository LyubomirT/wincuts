import getpass
from pathlib import Path
import os

user = getpass.getuser()

def remove_from_startup(name=""):
    if name == "":
        raise ValueError("The file name cannot be empty.")
    
    # The path to the Startup folder
    startup_path = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    
    # Check if the .bat file exists in the Startup folder
    file_path = startup_path / name
    if file_path.exists():
        os.remove(file_path)
        print(f"Deleted {name} from Startup.")
    else:
        print(f"{name} not found in Startup.")

with open("del.ini", "r") as file:
    exe_name = file.readline().strip()
    remove_from_startup("integrated_wincuts.bat")
