from models import Record, AddressBook

class InputError(Exception):
    pass

class ContactAssistant:
    def __init__(self):
        self.address_book = AddressBook()

    def add_contact(self, name, phone):
        try:
            record = Record(name)
            record.add_phone(phone)
            self.address_book.add_record(record)
            return f"Contact {name} added with phone {phone}"
        except ValueError as e:
            raise InputError(str(e))

    def change_contact(self, name, phone):
        try:
            record = self.address_book.find(name)
            if record:
                record.edit_phone(record.phones[0].value, phone)
                return f"Phone number for {name} changed to {phone}"
            else:
                raise IndexError
        except (ValueError, IndexError) as e:
            raise InputError(str(e))

    def get_phone(self, name):
        try:
            record = self.address_book.find(name)
            if record:
                return f"The phone number for {name} is {record.phones[0]}"
            else:
                raise IndexError
        except (ValueError, IndexError) as e:
            raise InputError(str(e))

    def show_all_contacts(self):
        records = list(self.address_book.values())
        if not records:
            return "No contacts found"
        else:
            result = "All contacts:\n"
            for record in records:
                result += f"{record.name}: {record.phones[0]}\n"
            return result.strip()


class CommandHandler:
    def __init__(self, contact_assistant):
        self.contact_assistant = contact_assistant

    def handle_hello(self, args):
        return "How can I help you?"

    def handle_add(self, args):
        if len(args) == 0:
            raise InputError("Invalid command. Please try again. Use 'add <name> <phone>'")

        contact_info = args.split(" ")
        if len(contact_info) != 3:
            raise InputError("Invalid command. Please try again. Use 'add <name> <phone>'")

        _, name, phone = args.split(" ")
        return self.contact_assistant.add_contact(name, phone)

    def handle_change(self, args):
        if len(args) == 0:
            raise InputError("Invalid command. Please try again. Use 'change <name> <phone>'")

        contact_info = args.split(" ")
        if len(contact_info) != 3:
            raise InputError("Invalid command. Please try again. Use 'add <name> <phone>'")

        _, name, phone = args.split(" ")
        return self.contact_assistant.change_contact(name, phone)

    def handle_phone(self, args):
        if len(args) == 0:
            raise InputError("Invalid command. Please try again. Use 'phone <name>'")
        args_list = args.split(" ")
        name = args_list[1]
        return self.contact_assistant.get_phone(name)

    def handle_show(self, args):
        return self.contact_assistant.show_all_contacts()

    def handle_bye(self, args):
        print("Good bye!")
        return None

    def choice_action(self, data):
        actions = {
            'hello': self.handle_hello,
            'add': self.handle_add,
            "change": self.handle_change,
            "phone": self.handle_phone,
            "show": self.handle_show,
            "close": self.handle_bye,
            "exit": self.handle_bye,
            "good bye": self.handle_bye,
        }
        return actions.get(data, lambda args: "Invalid command")

    def process_input(self, user_input):
        try:
            if not user_input:
                raise InputError("Invalid command. Please try again.")

            space_index = user_input.find(' ')

            if space_index != -1:
                first_word = user_input[:space_index]
            else:
                first_word = user_input

            if first_word in ["good", "bye"]:
                first_word = "good bye"

            func = self.choice_action(first_word)
            result = func(user_input)

            if result is None:
                return None
            else:
                return result
        except InputError as e:
            return str(e)


def main():
    contact_assistant = ContactAssistant()
    command_handler = CommandHandler(contact_assistant)

    while True:
        try:
            user_input = input("Enter command: ").lower().strip()
            result = command_handler.process_input(user_input)

            if result is None:
                break
            else:
                print(result)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
