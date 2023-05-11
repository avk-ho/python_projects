import json
from datetime import date
from templates import *
# from application import Application


APPLICATIONS_FILE_PATH = "applications.json"
NON_EDITABLE_VALUES = ["id", "application_date"]

# FILE MODIFICATIONS


def read_applications(file_path):
    try:
        with open(file_path, "r") as file:
            applications = json.load(file)["applications"]
    except FileNotFoundError:
        applications = []

    return applications


def write_applications(file_path, applications):
    with open(file_path, "w") as file:
        applications = {"applications": applications}
        json.dump(applications, file)


# APPLICATIONS
def add_application(applications):
    # Mandatory fields
    while True:
        position = input("Input the position/role: ")
        if position == "":
            print("Mandatory field, please enter the position/role.")
        else:
            break

    while True:
        company = input("Input the company: ")
        if company == "":
            print("Mandatory field, please enter the company name.")
        else:
            break

    while True:
        contact = input("Input the contact: ")
        if contact == "":
            print("Mandatory field, please enter a contact address.")
        else:
            if is_valid_contact(contact):
                break
            else:
                print("Invalid contact address.")

    while True:
        priority = input(
            "Input a priority number between 1 and 5 (both included): ")

        if priority.isnumeric():
            priority = int(priority)
            if 1 <= priority <= 5:
                break

        print("Invalid input.")

    application_date = date.isoformat(date.today())

    # Optional fields
    description = input("Input a description (opt): ")
    location = input("Input the location (opt): ")
    notes = input("Input notes (opt): ")

    while True:
        url = input("Input url (opt): ")

        if url == "":
            break
        else:
            if is_valid_url(url):
                break
            else:
                print("Invalid url.")

    while True:
        interview_date = input("Input the interview date (YYYY-MM-DD, opt): ")

        if interview_date != "":
            if is_valid_interview_date(interview_date, application_date):
                break
            else:
                print("Invalid date.")

        else:
            interview_date = ""
            break

    application = {
        "id": len(applications),
        "position": position,
        "company": company,
        "contact": contact,
        "status": "pending",
        "priority": priority,
        "description": description,
        "location": location,
        "notes": notes,
        "url": url,
        "application_date": application_date,
        "interview_date": interview_date
    }

    if is_different_application(applications, application):
        applications.append(application)
        print("Application added.")
    else:
        print("Error, already applied to the position.")


def is_valid_contact(contact):
    if not "@" in contact:
        return False

    split_contact = contact.split("@")
    identifier = "".join(split_contact[:-1])
    domain = split_contact[-1]

    if len(identifier) < 1:
        return False

    if "." not in domain:
        return False

    if domain.count(".") > 1:
        return False

    split_domain = domain.split(".")
    for section in split_domain:
        if section == "":
            return False

    return True


def is_valid_url(url):
    if not "." in url:
        return False

    split_url = url.split(".")
    for section in split_url:
        if section == "":
            return False

    return True


def is_valid_interview_date(interview_date_str, application_date_str):
    if "-" not in interview_date_str:
        return False

    split_interview_date = interview_date_str.split("-")
    if len(split_interview_date) != 3:
        return False

    for idx in range(len(split_interview_date)):
        section = split_interview_date[idx]
        if section == "":
            return False
        if not section.isnumeric():
            return False

        if idx == 1:
            if not (1 <= int(section) <= 12):
                return False

        if idx == 2:
            if not (1 <= int(section) <= 31):
                return False

    interview_date = date.fromisoformat(interview_date_str)
    application_date = date.fromisoformat(application_date_str)
    if interview_date > application_date:
        return True
    else:
        return False

    # application date more recent than interview date
    if interview_date < application_date:
        return False

    return True


def is_different_application(applications, new_application):
    # check Position, Company, Application date
    is_different = True

    position = new_application["position"]
    company = new_application["company"]
    application_date = new_application["application_date"]
    relevant_applications = search_by_company(applications, company)

    for application in relevant_applications:
        if application_date == application["application_date"] \
                and position == application["position"]:
            is_different = False
            break

    return is_different


