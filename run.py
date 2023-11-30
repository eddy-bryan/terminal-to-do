import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import sys
from colorama import Fore, Style


# Google Sheets API autheentication setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("terminal_to_do")


def show_tasks(page):
    """
    Displays a list of tasks to the terminal from the specified worksheet.
    """
    try:
        # Get the worksheet
        worksheet = SHEET.worksheet(page)

        # Retrieve all values from the worksheet
        all_values = worksheet.get_all_values()

        # Check if there are tasks
        if not all_values:
            print(f"{Fore.RED}No tasks found in the '{page}' worksheet."
                  f"{Style.RESET_ALL}")
            return

        # Extract task data (excluding header)
        task_data = [row[:3] for row in all_values[1:]]

        # Display task information
        for task in task_data:
            print('_' * 80 + '\n')
            print(f"Task Name: {task[0]}\n")
            print(f"Description: {task[1]}\n")
            print(f"Due Date: {task[2]}")
    except ValueError as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")


def is_valid_date(date_str):
    """
    Checks the format of the date input by the user and checks that the
    date provided is not in the past tense.
    """
    try:
        # Parse the date string
        parsed_date = datetime.strptime(date_str, '%d-%m-%Y')

        # Check if the date is in the past
        if parsed_date.date() < date.today():
            raise ValueError(f"{Fore.RED}Due date cannot be in the past."
                             f"{Style.RESET_ALL}")

        return True
    except ValueError:
        return False


def new_task():
    """
    This function prompts the user to input task details, validates the input,
    and appends a new task to the 'Tasks' worksheet.
    """
    tasks_worksheet = SHEET.worksheet("tasks")

    while True:
        # Get the task name from the user
        task_name = input("\nEnter the task name (or enter 'cancel' to cancel)"
                          ":\n")

        # Check if the user wants to cancel task creation
        if task_name.lower() == "cancel":
            print("Task creation canceled.")
            return
        elif not task_name or task_name.isspace():
            print(f"\n{Fore.RED}Error: Task name cannot be empty."
                  f"{Style.RESET_ALL}")
            continue

        # Check a task with the same name already exists
        all_values = tasks_worksheet.get_all_values()
        task_exists = False

        for row in all_values[1:]:
            if row[0].lower() == task_name.lower():
                task_exists = True
                break

        if task_exists:
            print(f"\n{Fore.RED}Task with the same name already exists."
                  f"{Style.RESET_ALL}")
            continue

        break

    while True:
        try:
            # Get task description from the user
            task_description = input("\nEnter the task description (or enter "
                                     "'cancel' to cancel):\n")

            # Check if the user wants to cancel task creation
            if task_description.lower() == "cancel":
                print("Task creation canceled.")
                return
            elif not task_description or task_description.isspace():
                raise ValueError(f"{Fore.RED}Task description cannot be empty."
                                 f"{Style.RESET_ALL}")

            break

        except ValueError as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")

    while True:
        try:
            # Get the due date from the user
            due_date = input("\nEnter the due date (format: DD-MM-YYYY) (or "
                             "enter 'cancel' to cancel):\n")

            # Check if the user wants to cancel task creation
            if due_date.lower() == "cancel":
                print("Task creation canceled.")
                return
            if not is_valid_date(due_date):
                raise ValueError(f"{Fore.RED}Invalid date provided. Dates "
                                 f"should not be in the past and should be "
                                 f"provided in format: DD-MM-YYYY."
                                 f"{Style.RESET_ALL}")

            break

        except ValueError as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")

    print("\nUpdating tasks worksheet...")

    tasks_worksheet.append_row([task_name, task_description, due_date])

    print("New task added successfully!")


def get_task_details(worksheet, task_name):
    """
    This function searches for a task with the provided name in the given
    worksheet. If the task is found, its details are returned. If the task
    is not found, the user is prompted to enter a valid task name or cancel
    the action.
    """
    while True:
        try:
            # Get all values from the worksheet
            all_values = worksheet.get_all_values()

            # Initialize task details
            task_details = None

            # Search for the task in the worksheet
            for row in all_values[1:]:
                if row[0].lower() == task_name.lower():
                    task_details = row
                    break

            # Return task details if found
            if task_details is not None:
                return task_details
            else:
                raise ValueError(f"{Fore.RED}Task not found. Please enter a "
                                 f"valid task name (or enter 'cancel' to "
                                 f"cancel):{Style.RESET_ALL}")

        except ValueError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

            # Check if the action is canceled
            if task_name.lower() == "cancel":
                print("Action canceled.")
                return None


