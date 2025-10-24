from typing import Tuple, List, Dict, Optional, Literal, Callable, Any
from functools import wraps

Contacts = Dict[str, str]

UNIVERSAL_ERROR_MESSAGE = "Enter the argument for the command"


def input_error(func: Callable[..., str]) -> Callable[..., str]:
    """
    A decorator that handles KeyError, ValueError, and IndexError exceptions
    raised in command handler functions and returns the unified error message
    "Enter the argument for the command".
    """

    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> str:
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError):
            # Catch all required exceptions (ValueError, IndexError, KeyError)
            # and return the single universal error message, as requested.
            return UNIVERSAL_ERROR_MESSAGE

    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """
    Parses the user input string into a command and its arguments using a
    state machine approach (cycle over the string).
    Supports multi-word arguments enclosed in double (") or single (') quotes.
    Nested quotes (e.g., 'text with "inner" quotes') are treated as literal text.
    The command is case-insensitive.
    """

    args: List[str] = []

    current_arg: str = ""
    in_quotes: Optional[Literal] = None

    # Pre-process the input by normalizing spaces and stripping leading/trailing whitespace
    user_input = ' '.join(user_input.split())

    if not user_input:
        return "", []

    parts = user_input.split(maxsplit=1)
    command = parts[0].strip().lower()

    if len(parts) == 1:
        return command, []

    args_string = parts[1]

    for char in args_string:
        if in_quotes is not None:
            if char == in_quotes:
                in_quotes = None
            else:
                current_arg += char
        else:
            if char in ('"', "'"):
                in_quotes = char
            elif char == ' ':
                if current_arg:
                    args.append(current_arg)
                current_arg = ""
            else:
                current_arg += char

    if current_arg or (current_arg == "" and in_quotes is None and args_string.endswith(('"', "'")) and not args):
        # Add the last collected argument, or handle case where input ends with an argument in quotes
        args.append(current_arg)

    # Check for unclosed quotes after processing
    if in_quotes is not None:
        # If quotes are unclosed, treat the whole remaining part as one argument
        # For this simple bot, we'll just return the arguments collected so far,
        # but in a real app, this would be an error.
        pass

    return command, args


@input_error
def add_contact(args: List[str], contacts: Contacts) -> str:
    """
    Adds a new contact (name and phone) to the contacts dictionary.
    Raises IndexError if args are missing.
    Raises ValueError if contact already exists (treated as input error).
    """
    name, phone = args

    if name in contacts:
        raise ValueError(f"Contact name '{name}' already exists.")

    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: List[str], contacts: Contacts) -> str:
    """
    Changes the phone number for an existing contact.
    Raises IndexError if args are missing.
    Raises KeyError if contact is not found.
    """
    name, new_phone = args

    if name not in contacts:
        raise KeyError(f"Contact name '{name}' not found.")

    contacts[name] = new_phone
    return "Contact updated."


@input_error
def show_phone(args: List[str], contacts: Contacts) -> str:
    """
    Retrieves and displays the phone number for a given contact name.
    Raises IndexError if args are missing.
    Raises KeyError if contact is not found.
    """
    name = args[0]

    return contacts[name]


def show_all(contacts: Contacts) -> str:
    """
    Displays all stored contacts and their phone numbers.
    """
    if not contacts:
        return "No contacts saved."

    all_contacts: List[str] = []
    for name, phone in contacts.items():
        all_contacts.append(f"{name}: {phone}")

    return "\n".join(all_contacts)


def main() -> None:
    """
    The main function that manages the command processing loop.
    """
    contacts: Contacts = {}

    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input: str = input("Enter a command: ").strip()
        # Handle EOF (e.g., Ctrl+D) to exit gracefully
        except EOFError:
            print("\nGood bye!")
            break

        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