def edit_application(applications, id):
    SKIP_INPUT = "skip"
    temp_application = None
    application_idx = None
    for idx in range(len(applications)):
        application = applications[idx]
        if application["id"] == id:
            temp_application = application.copy()
            application_idx = idx

            print(f"You can skip editing values by typing '{SKIP_INPUT}'.")
            for key, value in temp_application.items():
                if key in NON_EDITABLE_VALUES:
                    continue

                while True:
                    if key == "interview_date":
                        new_value = input(
                            f"Current {key}: '{value}'. Input new {key} (YYYY-MM-DD): ")
                    else:
                        new_value = input(
                            f"Current {key}: '{value}'. Input new {key}: ")

                    if new_value == SKIP_INPUT:
                        break

                    elif key == "interview_date" and new_value != "":
                        if is_valid_interview_date(new_value, application["application_date"]):
                            break

                        print("Invalid new date.")

                    # Mandatory fields
                    elif new_value == "" and \
                        (key == "contact" or key == "status" or key == "position"
                            or key == "company"):
                        print(
                            f"Error, either '{SKIP_INPUT}' or a value must be given.'")

                    elif key == "priority":
                        if new_value.isnumeric():
                            new_value = int(new_value)
                            if 1 <= new_value <= new_value:
                                break

                        print("Error, input not a number between 1 and 5.")
                    else:
                        break

                if new_value == SKIP_INPUT:
                    continue

                temp_application[key] = new_value

    if temp_application is not None:
        print("This is a preview of the changes:")
        display_full_application([temp_application], temp_application["id"])

        while True:
            confirm_edit = input("Do you want to confirm the changes (y/n)? ")

            if confirm_edit == "y":
                applications[application_idx] = temp_application
                print("Changes applied.")
                break
            elif confirm_edit == "n":
                print("Changes reversed.")
                break
            else:
                print("Error, wrong input.")

    else:
        print(f"Error, no application with the id: {id} exists.")


def format_application_short(application):
    formatted_application_str = SHORTENED_APPLICATION

    # Mandatory fields
    formatted_application_str = formatted_application_str.replace(
        "ID_NUM", str(application["id"]))
    formatted_application_str = formatted_application_str.replace(
        "POSITION_NAME", application["position"])
    formatted_application_str = formatted_application_str.replace(
        "COMPANY_NAME", application["company"])
    formatted_application_str = formatted_application_str.replace(
        "PRIORITY_NUM", str(application["priority"]))
    formatted_application_str = formatted_application_str.replace(
        "CURRENT_STATUS", application["status"])
    formatted_application_str = formatted_application_str.replace(
        "CONTACT_ADDRESS", application["contact"])

    application_date_str = application["application_date"]
    formatted_application_str = formatted_application_str.replace(
        "APPLICATION_DATE", application_date_str)

    # Optional fields
    str_interview_date = application["interview_date"]
    if str_interview_date != "":
        str_interview_date = "| Interview: " + str_interview_date
    formatted_application_str = formatted_application_str.replace(
        "INTERVIEW_DATE", str_interview_date)

    return formatted_application_str.strip()


def format_application_full(application):
    formatted_application_str = FULL_APPLICATION

    # Mandatory fields
    formatted_application_str = formatted_application_str.replace(
        "ID_NUM", str(application["id"]))
    formatted_application_str = formatted_application_str.replace(
        "POSITION_NAME", application["position"])
    formatted_application_str = formatted_application_str.replace(
        "COMPANY_NAME", application["company"])
    formatted_application_str = formatted_application_str.replace(
        "PRIORITY_NUM", str(application["priority"]))
    formatted_application_str = formatted_application_str.replace(
        "CURRENT_STATUS", application["status"])
    formatted_application_str = formatted_application_str.replace(
        "CONTACT_ADDRESS", application["contact"])

    application_date_str = application["application_date"]
    formatted_application_str = formatted_application_str.replace(
        "APPLICATION_DATE", application_date_str)

    # Optional fields
    str_interview_date = ""
    if application["interview_date"] != "":
        str_interview_date = "| Interview: " + application["interview_date"]
    formatted_application_str = formatted_application_str.replace(
        "INTERVIEW_DATE", str_interview_date)

    str_url = ""
    if application["url"] != "":
        str_url = "| Url: " + application["url"]
    formatted_application_str = formatted_application_str.replace(
        "URL_ADDRESS", str_url)

    str_location = ""
    if application["location"] != "":
        str_location = "| Location: " + application["location"]
    formatted_application_str = formatted_application_str.replace(
        "LOCATION_ADDRESS", str_location)

    str_description = ""
    if application["description"] != "":
        str_description = "Description: \n" + application["description"]
    formatted_application_str = formatted_application_str.replace(
        "FULL_DESCRIPTION", str_description)

    str_notes = ""
    if application["notes"] != "":
        str_notes = "Notes: \n" + application["notes"]
    formatted_application_str = formatted_application_str.replace(
        "FULL_NOTES", str_notes)

    return formatted_application_str.strip()

