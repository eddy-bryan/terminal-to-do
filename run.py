import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import sys

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
    Displays a menu of actions the user can select from.
    """
    print('Welcome to Terminal To Do!')

    while True:
        print('_' * 80 + '\n')
        print('Main menu:')
        for option in MENU_OPTIONS:
            print(f'- {option}')
        print('_' * 80 + '\n')
        action = input("What would you like to do:\n").capitalize()

        if action in MENU_OPTIONS:
            print(f"\nYou selected '{action}'.")
            MENU_OPTIONS[action]()
        else:
            print('\nAction invalid, please select an option from the "Main menu".')


def show_tasks(page):
    """
    Displays a list of tasks to the terminal from the specified worksheet.
    """
    try:
        worksheet = SHEET.worksheet(page)
        all_values = worksheet.get_all_values()
        
        if not all_values:
            print(f"No tasks found in the '{page}' worksheet.")
            return

        task_data = [row[:3] for row in all_values[1:]]

        for task in task_data:
            print('_' * 80 + '\n')
            print(f"Task Name: {task[0]}\n")
            print(f"Description: {task[1]}\n")
            print(f"Due Date: {task[2]}")
    except ValueError as e:
        print(f"Error: {e}")


def is_valid_date(date_str):
    """
    Checks the format of the date input by the user and checks that the
    date provided is not in the past tense.
    """
    try:
        parsed_date = datetime.strptime(date_str, '%d-%m-%Y')

        if parsed_date.date() < date.today():
            raise ValueError("Due date cannot be in the past.")

        return True
    except ValueError:
        return False


def new_task():
    """
    This function prompts the user to input task details, validates the input,
    and appends a new task to the 'Tasks' worksheet.
    """
    tasks_worksheet = SHEET.worksheet('tasks')

    while True:
        task_name = input("\nEnter the task name (or enter 'cancel' to cancel):\n")

        if task_name.lower() == 'cancel':
            print("Task creation canceled.")
            return
        elif not task_name:
            print("Error: Task name cannot be empty.")
            continue

        all_values = tasks_worksheet.get_all_values()
        task_exists = False

        for row in all_values[1:]:
            if row[0].lower() == task_name.lower():
                task_exists = True
                break

        if task_exists:
            print("Task with the same name already exists.")
            continue

        break

    while True:
        try:
            task_description = input("\nEnter the task description (or enter 'cancel' to cancel):\n")

            if task_description.lower() == 'cancel':
                print("Task creation canceled.")
                return
            elif not task_description:
                raise ValueError("Task description cannot be empty.")

            break

        except ValueError as e:
            print(f"Error: {e}")

    while True:
        try:
            due_date = input("\nEnter the due date (format: DD-MM-YYYY) (or enter 'cancel' to cancel):\n")

            if due_date.lower() == 'cancel':
                print("Task creation canceled.")
                return
            if not is_valid_date(due_date):
                raise ValueError("Invalid date provided. Dates should not be in the past and should be provided in format: DD-MM-YYYY.")

            break

        except ValueError as e:
            print(f"Error: {e}")

    tasks_worksheet = SHEET.worksheet('tasks')

    print("\nUpdating tasks worksheet...")

    tasks_worksheet.append_row([task_name, task_description, due_date])

    print("New task added successfully!")


def get_task_details(worksheet, task_name):
    """
    This function searches for a task with the provided name in the given worksheet.
    If the task is found, its details are returned. If the task is not found, the user
    is prompted to enter a valid task name or cancel the action.
    """
    while True:
        try:
            all_values = worksheet.get_all_values()

            task_details = None

            for row in all_values[1:]:
                if row[0].lower() == task_name.lower():
                    task_details = row
                    break

            if task_details is not None:
                return task_details
            else:
                raise ValueError("\nTask not found. Please enter a valid task name (or enter 'cancel' to cancel):")

        except ValueError as e:
            print(f"Error: {e}")

            if task_name.lower() == 'cancel':
                print("Action canceled.")
                return None


def complete_task():
    """
    This function displays the list of tasks from the 'tasks' worksheet and prompts the user
    to enter the name of the task they want to mark as complete. If the task is found, it is moved
    to the 'completed_tasks' worksheet, and the original entry is deleted from the 'tasks' worksheet.
    """
    try:
        tasks_worksheet = SHEET.worksheet('tasks')
        completed_tasks_worksheet = SHEET.worksheet('completed_tasks')

        while True:
            show_tasks('tasks')

            all_values = tasks_worksheet.get_all_values()

            print('_' * 80 + '\n')
            task_name = input("Enter the name of the task you would like to mark as complete (or enter 'cancel' to cancel):\n")

            if task_name.lower() == 'cancel':
                print("Task completion canceled.")
                return

            task_found = False

            for i in range(1, len(all_values)):
                if all_values[i][0].lower() == task_name.lower():
                    task_found = True
                    row_to_delete = i + 1
                    break

            if task_found:
                print("\nUpdating completed tasks worksheet...")
                completed_tasks_worksheet.append_row(all_values[row_to_delete-1])
                print("Completed tasks worksheet updated successfully.")

                print("Updating tasks worksheet...")
                tasks_worksheet.delete_rows(row_to_delete)
                print("Tasks worksheet updated successfully.")

                print(f"\nTask '{task_name}' marked as complete and moved to completed tasks.")
                break
            else:
                print("\nTask not found. Please enter a valid task name (or enter 'cancel' to cancel):\n")
    
    except ValueError as e:
        print(f"Error: {e}")


def delete_task():
    """
    This function prompts the user to select whether they want to delete a task from the 'tasks'
    or 'completed_tasks' worksheet. It then displays the list of tasks from the selected worksheet
    and prompts the user to enter the name of the task they want to delete. If the task is found,
    it is deleted from the worksheet.
    """
    try:
        while True:
            selection = input("Would you like to delete from the 'Tasks' or 'Completed Tasks' list (or enter 'cancel' to cancel):\n")

            if selection.lower() == 'cancel':
                print("Task deletion canceled.")
                return
            elif selection.lower() == 'tasks':
                worksheet = SHEET.worksheet('tasks')
                break
            elif selection.lower() == 'completed tasks':
                worksheet = SHEET.worksheet('completed_tasks')
                break
            else:
                print("Selection invalid, please choose either the 'Tasks' or 'Completed Tasks' list (or enter 'cancel' to cancel):\n")

        while True:
            show_tasks(selection.lower().replace(" ", "_"))

            all_values = worksheet.get_all_values()

            print('_' * 80 + '\n')
            task_name = input("Enter the name of the task you would like to delete (or enter 'cancel' to cancel):\n")

            if task_name.lower() == 'cancel':
                print("Task deletion canceled.")
                return

            task_found = False

            for i in range(1, len(all_values)):
                if all_values[i][0].lower() == task_name.lower():
                    task_found = True
                    row_to_delete = i + 1
                    break

            if task_found:
                print(f"\nUpdating {worksheet.title.capitalize()} worksheet...")
                worksheet.delete_rows(row_to_delete)
                print(f"{worksheet.title.capitalize()} worksheet updated successfully.")

                print(f"\nTask '{task_name}' has been deleted.")
                break
            else:
                print("\nTask not found. Please enter a valid task name (or enter 'cancel' to cancel):\n")
    
    except ValueError as e:
        print(f"Error: {e}")


def exit_program():
    print("\nExiting program...")
    sys.exit()


MENU_OPTIONS = {
    'Show tasks': lambda: show_tasks('tasks'),
    'New task': new_task,
    'Complete task': complete_task,
    'Delete task': delete_task,
    'Exit': exit_program
}


display_menu()