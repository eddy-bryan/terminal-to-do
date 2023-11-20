import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('terminal_to_do')


def display_menu():
    """
    Displays a menu of actions the user can select from
    """
    print('Welcome to Terminal To Do!')

    while True:
        print('_' * 80 + '\n')
        print('Main menu:\n\n- Show Tasks\n- New Task\n- Complete Task\n- Exit')
        print('_' * 80 + '\n')
        action = input("What would you like to do:\n").capitalize()

        if action == 'Show tasks':
            print(f"\nYou selected '{action}'.")
            show_tasks()
        elif action == 'New task':
            print(f"\nYou selected '{action}'.")
            new_task()
        elif action == 'Complete task':
            print(f"\nYou selected '{action}'.")
            # complete_task()
        elif action == 'Exit':
            print("\nExiting program...")
            break
        else:
            print('\nAction invalid, please select an option from the "Main menu".')
            print('_' * 80 + '\n')
            print('Main menu:\n\n- Show Tasks\n- New Task\n- Complete Task\n- Exit')


def show_tasks():
    tasks_worksheet = SHEET.worksheet('tasks')
    all_values = tasks_worksheet.get_all_values()
    task_data = [row[:3] for row in all_values[1:]]

    for task in task_data:
        print('_' * 80 + '\n')
        print(f"Task Name: {task[0]}\n")
        print(f"Description: {task[1]}\n")
        print(f"Due Date: {task[2]}")


def is_valid_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, '%d-%m-%Y')

        if parsed_date.date() < date.today():
            raise ValueError("Due date cannot be in the past.")

        return True
    except ValueError:
        return False


def new_task():
    while True:
        try:
            task_name = input("\nEnter the task name:\n")

            if not task_name:
                raise ValueError("Task name cannot be empty.")

            break

        except ValueError as e:
            print(f"Error: {e}")

    while True:
        try:
            task_description = input("\nEnter the task description:\n")

            if not task_description:
                raise ValueError("Task description cannot be empty.")

            break

        except ValueError as e:
            print(f"Error: {e}")

    while True:
        try:
            due_date = input("\nEnter the due date (format: DD-MM-YYYY):\n")

            if not is_valid_date(due_date):
                raise ValueError("Invalid date provided. Dates should not be in the past and should be provided in format: DD-MM-YYYY.")

            break

        except ValueError as e:
            print(f"Error: {e}")

    tasks_worksheet = SHEET.worksheet('tasks')

    print("\nUpdating tasks worksheet...")

    tasks_worksheet.append_row([task_name, task_description, due_date])

    print("New task added successfully!")


# def complete_task():


display_menu()