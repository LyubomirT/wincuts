import getpass
from pathlib import Path

user = getpass.getuser()

def add_to_startup(file_name="", name=""):
    if file_name == "":
        raise ValueError("The file name cannot be empty.")
    
    # The path to the Startup folder
    startup_path = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    
    # The path to the directory where this script is located
    script_path = Path(__file__).resolve().parent.parent
    print (f"Script path: {script_path}")
    print(f"Script path original: {Path(__file__).resolve()}")
    
    # The path to the 'main.exe' assuming it's in the parent directory of this script
    parent_dir_path = script_path.parent
    file_path = parent_dir_path / file_name
    
    print(f"File path: {file_path}",
          f"\nStartup path: {startup_path}")
    
    with open(startup_path / name, "w") as bat_file:
        bat_file.write(f'@echo off\nstart "" "{file_path}" -litr')

with open("init.ini", "r") as file:
    exe_name = file.readline().strip()
    add_to_startup(exe_name, "integrated_wincuts.bat")
