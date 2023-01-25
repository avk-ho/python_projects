# https://www.programmingexpert.io/projects/contact-list

# valid phone number: 10 digits, only numbers
# each unique contact has a unique first and last name combination

# contacts = {"contacts": [{contact}]}

# contact:
# First Name: str
# Last Name: str
# Mobile phone number: int (opt)
# Home phone number: int (opt)
# Email: str (opt)
# Address: str (opt)

import json

CONTACT_FILE_PATH = "contacts.json"

### BASE CODE ###
def read_contacts(file_path):
    try:
        with open(file_path, 'r') as f:
            contacts = json.load(f)['contacts']
    except FileNotFoundError:
        contacts = []

    return contacts


def write_contacts(file_path, contacts):
    with open(file_path, 'w') as f:
        contacts = {"contacts": contacts}
        json.dump(contacts, f)


def verify_email_address(email):
    if "@" not in email:
        return False

    split_email = email.split("@")
    identifier = "".join(split_email[:-1])
    domain = split_email[-1]

    if len(identifier) < 1:
        return False

    if "." not in domain:
        return False

    split_domain = domain.split(".")

    for section in split_domain:
        if len(section) == 0:
            return False

    return True

### END OF BASE CODE ###
# takes a string, returns a bool
def verify_phone_number(phone_num):
    stripped_num = phone_num.split("-")
    
    if len(stripped_num) == 3:
        valid = len(stripped_num[0]) == 3 and len(stripped_num[1]) == 3 and len(stripped_num[2]) == 4
    else:
        valid = len(stripped_num) == 1

    stripped_num = "".join(stripped_num)

    return valid and stripped_num.isdecimal() and len(stripped_num) == 10

# recursive alphabetical sort used in add_contact
def add_contact_sort_helper(new_contact, contacts):
    if len(contacts) == 0:
        contacts.append(new_contact)
        return
    
    prev_contact = contacts.pop()
    new_first_name = new_contact["First Name"].lower()
    new_last_name = new_contact["Last Name"].lower()

    prev_first_name = prev_contact["First Name"].lower()
    prev_last_name = prev_contact["Last Name"].lower()

    new_longest_first_name = len(new_first_name) >= len(prev_first_name)
    if new_longest_first_name:
        for i in range(len(new_first_name)):
            if i >= len(prev_first_name):
                contacts.append(prev_contact)
                contacts.append(new_contact)
                return
            elif new_first_name[i] == prev_first_name[i]:
                continue
            elif new_first_name[i] > prev_first_name[i]:
                contacts.append(prev_contact)
                contacts.append(new_contact)
                return
            else:
                add_contact_sort_helper(new_contact, contacts)
                contacts.append(prev_contact)
                return
    else:
        for i in range(len(prev_first_name)):
            if i >= len(new_first_name):
                add_contact_sort_helper(new_contact, contacts)
                contacts.append(prev_contact)
                return
            elif new_first_name[i] == prev_first_name[i]:
                continue
            elif new_first_name[i] > prev_first_name[i]:
                contacts.append(prev_contact)
                contacts.append(new_contact)
                return
            else:
                add_contact_sort_helper(new_contact, contacts)
                contacts.append(prev_contact)
                return

    new_longest_last_name = len(new_last_name) >= len(prev_last_name)
    if new_longest_last_name:
        for i in range(len(new_last_name)):
            if i >= len(prev_last_name):
                contacts.append(prev_contact)
                contacts.append(new_contact)
                return
            elif new_last_name[i] == prev_last_name[i]:
                continue
            elif new_last_name[i] > prev_last_name[i]:
                contacts.append(prev_contact)
                contacts.append(new_contact)
                return
            else:
                add_contact_sort_helper(new_contact, contacts)
                contacts.append(prev_contact)
                return
    else:
        for i in range(len(prev_last_name)):
            if i >= len(new_last_name):
                add_contact_sort_helper(new_contact, contacts)
                contacts.append(prev_contact)
                return
            elif new_last_name[i] == prev_last_name[i]:
                continue
            elif new_last_name[i] > prev_last_name[i]:
                contacts.append(prev_contact)
                contacts.append(new_contact)
                return
            else:
                add_contact_sort_helper(new_contact, contacts)
                contacts.append(prev_contact)
                return


