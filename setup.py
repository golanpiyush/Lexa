import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need to be included manually
build_exe_options = {
    "packages": ["os", "psutil", "time", "shutil", "requests", "subprocess", "webbrowser", "threading", "platform"],
    "excludes": [],
    "include_files": ["helpers"]  # Include additional files or directories here
}

# Define MSI specific options
bdist_msi_options = {
    "add_to_path": True,  # Add the application to the system PATH
    "upgrade_code": "{12345678-1234-1234-1234-123456789012}",  # Unique identifier for your application
}

base = None
if sys.platform == "win32":
    base = "Console"  # Use "Console" for CLI-based scripts

setup(
    name="LexaMovieCLI",
    version="0.1",
    description="CLI-based movie torrent streaming application",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[Executable("main.py", base=base)],
)
