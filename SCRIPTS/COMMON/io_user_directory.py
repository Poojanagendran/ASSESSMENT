# This is the local user directory, should be ignored while pushing to git repo
from pathlib import Path
path = str(Path(__file__).parents[2])
input_common_dir = path + r'\PythonWorkingScripts_InputData'
output_common_dir = path + r'\PythonWorkingScripts_Output'
chrome_driver_dir = path
