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
    


# Приклад для використання
address_book = AddressBook()

# Додаємо контакт
contact1 = Record("John Doe")
contact1.add_phone("123456789")
contact1.add_birthday("15.05.1990")
address_book.add_contact(contact1)

contact2 = Record("Jane Smith")
contact2.add_phone("987654321")
contact2.add_birthday("20.05.1985")
address_book.add_contact(contact2)



# Отримуємо список контактів з наступними днями народженнями
upcoming_birthdays = address_book.get_upcoming_birthdays()
for contact in upcoming_birthdays:
    print(f"{contact.name.value}'s birthday is coming up!")