# shows an overview of all applications
# with Position, Status, Priority, Company, Application and interview dates


def list_applications(applications):
    formatted_applications = []

    for application in applications:
        formatted_application = format_application_short(application)
        formatted_applications.append(formatted_application)

    print("\n" + "\n".join(formatted_applications) + "\n")

    if len(formatted_applications) == 0:
        print("No applications found.")


def display_full_application(applications, id):
    formatted_application = ""
    for application in applications:
        if application["id"] == id:
            formatted_application = format_application_full(application)

    if formatted_application == "":
        formatted_application = f"No application with id: {id} found."

    print("\n" + formatted_application + "\n")


# SEARCH
def search_by_status(applications, status):
    relevant_applications = []
    for application in applications:
        if application["status"] == status:
            relevant_applications.append(application)

    return relevant_applications


def search_by_company(applications, company):
    relevant_applications = []
    for application in applications:
        if application["company"] == company:
            relevant_applications.append(application)

    return relevant_applications


def search_by_location(applications, location):
    relevant_applications = []
    for application in applications:
        if application["location"] == location:
            relevant_applications.append(application)

    return relevant_applications


# SORT
def sort_by_application_date(applications, reverse=False):
    # by default, most recent to less recent
    # if reverse == True, less recent to most recent
    def recursive_sort_helper(application, sorted_applications, reverse):
        if len(sorted_applications) == 0:
            sorted_applications.append(application)
            return

        prev_application = sorted_applications.pop()
        prev_application_date_str = prev_application["application_date"]
        current_application_date_str = application["application_date"]
        prev_application_date = date.fromisoformat(prev_application_date_str)
        current_application_date = date.fromisoformat(current_application_date_str)

        if not reverse:
            # if prev application date is less recent
            if prev_application_date < current_application_date:
                recursive_sort_helper(
                    application, sorted_applications, reverse)
                sorted_applications.append(prev_application)

            else:
                sorted_applications.append(prev_application)
                sorted_applications.append(application)
        else:
            if prev_application_date > current_application_date:
                recursive_sort_helper(
                    application, sorted_applications, reverse)
                sorted_applications.append(prev_application)

            else:
                sorted_applications.append(prev_application)
                sorted_applications.append(application)

    sorted_applications = []
    for application in applications:
        recursive_sort_helper(application, sorted_applications, reverse)

    return sorted_applications


def sort_by_interview_date(applications, reverse=False):
    # by default, most recent to less recent
    # if reverse == True, less recent to most recent
    def recursive_sort_helper(application, sorted_applications, reverse):
        if len(sorted_applications) == 0:
            sorted_applications.append(application)
            return

        prev_application = sorted_applications.pop()
        prev_interview_date_str = prev_application["interview_date"]
        current_interview_date_str = application["interview_date"]
        prev_interview_date = None
        current_interview_date = None

        if prev_interview_date_str != "":
            prev_interview_date = date.fromisoformat(prev_interview_date_str)
        if current_interview_date_str != "":
            current_interview_date = date.fromisoformat(current_interview_date_str)
        
        if prev_interview_date is None:
            recursive_sort_helper(application, sorted_applications, reverse)
            sorted_applications.append(prev_application)
        elif current_interview_date is None:
            recursive_sort_helper(prev_application, sorted_applications, reverse)
            sorted_applications.append(application)
        
        else: #if prev_interview_date is not None and current_interview_date is not None:
            if not reverse:
                # if prev interview date is less recent
                if prev_interview_date < current_interview_date:
                    recursive_sort_helper(
                        application, sorted_applications, reverse)
                    sorted_applications.append(prev_application)

                else:
                    sorted_applications.append(prev_application)
                    sorted_applications.append(application)
            else:
                if prev_interview_date > current_interview_date:
                    recursive_sort_helper(
                        application, sorted_applications, reverse)
                    sorted_applications.append(prev_application)

                else:
                    sorted_applications.append(prev_application)
                    sorted_applications.append(application)

    sorted_applications = []
    for application in applications:
        recursive_sort_helper(application, sorted_applications, reverse)

    return sorted_applications


