from datetime import datetime, timedelta

class Field:
    pass

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        self.value = value
        # Перевірка на коректність номера телефону

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, record):
        self.contacts.append(record)

    def get_upcoming_birthdays(self):
        today = datetime.now()
        upcoming_birthdays = []

        for contact in self.contacts:
            if contact.birthday:
                # Перевіряємо чи наступає день народження наступного тижня
                if (contact.birthday.value - today).days <= 7:
                    upcoming_birthdays.append(contact)

        return upcoming_birthdays
    
def parse_input(user_input):
    return user_input.strip().split(" ")

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return wrapper

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record:
        return f"{name} does not have a birthday set."
    else:
        return "Contact not found."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{contact.name.value}'s birthday is coming up on {contact.birthday.value.strftime('%d.%m.%Y')}." for contact in upcoming_birthdays])
    else:
        return "No upcoming birthdays in the next week."
    
@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError("Invalid number of arguments. Please provide name and phone number.")
    
    name, phone = args
    book.add_contact(name, phone)
    return f"Contact added/updated: {name} - {phone}"

@input_error
def change(args, book):
    if len(args) != 3:
        raise ValueError("Invalid number of arguments. Please provide name, old phone number, and new phone number.")
    
    name, old_phone, new_phone = args
    book.change_phone(name, old_phone, new_phone)
    return f"Phone number updated for {name}."

@input_error
def phone(args, book):
    if len(args) != 1:
        raise ValueError("Invalid number of arguments. Please provide name.")
    
    name = args[0]
    phones = book.get_phone_numbers(name)
    if phones:
        return f"Phone number(s) for {name}: {' '.join(phones)}"
    else:
        return f"No phone numbers found for {name}."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change(args, book))

        elif command == "phone":
            print(phone(args, book))

        elif command == "all":
            print(all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")