import pickle
from collections import UserDict



class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Birthday(Field):
    pass


class Record:
    def __init__(self, name: Name, phones=None, birthday: Birthday = None):
        self.name = name
        self.phones = phones if phones else []
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone_value: str):
        self.phones = [p for p in self.phones if p.value != phone_value]


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, name: str):
        if name in self.data:
            del self.data[name]


def save_data(book: AddressBook, filename="addressbook.pkl"):

    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl") -> AddressBook:

    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()



def main():

    book = load_data()

    print("Ласкаво просимо до адресної книги!")

    while True:
        print("\nМеню:")
        print("1. Додати контакт")
        print("2. Видалити контакт")
        print("3. Показати всі контакти")
        print("4. Вийти")

        choice = input("Оберіть опцію (1-4): ").strip()

        if choice == "1":
            name_input = input("Ім'я: ").strip()
            phone_input = input("Телефон: ").strip()
            record = Record(Name(name_input))
            record.add_phone(Phone(phone_input))
            book.add_record(record)
            print(f"Контакт '{name_input}' додано!")

        elif choice == "2":
            name_input = input("Введіть ім'я для видалення: ").strip()
            if name_input in book:
                book.remove_record(name_input)
                print(f"Контакт '{name_input}' видалено!")
            else:
                print("Такого контакту не існує.")

        elif choice == "3":
            if not book.data:
                print("Адресна книга порожня.")
            else:
                print("Контакти:")
                for name, record in book.data.items():
                    phones = ", ".join([p.value for p in record.phones])
                    print(f"{name}: {phones}")

        elif choice == "4":

            save_data(book)
            print("Адресна книга збережена. До побачення!")
            break

        else:
            print("Невірний вибір, спробуйте ще раз.")


if __name__ == "__main__":
    main()