def complete_task():
    """
    This function displays the list of tasks from the 'tasks' worksheet and
    prompts the user to enter the name of the task they want to mark as
    complete. If the task is found, it is moved to the 'completed_tasks'
    worksheet, and the original entry is deleted from the 'tasks' worksheet.
    """
    try:
        # Get the 'tasks' and 'completed_tasks' worksheets
        tasks_worksheet = SHEET.worksheet("tasks")
        completed_tasks_worksheet = SHEET.worksheet("completed_tasks")

        while True:
            # Show the list of tasks in the 'tasks' worksheet
            show_tasks("tasks")

            # Get all values from the 'tasks' worksheet
            all_values = tasks_worksheet.get_all_values()

            print("_" * 80 + "\n")
            # Get the name of the task to mark as complete from the user
            task_name = input("Enter the name of the task you would like to "
                              "mark as complete (or enter 'cancel' to cancel)"
                              ":\n")

            # Check if the task completion is canceled
            if task_name.lower() == "cancel":
                print("Task completion canceled.")
                return

            task_found = False

            # Find the task in the 'tasks' worksheet
            for i in range(1, len(all_values)):
                if all_values[i][0].lower() == task_name.lower():
                    task_found = True
                    row_to_delete = i + 1
                    break

            if task_found:
                print("\nUpdating completed tasks worksheet...")
                # Append the task to the 'completed_tasks' worksheet
                completed_tasks_worksheet.append_row(all_values
                                                     [row_to_delete-1])
                print("Completed tasks worksheet updated successfully.")

                print("Updating tasks worksheet...")
                # Delete the task from the 'tasks' worksheet
                tasks_worksheet.delete_rows(row_to_delete)
                print("Tasks worksheet updated successfully.")

                print(f"\nTask '{task_name}' marked as complete and moved to "
                      f"completed tasks.")
                break
            else:
                print(f"{Fore.RED}\nTask not found. Please enter a valid task "
                      f"name.{Style.RESET_ALL}")

    except ValueError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def delete_task():
    """
    This function prompts the user to select whether they want to delete a
    task from the 'tasks' or 'completed_tasks' worksheet. It then displays
    the list of tasks from the selected worksheet and prompts the user to
    enter the name of the task they want to delete. If the task is found, it
    is deleted from the worksheet.
    """
    while True:
        print("\nAvailable worksheets:\n")
        print("1. Tasks")
        print("2. Completed Tasks")
        try:
            selection = input("\nSelect a worksheet number that you would "
                              "like to delete from (or enter 'cancel' to "
                              "cancel):\n")

            if selection == '1':
                worksheet = SHEET.worksheet("tasks")
                page = "tasks"
                print("You selected 'Tasks'.")
                break
            elif selection == '2':
                worksheet = SHEET.worksheet("completed_tasks")
                page = "completed_tasks"
                print("You selected 'Completed Tasks'.")
                break
            elif selection.lower() == "cancel":
                print("Task deletion canceled.")
                return
            else:
                raise ValueError(f"{Fore.RED}Selection invalid, please "
                                 f"choose a valid worksheet number."
                                 f"{Style.RESET_ALL}")
        except ValueError as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")

    while True:
        show_tasks(page)
        all_values = worksheet.get_all_values()

        print("_" * 80 + "\n")
        # Get the task name to delete from the user
        task_name = input("Enter the name of the task you would like to "
                          "delete (or enter 'cancel' to cancel):\n")

        # Check if the user wants to cancel task deletion
        if task_name.lower() == "cancel":
            print("Task deletion canceled.")
            return

        task_found = False

        # Find the task in the worksheet
        for i in range(1, len(all_values)):
            if all_values[i][0].lower() == task_name.lower():
                task_found = True
                row_to_delete = i + 1
                break

        if task_found:
            print(f"\nUpdating {worksheet.title.capitalize()} "
                  f"worksheet...")
            # Delete the task from the worksheet
            worksheet.delete_rows(row_to_delete)
            print(f"{worksheet.title.capitalize()} worksheet updated "
                  f"successfully.")

            print(f"\nTask '{task_name}' has been deleted.")
            break
        else:
            print(f"\n{Fore.RED}Task not found. Please enter a valid task "
                  f"name."
                  f"{Style.RESET_ALL}")


def exit_program():
    """
    Simple function to terminate the program
    """
    print("\nExiting program...")
    sys.exit()


# Dictionary of menu options and corresponding functions
MENU_OPTIONS = [
    ("Show tasks", lambda: show_tasks("tasks")),
    ("New task", new_task),
    ("Complete task", complete_task),
    ("Delete task", delete_task),
    ("Exit", exit_program)
]


def display_menu():
    """
    Displays a menu of actions the user can select from.
    """
    print("Welcome to Terminal To Do!")

    while True:
        # Display the menu options
        print("_" * 80 + "\n")
        print("Main menu:")

        # Enumerate through MENU_OPTIONS and display each option
        for i, (option, _) in enumerate(MENU_OPTIONS, start=1):
            print(f"{i}. {option}")
        print("_" * 80 + "\n")

        try:
            # Get user input for action selection
            action_num = int(input("Select the number of the action you would "
                                   "like to perform:\n"))

            # Check if the entered action number is valid
            if 1 <= action_num <= len(MENU_OPTIONS):
                # Execute the selected action
                action = MENU_OPTIONS[action_num - 1][1]
                print(f"\nYou selected '{MENU_OPTIONS[action_num - 1][0]}'.")
                action()
            else:
                print(f"{Fore.RED}\nInvalid action number. Please select a "
                      f"number from the menu.{Style.RESET_ALL}")

        except ValueError:
            print(f"{Fore.RED}\nInvalid input. Please enter a number."
                  f"{Style.RESET_ALL}")


# Main execution
display_menu()
