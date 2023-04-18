import json
from datetime import date
from templates import *
# from application import Application


APPLICATIONS_FILE_PATH = "applications.json"
NOT_EDITABLE_VALUES = ["id", "application_date"]

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
    position = input("Input the position/role: ")
    company = input("Input the company: ")
    contact = input("Input the contact: ")
    while True:
        priority = input("Input a priority number between 1 and 5 (both included): ")
        
        if priority.isnumeric():
            priority = int(priority)
            if 1 <= priority <= 5:
                break
        
        print("Error, wrong input.")
        
    description = input("Input a description (opt): ")
    location = input("Input the location (opt): ")
    notes = input("Input notes (opt): ")
    url = input("Input url (opt): ")
    
    interview_date = input("Input the interview date (YYYY-MM-DD, opt):")
    
    ### EVENTUAL CHECK ON INTERVIEW DATE

    if interview_date != "":
        interview_date = date.fromisoformat(interview_date)

    application = {
        "id": len(applications),
        "position": position,
        "company": company,
        "contact": contact,
        "status": "Pending",
        "priority": priority,
        "description": description,
        "location": location,
        "notes": notes,
        "url": url,
        "application_date": date.today(),
        "interview_date": interview_date
    }

    if is_different_application(applications, application):
        applications.append(application)
        print("Application added.")
    else:
        print("Error, already applied to the position.")


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
    SKIP_INPUT = "no edit"
    temp_application = None
    application_idx = None
    for idx in range(len(applications)):
        application = applications[idx]
        if application["id"] == id:
            temp_application = application
            application_idx = idx

            print(f"You can skip editing values by typing {SKIP_INPUT}.")
            for key, value in application.items():
                if key in NOT_EDITABLE_VALUES:
                    continue

                new_value = input(f"Current {key}: {value}. Input new {key}:")
                if new_value == SKIP_INPUT:
                    continue

                temp_application[key] = new_value

    if temp_application is not None:
        print("This is a preview of the changes:")
        display_full_application([temp_application], temp_application["id"])

        while True:
            confirm_edit = input("Do you want to confirm the changes ? (y/n)")

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


# UNFINISHED
def format_application_short(application):
    formatted_application_str = SHORTENED_APPLICATION
    
    formatted_application_str = formatted_application_str.replace("ID_NUM", application["id"])
    formatted_application_str = formatted_application_str.replace("POSITION_NAME", application["position"])
    formatted_application_str = formatted_application_str.replace("COMPANY_NAME", application["company"])
    formatted_application_str = formatted_application_str.replace("PRIORITY_NUM", str(application["priority"]))
    formatted_application_str = formatted_application_str.replace("CURRENT_STATUS", application["status"])
    formatted_application_str = formatted_application_str.replace("CONTACT_ADDRESS", application["contact"])
    
    # prepare formatting
    formatted_application_str = formatted_application_str.replace("APPLICATION_DATE", application["application_date"])
    formatted_application_str = formatted_application_str.replace("INTERVIEW_DATE", application["interview_date"])
    
    return formatted_application_str

# UNFINISHED
def format_application_full(application):
    formatted_application_str = FULL_APPLICATION
    
    formatted_application_str = formatted_application_str.replace("ID_NUM", str(application["id"]))
    formatted_application_str = formatted_application_str.replace("POSITION_NAME", application["position"])
    formatted_application_str = formatted_application_str.replace("COMPANY_NAME", application["company"])
    formatted_application_str = formatted_application_str.replace("PRIORITY_NUM", str(application["priority"]))
    formatted_application_str = formatted_application_str.replace("CURRENT_STATUS", application["status"])
    formatted_application_str = formatted_application_str.replace("CONTACT_ADDRESS", application["contact"])
    formatted_application_str = formatted_application_str.replace("URL_ADDRESS", application["url"])
    formatted_application_str = formatted_application_str.replace("LOCATION_ADDRESS", application["location"])
    formatted_application_str = formatted_application_str.replace("FULL_DESCRIPTION", application["description"])
    formatted_application_str = formatted_application_str.replace("FULL_NOTES", application["notes"])
    
    # prepare formatting
    formatted_application_str = formatted_application_str.replace("APPLICATION_DATE", application["application_date"])
    formatted_application_str = formatted_application_str.replace("INTERVIEW_DATE", application["interview_date"])
    
    return formatted_application_str

# shows an overview of all applications
# with Position, Status, Priority, Company, Application and interview dates
def show_applications(applications):
    formatted_applications = []
    
    for application in applications:
        formatted_application = format_application_short(application)
        formatted_applications.append(formatted_application)
        
    print("\n".join(formatted_applications))


def display_full_application(applications, id):
    for application in applications:
        if application["id"] == id:
            formatted_application = format_application_full(application)
            
    print(formatted_application)


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
def sort_by_application_date(applications):
    pass


def sort_by_interview_date(applications):
    pass


def sort_by_priority(applications):
    pass


# MAIN
def main(applications_file_path):
    # print("Commands:")
    pass


if __name__ == "__main__":
    main(APPLICATIONS_FILE_PATH)
    d = {}
    print(max(d))
