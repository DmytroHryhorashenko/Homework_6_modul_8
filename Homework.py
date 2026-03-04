import pickle
from collections import UserDict
import re

# --- Класи для полів ---
class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value: str):
        digits = re.sub(r"\D", "", value)
        if len(digits) != 10:
            raise ValueError("Телефон повинен містити рівно 10 цифр.")
        super().__init__(digits)

class Birthday(Field):
    pass

# --- Клас для запису ---
class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone: str):
        self.phones = [p for p in self.phones if p.value != phone]

# --- Адресна книга ---
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_record(self, name: str):
        return self.data.get(name)

# --- Серіалізація та десеріалізація ---
def save_data(book: AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

# --- Основний цикл ---
def main():
    book = load_data()
    print("Адресна книга завантажена. Використовуйте add/show/exit.")

    while True:
        command_line = input(">>> ").strip()
        if not command_line:
            continue
        parts = command_line.split()
        command = parts[0].lower()

        if command == "add" and len(parts) == 3:
            name = parts[1]
            phone = parts[2]
            try:
                rec = Record(Name(name), Phone(phone))
                book.add_record(rec)
                print(f"Додано {name} з телефоном {phone}")
            except ValueError as e:
                print(e)

        elif command == "show":
            if not book.data:
                print("Адресна книга порожня.")
            for rec_name, rec in book.data.items():
                phones = ", ".join(p.value for p in rec.phones)
                print(f"{rec_name}: {phones}")

        elif command == "exit":
            save_data(book)
            print("Адресна книга збережена. Вихід...")
            break

        else:
            print("Невідома команда або неправильний формат. Використовуйте add <ім'я> <телефон>, show або exit.")

if __name__ == "__main__":
    main()