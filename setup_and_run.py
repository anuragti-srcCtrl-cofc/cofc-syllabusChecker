import os
import subprocess
import sys

def install_python_and_dependencies():
    # Check for Python installation
    try:
        subprocess.check_call([sys.executable, '--version'])
    except subprocess.CalledProcessError:
        print("Python not found. Installing Python...")
        # Handle Python installation based on the OS
        if os.name == 'nt':  # Windows
            subprocess.check_call(['powershell', '-Command', 'Start-Process', 'choco', 'install', 'python', '-y'])
        elif sys.platform == 'darwin':  # macOS
            subprocess.check_call(['brew', 'install', 'python'])
        elif os.name == 'posix':  # Linux
            subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'python3'])
        else:
            raise EnvironmentError("Unsupported OS")

    # Install dependencies
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pypdf', 'python-docx', 'tk'])

def run_main_script():
    # Path to the main script
    main_script = 'SyllabusCheckerv2.py'
    subprocess.check_call([sys.executable, main_script])

if __name__ == "__main__":
    install_python_and_dependencies()
    run_main_script()