def add_contact(contacts):
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    mobile_phone_num = input("Mobile Phone Number: ")
    home_phone_num = input("Home Phone Number: ")
    email = input("Email Address: ")
    address = input("Address: ")

    valid_names = len(first_name) > 0 and len(last_name) > 0
    valid_mobile_num = verify_phone_number(mobile_phone_num) or mobile_phone_num == ""
    valid_home_num = verify_phone_number(home_phone_num) or home_phone_num == ""
    valid_email = verify_email_address(email) or email == ""

    already_exists = False
    for contact in contacts:
        if contact["First Name"] == first_name and contact["Last Name"] == last_name:
            already_exists = True

    if not valid_names:
        print("Contact must have a first name and last name.")

    if not valid_email:
        print("Invalid email address.")

    if not valid_mobile_num:
        print("Invalid mobile phone number.")

    if not valid_home_num:
        print("Invalid home phone number.")

    if already_exists:
        print("A contact with this name already exists.")
    
    if not already_exists and valid_names and valid_email and \
        valid_home_num and valid_mobile_num:
        contact = {
            "First Name": first_name,
            "Last Name": last_name,
            "Mobile phone number": mobile_phone_num,
            "Home phone number": home_phone_num,
            "Email": email,
            "Address": address
        }

        add_contact_sort_helper(contact, contacts)
        print("Contact added!")

    else:
        print("You entered invalid information, this contact was not added.")

def search_for_contact(contacts):
    if len(contacts) < 1:
        print("No contact registered. Please add a contact first. ")
        return
    
    target_first_name = input("First Name: ").lower()
    target_last_name = input("Last Name: ").lower()
    
    if target_first_name == "" and target_last_name == "":
        print("Please enter at least either a First Name or a Last Name.")
        return

    matching_contacts = []
    for contact in contacts:
        first_name = contact["First Name"].lower()
        last_name = contact["Last Name"].lower()

        first_valid = target_first_name in first_name
        last_valid = target_last_name in last_name
        
        if first_valid and last_valid:
            matching_contacts.append(contact)

    if len(matching_contacts) > 0:
        print(f"Found {len(matching_contacts)} matching contacts.")
        list_contacts(matching_contacts)

    else:
        print("No match found.")


def delete_contact(contacts):
    if len(contacts) < 1:
        print("No contact registered. Please add a contact first. ")
        return

    target_first_name = input("First Name: ")
    target_last_name = input("Last Name: ")

    target_idx = -1
    for i in range(len(contacts)):
        contact = contacts[i]
        if contact["First Name"] == target_first_name and contact["Last Name"] == target_last_name:
            target_idx = i
            break

    if target_idx >= 0:
        confirm_delete = input(
            "Are you sure you would like to delete this contact (y/n)? ")
        
        if confirm_delete == "y":
            contacts.pop(target_idx)
            print("Contact deleted!")

    else:
        print("No contact with this name exists.")



def list_contacts(contacts):
    if len(contacts) < 1:
        print("No contact registered. Please add a contact first. ")
    else:
        i = 1
        for contact in contacts:
            name = contact["First Name"] + " " + contact["Last Name"]
            mobile = contact["Mobile phone number"]
            home = contact["Home phone number"]
            email = contact["Email"]
            address = contact["Address"]

            print(str(i) + ". " + name)
            if mobile != "":
                print("        Mobile: " + mobile)
            if home != "":
                print("        Home: " + home)
            if email != "":
                print("        Email: " + email)
            if address != "":
                print("        Address: " + address)

            i += 1


def main(contacts_path):
    print('Welcome to your contact list! \n' +
          'The following is a list of useable commands: \n' +
          '"add": Adds a contact. \n' +
          '"delete": Deletes a contact. \n' +
          '"list": Lists all contacts. \n' +
          '"search": Searches for a contact by name. \n' +
          '"q": Quits the program and saves the contact list. ')

    end_program = False
    contacts = read_contacts(contacts_path)
    while not end_program:
        command = input("Type a command: ")

        if command == "add":
            add_contact(contacts)
        elif command == "delete":
            delete_contact(contacts)
        elif command == "list":
            list_contacts(contacts)
        elif command == "search":
            search_for_contact(contacts)
        elif command == "q":
            end_program = True
        else:
            print("Unknown command.")


    write_contacts(contacts_path, contacts)
    print("Contacts were saved successfully. ")

if __name__ == "__main__":
    main(CONTACT_FILE_PATH)