def sort_by_priority(applications, reverse=False):
    # by default, highest priority to lowest
    # if reverse == True, lowest priority to highest
    def recursive_sort_helper(application, sorted_applications, reverse):
        if len(sorted_applications) == 0:
            sorted_applications.append(application)
            return

        prev_application = sorted_applications.pop()
        if reverse:
            if prev_application["priority"] < application["priority"]:
                recursive_sort_helper(
                    application, sorted_applications, reverse)
                sorted_applications.append(prev_application)

            else:
                sorted_applications.append(application)
                sorted_applications.append(prev_application)
        else:
            if prev_application["priority"] > application["priority"]:
                recursive_sort_helper(
                    application, sorted_applications, reverse)
                sorted_applications.append(prev_application)

            else:
                sorted_applications.append(application)
                sorted_applications.append(prev_application)

    sorted_applications = []
    for application in applications:
        recursive_sort_helper(application, sorted_applications, reverse)

    return sorted_applications


# MAIN
def main(applications_file_path):
    applications = read_applications(APPLICATIONS_FILE_PATH)

    end_program = False
    while not end_program:
        print('List of commands: \n' +
              '"add": Adds an application. \n' +
              '"edit <id>": Edits the application with <id>. \n' +
              '"list": Lists all applications. \n' +
              '"read <id>": Show application <id> in full detail. \n' +
              '"search <criteria> <name>": Searches for applications by <criteria> (status/company/location) + <name> (ex: pending, Google, Paris). \n' +
              '    ex: "search status accepted"\n' +
              '"sort <criteria> <direction>": Sorts by <criteria> (application/interview/priority) in <direction> (asc/desc).\n' +
              '    ex: "sort application desc"\n' +
              '"q": Saves and quits the program. ')

        user_input = input("Type your command: ")

        # PROCESS INPUT
        split_input = user_input.split()
        command = split_input[0]

        if len(split_input) == 1:
            if command == "add":
                add_application(applications)

            elif command == "list":
                list_applications(applications)

            elif command == "q":
                end_program = True

            else:
                print("Error, wrong input.")

        elif len(split_input) == 2:
            if split_input[1].isnumeric():
                id = int(split_input[1])

                if command == "edit":
                    edit_application(applications, id)

                elif command == "read":
                    display_full_application(applications, id)

                else:
                    print("Error, wrong input.")
            else:
                print("Error, wrong input.")

        elif len(split_input) > 2:
            criteria = split_input[1]

            if command == "search":
                if criteria == "status":
                    valid_status = ["pending", "accepted",
                                    "refused", "cancelled"]
                    status = split_input[2].lower()
                    if status in valid_status:
                        search_result = search_by_status(applications, status)
                        list_applications(search_result)

                elif criteria == "company":
                    name = " ".join(split_input[2:])
                    search_result = search_by_company(applications, name)
                    list_applications(search_result)

                elif criteria == "location":
                    name = " ".join(split_input[2:])
                    search_result = search_by_location(applications, name)
                    list_applications(search_result)

                else:
                    print("Error, wrong input.")

            elif command == "sort":
                direction = split_input[2]

                reverse = False
                if direction == "asc":
                    reverse = True

                if criteria == "application":
                    applications = sort_by_application_date(
                        applications, reverse)
                    list_applications(applications)
                elif criteria == "interview":
                    applications = sort_by_interview_date(
                        applications, reverse)
                    list_applications(applications)
                elif criteria == "priority":
                    applications = sort_by_priority(applications, reverse)
                    list_applications(applications)

                else:
                    print("Error, wrong input.")

            else:
                print("Error, wrong input.")

    write_applications(APPLICATIONS_FILE_PATH, applications)
    print("Applications saved. Ending program.")


if __name__ == "__main__":
    main(APPLICATIONS_FILE_PATH)
