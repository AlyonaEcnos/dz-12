from models import Record, AddressBook

class ContactAssistant:
    def __init__(self):
        self.address_book = AddressBook()

    def add_contact(self, name, phone):
        record = Record(name)
        record.add_phone(phone)
        self.address_book.add_record(record)
        return f"Contact {name} added with phone {phone}"

    def change_contact(self, name, phone):
        record = self.address_book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, phone)
            return f"Phone number for {name} changed to {phone}"
        else:
            raise IndexError

    def get_phone(self, name):
        record = self.address_book.find(name)
        if record:
            return f"The phone number for {name} is {record.phones[0]}"
        else:
            raise IndexError

    def show_all_contacts(self):
        records = list(self.address_book.values())
        if not records:
            return "No contacts found"
        else:
            result = "All contacts:\n"
            for record in records:
                result += f"{record.name}: {record.phones[0]}\n"
            return result.strip()

def main():
    assistant = ContactAssistant()

    while True:
        try:
            user_input = input("Enter command: ").lower().split(" ", 1)

            if not user_input:
                raise ValueError("Invalid command. Please try again.")

            command = user_input[0]

            if command == "hello":
                print("How can I help you?")
            elif command == "add":
                if len(user_input) == 1:
                    raise ValueError("Invalid command. Please try again. Use 'add <name> <phone>'")
                _, contact_info = user_input
                if len(contact_info.split()) != 2:
                    raise ValueError("Invalid command. Please try again. Use 'add <name> <phone>'")
                name, phone = contact_info.split(" ", 1)
                print(assistant.add_contact(name, phone))
            elif command == "change":
                if len(user_input) == 1:
                    raise ValueError("Invalid command. Please try again. Use 'change <name> <phone>'")
                _, contact_info = user_input
                name, phone = contact_info.split(" ", 1)
                print(assistant.change_contact(name, phone))
            elif command == "phone":
                if len(user_input) == 1:
                    raise ValueError("Invalid command. Please try again. Use 'phone <name>'")
                _, name = user_input
                print(assistant.get_phone(name))
            elif command == "show":
                if len(user_input) == 1 or (len(user_input) == 2 and user_input[1] == "all"):
                    print(assistant.show_all_contacts())
                else:
                    raise ValueError("Invalid command. Please try again.")
            elif command in ["close", "exit"] or (user_input[0] == 'good' and user_input[1] == 'bye'):
                print("Good bye!")
                break
            else:
                raise ValueError("Invalid command. Please try again.")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
