import pandas as pd
import numpy as np
from datetime import datetime
import shlex


def help_message():
    print("""
Commands:
  add "description"            - Add a new task
  update <id> "new desc"       - Update task description
  delete <id>                  - Delete a task
  list                         - List all tasks
  list done|todo|in-progress   - Filter by status
  mark-done <id>               - Mark a task as done
  mark-in-progress <id>        - Mark a task as in-progress
  exit                         - Exit the program
""")
    

warning_color = '\033[91m' # the color the warning messages will be (currently red)
commands_color = '\033[93m' # the color the user input and printed results will be in (currently yellow)
program_color = '\033[92m' # the color that 'task-cli' will be printed in (currently green)

try:
    tasks = pd.read_json('tasks.json')
    tasks = tasks.dropna(how='all')
except (ValueError, FileNotFoundError):
    tasks = pd.DataFrame(columns=['id', 'description', 'status', 'createdAt', 'updatedAt'])
    tasks.to_json('tasks.json')
    help_message()

def save():
    tasks.to_json('tasks.json')

def add(desc):
    desc = desc.strip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks.loc[len(tasks)] = [int(tasks['id'].max() + 1) if not tasks.empty else 0, desc, 'todo', now, now]
    save()

def update(id, desc):
    id = int(id)
    desc = desc.strip()
    if not tasks[tasks['id'] == id].empty:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tasks.loc[tasks['id'] == id, 'updatedAt'] = now
        tasks.loc[tasks['id'] == id, 'description'] = desc
        save()
    else:
        print(f'{warning_color}Task was not found')

def delete(id):
    id = int(id)
    global tasks
    if not tasks[tasks['id'] == id].empty:
        tasks = tasks[tasks['id'] != id]
        save()
    else:
        print(f'{warning_color}Task was not found')
    
def list_done():
    print(tasks[tasks['status'] == 'done'].to_string(index=False))

def list_not_done():
    print(tasks[tasks['status'] == 'todo'].to_string(index=False))

def list_in_progress():
    print(tasks[tasks['status'] == 'in-progress'].to_string(index=False))

def list(arg=None):
    if arg is None:
        print(tasks.to_string(index=False))
    else:
        if arg == 'done':
            list_done()
        elif arg == 'todo':
            list_not_done()
        elif arg == 'in-progress':
            list_in_progress()
        else:
            print(f'{warning_color}Invalid argument')

def mark_in_progress(id):
    id = int(id)
    if not tasks[tasks['id'] == id].empty:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tasks.loc[tasks['id'] == id, 'updatedAt'] = now
        tasks.loc[tasks['id'] == id, 'status'] = 'in-progress'
        save()
    else:
        print(f'{warning_color}Task was not found')

def mark_done(id):
    id = int(id)
    if not tasks[tasks['id'] == id].empty:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tasks.loc[tasks['id'] == id, 'updatedAt'] = now
        tasks.loc[tasks['id'] == id, 'status'] = 'done'
        save()
    else:
        print(f'{warning_color}Task was not found')


func_map = {
    'add': add,
    'update': update,
    'delete': delete,
    'list': list,
    'mark-done': mark_done,
    'mark-in-progress': mark_in_progress,
    "help": help_message
}

def run_command(first_arg, second_arg = None, third_arg = None):
    if first_arg not in func_map:
        print(f"{warning_color}Unknown command: {first_arg}. Type 'help' to see available commands.")
        return
    try:
        if third_arg is not None:
            func_map[first_arg](second_arg, third_arg)
        elif second_arg is not None:
            func_map[first_arg](second_arg)
        else:
            func_map[first_arg]()
    except Exception as e:
        print(f'{warning_color}Error running command: {e}')
    

while True:
    usr_input = input(f'{program_color}task-cli {commands_color}')

    if usr_input == '':
        help_message()
        continue

    if usr_input == 'exit':
        print(f'{warning_color}Closing...\033[0m') # resets the terminal colors upon exiting the program
        break

    usr_input = shlex.split(usr_input)

    if len(usr_input) == 0:
        continue
    elif len(usr_input) > 3:
        print(f'{warning_color}Too many arguments.')
    elif len(usr_input) == 3:
        run_command(usr_input[0], usr_input[1], usr_input[2])
    elif len(usr_input) == 2:
        run_command(usr_input[0], usr_input[1])
    else:
        run_command(usr_input[0])
    
    continue

    