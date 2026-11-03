### CLI Task Manager

import json
from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent

TASKS_FILE = SCRIPT_DIRECTORY / "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
            return tasks
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        sys.exit('File "tasks.json" could not be read')


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent = 2)

def print_main_menu():
    try:
        print('''
===== TASK MANAGER =====
===== Main Menu =====

1. View Tasks
2. Exit
        ''')
        return int(input("Please select an option: "))
    except ValueError:
        return None

def print_tasks(tasks):
    if not tasks:
        print("No tasks found")
    else:
        for index, task in enumerate(tasks, start = 1):
            print(f"{index}. {task["description"]}: {task["completed"]}")

def print_tasks_menu(tasks):
    try:
        print('''
===== TASK MANAGER =====
===== Tasks Menu =====

Tasks:''')
        print_tasks(tasks)
        print('''
1. Add Task
2. Complete Task
3. Delete Task
4. View Completed Tasks
5. Return to Main Menu
        ''')
        return int(input("Please select an option: "))
    except ValueError:
        return None

def print_completed_tasks(tasks):
    print('''
===== TASK MANAGER =====
===== Completed Tasks =====
''')
    found_completed = False
    for index, task in enumerate(tasks, start = 1):
        if task["completed"]:
            found_completed = True
            print(f'''{index}. {task["description"]}: {task["completed"]}''')
    if not found_completed:
        print('''You have no completed tasks''')
    print('''
1. Return to Task Menu
''')


def add_task(tasks):
    input_new_task = input('''
Add a new task: ''').strip()
    if input_new_task:
        new_task = {"description": input_new_task,
                    "completed": False}
        tasks.append(new_task)
        save_tasks(tasks)
        print(f'''
Task "{input_new_task}" added successfully!''')
    else:
        print("Please enter a new task")


def complete_task(tasks):
    selected_task_index = select_task(tasks, "complete")
    if selected_task_index is not None:
        if tasks[selected_task_index]["completed"]:
            print('''
This task has already been marked complete''')
        else:
            tasks[selected_task_index]["completed"] = True
            save_tasks(tasks)
            print(f'''
Task "{tasks[selected_task_index]["description"]}" is now marked complete!''')


def delete_task(tasks):
    selected_task_index = select_task(tasks, "delete")
    if selected_task_index is not None:
        print(f'''
Task "{tasks[selected_task_index]["description"]}" has been deleted''')
        del tasks[selected_task_index]
        save_tasks(tasks)

def select_task(tasks, action):
    try:
        if tasks:
            selected_task_number = int(input(f'''
Please select a task to {action}: '''))
            if not 1 <= selected_task_number <= len(tasks):
                print('''
The selected task does not exist''')
                return None
            else:
                return selected_task_number - 1
        else:
            print(f'''
You have no tasks to {action}''')
            return None
    except ValueError:
        print('''
Please select a valid option''')
        return None

def main():
    tasks = load_tasks()

    while True:
        main_menu_selected_option = print_main_menu()
        if main_menu_selected_option == 1:
            while True:
                tasks_menu_selected_option = print_tasks_menu(tasks)
                
                if tasks_menu_selected_option == 5:
                    break
                
                elif tasks_menu_selected_option == 1:
                    add_task(tasks)
                
                elif tasks_menu_selected_option == 2:
                    complete_task(tasks)

                elif tasks_menu_selected_option == 3:
                    delete_task(tasks)
                
                elif tasks_menu_selected_option == 4:
                    while True:
                        try:
                            print_completed_tasks(tasks)
                            if int(input('''Please select an option: ''')) == 1:
                                break
                            else:
                                print('''
Please select a valid option''')
                        except ValueError:
                            print('''
Please select a valid option''')

                        
                elif tasks_menu_selected_option is None or not 1 <= tasks_menu_selected_option <= 5:
                    print('''
Please select a valid option''')
        elif main_menu_selected_option == 2:
            print('''
Goodbye!
    ''')
            break
        else:
            print('''
Please select a valid option''')

if __name__ == "__main__":
    main()

