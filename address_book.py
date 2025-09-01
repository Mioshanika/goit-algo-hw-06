from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError('Name must be a non-empty string.')
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone):
        if not isinstance(phone, str) or not phone:
            raise ValueError('Phone must be a non-empty string.')
        if not len(phone) == 10 or not phone.isdigit():
            raise ValueError('Phone must be numeric string 10 digits long.')
        super().__init__(phone)

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
    def add_phone(self, phone: str):
        new_phone = Phone(phone)
        if not new_phone.value in [phone.value for phone in self.phones]:
            self.phones.append(new_phone)
    def remove_phone(self, phone: str):
        self.phones = [ph for ph in self.phones if ph.value != phone]
    def edit_phone(self, old_phone: str, new_phone: str):
        Phone(new_phone)
        if not old_phone in [phone.value for phone in self.phones]:
            raise ValueError('Phone was not found.')
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
    def find_phone(self, phone: str) -> Phone | None:
        for record_phone in self.phones:
            if record_phone.value == phone:
                return record_phone
        return None
    def __str__(self):
        output = f'Contact name: {self.name}, phones: '
        phones_string = ''
        for phone in self.phones:
            phones_string += f'{phone.value}; '
        if not phones_string:
            output += '[]'
        else:
            output += phones_string[0:-2]
        return output

class AddressBook(UserDict):
    def __init__(self, initial_data=None, custom_attribute=None):
        super().__init__(initial_data)
        self.custom_attribute = custom_attribute
    def add_record(self, record: Record):
        if not record.name.value in self.data.keys():
            self.data[record.name.value] = record
    def find(self, name: str) -> Record | None:
        for record_name in self.data.keys():
            if record_name == name:
                return self.data[record_name]
        return None
    def delete(self, name: str):
        if name in self.data.keys():
            del self.data[name]
        else:
            raise ValueError('Record was not found.')
    def __str__(self):
        output = ''
        for record in self.data.values():
            output += f'Contact [{record.name.value}] has '
            if record.phones:
                output += f'phones:\n'
                for phone in record.phones:
                    output += f' => {phone}\n'
            else:
                output += 'no phones.\n'
        return output

def main():
    book = AddressBook()

    try:
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
        book.add_record(john_record)

        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        book.add_record(jane_record)
    except Exception as e:
        print(str(e))
    
    print(book)

    john = book.find("John")
    if john:
        try:
            john.edit_phone("1234567890", "1112223333")
        except Exception as e:
            print(str(e))
        print(john)
        found_phone = john.find_phone("5555555555")
        print(f"{john.name}: {found_phone}")
    
    try:
        book.delete("Jane")
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()