import gspread
from google.oauth2.service_account import Credentials

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
    
    print('_' * 80 + '\n')

    print('Main menu:\n\n- Show Tasks\n- New Task\n- Complete Task\n- Exit')

    print('_' * 80 + '\n')

    action = input("What would you like to do:\n")
    print(f"You selected '{action}'.")


display_menu()