import time
from collections import UserDict
from datetime import datetime, timedelta
import pickle
from typing import Any

ADDRESSBOOK_FILE_NAME = "addressbook.pkl"


class Field:
    def __init__(self, value: str):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit():
            raise ValueError("Phone must contain only digits.")
        if len(value) != 10:
            raise ValueError("Phone must contain exactly 10 digits.")
        super().__init__(value)

    def __str__(self):
        return f"+{self.value}"


class Birthday(Field):
    def __init__(self, value: str):
        if not value:
            raise ValueError("Birthday cannot be empty.")
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone: str, new_phone: str) -> bool:
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ", ".join(str(p) for p in self.phones)
        birthday = self.birthday.value if self.birthday else "-"
        return f"{self.name.value}: {phones} | Birthday: {birthday}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(
                    record.birthday.value, "%d.%m.%Y"
                ).date()

                next_birthday = birthday_date.replace(year=today.year)

                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)

                delta = (next_birthday - today).days

                if 0 <= delta <= days:
                    if next_birthday.weekday() >= 5:
                        next_birthday += timedelta(days=7 - next_birthday.weekday())

                    result.append(
                        {
                            "name": record.name.value,
                            "birthday": next_birthday.strftime("%d.%m.%Y"),
                        }
                    )

        return result


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments provided."
        except ValueError as error:
            return str(error)
        except AttributeError:
            return "Contact not found."

    return wrapper


@input_error
def add_contact(args: str, book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args: str, book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record.change_phone(old_phone, new_phone):
        return "Phone updated."
    return "Old phone not found."


@input_error
def show_phone(args: str, book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    return ", ".join(str(phone) for phone in record.phones)


@input_error
def add_birthday_handler(args: str, book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: str, book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    return record.birthday.value


@input_error
def birthdays(book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No birthdays in the next 7 days."

    return "\n".join(f"{item['name']} - {item['birthday']}" for item in upcoming)


@input_error
def show_all(book: AddressBook) -> str:
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def show_one(args: str, book: AddressBook) -> str:
    if not args:
        pass
    print(args)
    return book.data[args[0]]


def save_data(book, filename=ADDRESSBOOK_FILE_NAME) -> None:
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename=ADDRESSBOOK_FILE_NAME) -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def parse_input(user_input: str) -> tuple[None, list[Any]] | tuple[str, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return None, []

    command = parts[0]
    args = parts[1:]

    return command, args


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()

        if not user_input:
            print("Please enter a command.")
            continue

        command, args = parse_input(user_input=user_input)

        if command in ("close", "exit"):
            save_data(book=book)
            print("Save data...")
            time.sleep(3)
            print("Save data successfully")
            time.sleep(1)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args=args, book=book))
        elif command == "change":
            print(change_contact(args=args, book=book))
        elif command == "phone":
            print(show_phone(args=args, book=book))
        elif command == "all-numbers":
            print(show_all(book=book))
        elif command == "one-number":
            print(show_one(args=args, book=book))
        elif command == "add-birthday":
            print(add_birthday_handler(args=args, book=book))
        elif command == "show-birthday":
            print(show_birthday(args=args, book=book))
        elif command == "birthdays":
            print(birthdays(book=book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
