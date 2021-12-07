import sys
import subprocess
import pkg_resources

required = {'pygame'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Installing required libraries...")
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing])
    print("All required libraries are now installed.")
else:
    print("All required libraries are already installed.")