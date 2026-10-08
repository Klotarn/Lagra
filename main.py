import msvcrt
import modules.local_crud as crud
from time import sleep

data = {"users": []}

current_user = None


def welcome():
    print("Welcome to Lagra (TM)")
    print("""
    l) Log in
    q) Quit
    """)

    options = {
        "l": login,
        "q": quit,
    }

    key = get_pressed_key(["l", "q"])

    if key in options:
        options[key]()


def login():
    global current_user
    username = input("Enter username: ")
    password = input("Enter password: ")

    print()

    if not any(
        user["username"] == username and user["password"] == password
        for user in data["users"]
    ):
        return login_failed()
    else:
        current_user = username
        return True


def clear():
    print("\033[2J\033[H", end="")


def login_failed():
    clear()
    global current_user
    print("Invalid username or password.")
    current_user = None

    print("""
    r) Try again
    q) Quit
    """)

    options = {
        "r": login,
        "q": quit,
    }

    key = get_pressed_key(["r", "q"])

    if key in options:
        return options[key]()

    return False


def logout():
    global current_user
    current_user = None
    clear()
    print("Logged out.\n")


def quit():
    print("Quitting...")
    exit()


def welcome_user():
    clear()
    print(f"Welcome, {current_user}!\n")
    list_items()


def select_user_action():
    print("Select an action:")
    print("""
    a) Add item
    r) Remove item
    l) List items
    q) Log out
    """)

    options = {
        "a": add_item,
        "r": remove_item,
        "l": list_items,
        "q": logout,
    }

    key = get_pressed_key(["a", "r", "l", "q"])

    if key in options:
        options[key]()


def add_item():
    clear()
    if current_user == None:
        print("No user is currently logged in.")
        return

    item = input("Enter the item to add (leave empty to not add any item): ").strip()
    print()

    clear()
    if item == "":
        print("No item added.\n")
        return

    # Get user dict where username matches current_user
    user_dict = next(
        (user for user in data["users"] if user["username"] == current_user), None
    )

    if user_dict != None:
        user_dict["items"].append(item)
        crud.write_save_file(data)
        print(f"Item '{item}' added.\n")
    else:
        print("User not found.\n")


def remove_item():
    clear()
    if current_user == None:
        print("No user is currently logged in.\n")
        return

    # Get user dict where username matches current_user
    user_dict = next(
        (user for user in data["users"] if user["username"] == current_user), None
    )

    if user_dict != None:
        list_items()

        item_idx_raw = input(
            "Enter the index of the item to remove (leave empty to not remove any item): "
        ).strip()
        while item_idx_raw != "" and (
            not item_idx_raw.isdigit()
            or not (1 <= int(item_idx_raw) <= len(user_dict["items"]))
        ):
            print(
                f"Invalid input. Please enter a number between 1 and {len(user_dict['items'])}.\n"
            )
            item_idx_raw = input(
                "Enter the index of the item to remove (leave empty to not remove any item): "
            ).strip()

        clear()
        if item_idx_raw == "":
            print("No items removed.\n")
            return

        item_idx = int(item_idx_raw) - 1

        removed_item = user_dict["items"].pop(item_idx)
        crud.write_save_file(data)
        print(f"Item '{removed_item}' removed.\n")
    else:
        print("User not found.\n")


def list_items():
    clear()
    if current_user == None:
        print("No user is currently logged in.\n")
        return

    # Get user dict where username matches current_user
    user_dict = next(
        (user for user in data["users"] if user["username"] == current_user), None
    )

    if user_dict == None:
        print("User not found.\n")
        return

    if user_dict["items"] == None or len(user_dict["items"]) <= 0:
        print("No items found.\n")
        return

    print("These are your items\n")

    for i, item in enumerate(user_dict["items"]):
        print(f"    {i + 1}) {item}")

    if user_dict["items"] and len(user_dict["items"]) > 0:
        print()


def get_pressed_key(valid_keys=None):
    key = msvcrt.getch()
    try:
        decoded_key = key.decode("utf-8").lower()
    except UnicodeDecodeError:
        decoded_key = None

    invalid_message_shown = False

    while valid_keys != None and decoded_key not in valid_keys:
        if key == b"\x03":  # Ctrl+C
            exit()

        if decoded_key not in valid_keys and decoded_key != None:
            print(f"Invalid key '{decoded_key}'. Please press", end=" ")
            invalid_message_shown = True
            for i, valid_key in enumerate(valid_keys):
                if i == len(valid_keys) - 1:
                    print(f"or {valid_key}", end="\n")
                elif i == len(valid_keys) - 2:
                    print(valid_key, end=" ")
                else:
                    print(valid_key, end=", ")

        key = msvcrt.getch()
        try:
            decoded_key = key.decode("utf-8").lower()
        except UnicodeDecodeError:
            decoded_key = None

    if invalid_message_shown:
        print()

    sleep(0.1)  # Add a small delay for better feel
    return decoded_key


def main():
    global data

    data = crud.read_save_file()

    if not data or not data["users"]:
        print("No save data found. Using default data...\n")
        data = crud.read_save_file("default_save.json")

    while (
        True
    ):  # While loop to keep the program running until the user chooses to quit, at which point exit() will be called in the quit() function.
        welcome()

        if current_user != None:
            welcome_user()

            while current_user != None:
                select_user_action()


clear()
main()
