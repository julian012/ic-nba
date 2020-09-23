# configureCWD.py - Sets current working directory relative to where program folder is located

import os


# Sets current working directory relative to where program folder is located
def set_current_working_directory(directory_name):
    program_directory = os.path.dirname(os.path.abspath(__file__))
    new_current_working_directory = os.path.join(program_directory, directory_name)
    os.chdir(new_current_working_directory)