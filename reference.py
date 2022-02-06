
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def initialize_firestore():
    """
    Create database connection
    """

    # Setup Google Cloud Key - The json file is obtained by going to 
    # Project Settings, Service Accounts, Create Service Account, and then
    # Generate New Private Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "C:/Users/Alma/Documents/W22/CSE 310/MedLog/Cloud database/Private/medilogs-4c4f3-firebase-adminsdk-6as2s-d77bec19cd.json"

    # Use the application default credentials.  The projectID is obtianed 
    # by going to Project Settings and then General.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'medilogs-4c4f3',
    })

    # Get reference to database
    db = firestore.client()
    return db

def add_new_patient(db):
    '''
    Prompt the user to add a new patient to Patients database.  The
    item name must be unique (firestore document id).  
    '''

    first_name = str(input("First Name: "))
    last_name = str(input("Last Name: "))
    birthdate = (input("Date of Birth: "))
    diagnosed = str(input("Diagnosed: "))
    injury_illness = str(input("Injury/Illness: "))

    # Build a dictionary to hold the contents of the firestore document.
    data = {"First Name" : first_name, 
            "Last Name" : last_name,
            "Date of Birth" : birthdate,
            "Diagnosed" : diagnosed,
            "Injury/Illness" : injury_illness,
            }
    db.collection("Patients").add(data)

    # Save this in the Patient collection in Firestore : Check In Confirmation:      
    log_checkin_confirmation(db, f"Added {first_name} {last_name} born {birthdate}.\n\n\nDiagnosed with {diagnosed} and will recieve treatment for {injury_illness}. ")

def add_medication_intake(db):
    '''
    Prompt the user to log medication intake from patient into Medication Log Database.  The
    item name must be unique (firestore document id).  
    '''

    first_name = str(input("First Name: "))
    last_name = str(input("Last Name: "))
    medication = str(input("Medication: "))
    medication_time = str(input("Medication Time: "))
    dosage = float(input("Dosage (mg): "))
    # Build a dictionary to hold the contents of the firestore document.
    data = {"First Name" : first_name, 
            "Last Name" : last_name,
            "Medication" : medication,
            "Medication Time" : medication_time,
            "Dosage (mg)" : dosage,
            }
    db.collection("Medication Log").add(data)

    # Save this in the Medication Confirmation collection in Firestore : Patient Medication Intake confirmation:    
    log_medication_confirmation(db, f" {first_name} {last_name}, just logged medication intake for {medication}, with a dosage amount of {dosage} mg.\n\n\n Day and Time dosage was taken: {medication_time}. ")
    
def search_patient_database(db):
    '''
    Search the database in multiple ways.
    '''

    print("Select Query")
    print("1) Show All Patient CheckIn Data")        
    print("2) Show All Patient Medication Logs")
    print("3) Show All Patient CheckIn Notifications")
    print("4) Show Medication Log Notifiations")
    
    choice = input("> ")
    print()

    # Build and execute the query based on the request made
    if choice == "1":
        results = db.collection("Patients").get()
            # Display all the results from choice:
                # Display all the results from choice:
        print("")
        print("Search Results\n")
        all_results = db.collection("Patients").get()
        for result in all_results:
            data = result.to_dict()
            print(f"\n\n\nID: {result.id}\n")
            print(f"Fields: {data}\n\n\n")
    elif choice == "2":
        results = db.collection("Medication Log").get()
                # Display all the results from choice:
        print("")
        print("Search Results\n")
        all_results = db.collection("Medication Log").get()
        for result in all_results:
            data = result.to_dict()
            print(f"\n\n\nID: {result.id}\n")
            print(f"Fields: {data}\n\n\n") 
    elif choice == "3":
        results = db.collection("Check In Confirmation").get()
                # Display all the results from choice:
        print("")
        print("Search Results\n")
        all_results = db.collection("Check In Confirmation").get()
        for result in all_results:
            data = result.to_dict()
            print(f"\n\n\nID: {result.id}\n")
            print(f"Fields: {data}\n\n\n")
    elif choice == "4":
        results = db.collection("Medication Confirmation").get()
                # Display all the results from choice:
        print("")
        print("Search Results\n")
        all_results = db.collection("Medication Confirmation").get()
        for result in all_results:
            data = result.to_dict()
            print(f"\n\n\nID: {result.id}\n")
            print(f"Fields: {data}\n\n\n")
    else:
        print("Invalid Selection")
        return

def log_checkin_confirmation(db, message):
    '''
    Save a message with current timestamp to the log collection in the
    Firestore database.
    '''
    data = {"MESSAGE" : message, "TIMESTAMP" : firestore.SERVER_TIMESTAMP}
    db.collection("Check In Confirmation").add(data)    
def log_medication_confirmation(db, message):
    '''
    Save a message with current timestamp to the log collection in the
    Firestore database.
    '''
    data = {"MESSAGE" : message, "TIMESTAMP" : firestore.SERVER_TIMESTAMP}
    db.collection("Medication Confirmation").add(data)    


def notify_patient_alert(results, changes, read_time):
    '''
    If patient was added, then display the changes.
    ADDED = Patient added medication log database.
    MODIFIED = Patient modified medication intake log.
    REMOVED = A medication intake log has been removed.
    '''

    for change in changes:
        if change.type.name == "ADDED": 
            print()
            print(f"Patient logged medication intake: {change.document.id}")
            print()
        elif change.type.name == "MODIFIED":
            print()
            print(f"Patient modified medication intake log: {change.document.id}")
            print()
        elif change.type.name == "REMOVED":
            print()
            print(f"Patient modified medication intake log: {change.document.id}")
            print()
            
    pass
        
def register_medication_time_intake_added(db):
    '''
    Monitor changes in medication log for patients.
    '''
    db.collection("Medication Log").where("Dosage","!=",0).on_snapshot(notify_patient_alert)

def main():
    db = initialize_firestore()
    register_medication_time_intake_added(db)
    choice = None
    while choice != "0":
        print("MEDILOG MENU:\n\n\n")
        print("0) Exit")
        print("1) Add New Patient")
        print("2) Log Medication Intake")
        print("3) Search Patient Database")
        choice = input(f"> ")
        print()
        if choice == "1":
            add_new_patient(db)
        elif choice == "2":
            add_medication_intake(db)
        elif choice == "3":
            search_patient_database(db)                        

if __name__ == "__main__":
    main()

