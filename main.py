
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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "inventory-d5804-firebase-adminsdk-2puf5-215941e1ae.json"

    # Use the application default credentials.  The projectID is obtianed 
    # by going to Project Settings and then General.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'inventory-d5804',
    })

    # Get reference to database
    db = firestore.client()
    return db

def add_new_item(db):
    '''
    Prompt the user for a new item to add to the inventory database.  The
    item name must be unique (firestore document id).  
    '''

    name = input("Item Name: ")
    price = float(input("Price: "))
    popular = input("Is it popular (Y/N): ") in ['Y','y']
    qty = int(input("Initial Quantity: "))

    # Check for an already existing item by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("inventory").document(name).get()
    if result.exists:
        print("Item already exists.")
        return

    # Build a dictionary to hold the contents of the firestore document.
    data = {"price" : price, 
            "popular" : popular,
            "qty" : qty}
    db.collection("inventory").document(name).set(data) 

    # Save this in the log collection in Firestore       
    log_transaction(db, f"Added {name} with initial quantity {qty}")

def add_inventory(db):
    '''
    Prompt the user to add quantity to an already existing item in the
    inventory database.  
    '''

    name = input("Item Name: ")
    add_qty = int(input("Add Quantity: "))

    # Check for an already existing item by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("inventory").document(name).get()
    if not result.exists:
        print("Invalid Item Name")
        return

    # Convert data read from the firestore document to a dictionary
    data = result.to_dict()

    # Update the dictionary with the new quanity and then save the 
    # updated dictionary to Firestore.
    data["qty"] += add_qty
    db.collection("inventory").document(name).set(data)

    # Save this in the log collection in Firestore
    log_transaction(db, f"Added {add_qty} {name}")

def use_inventory(db):
    '''
    Prompt the user to use quantity from an already existing item in the
    inventory database.  An error will be given if the requested amount
    exceeds the quanity in the database.
    '''

    name = input("Item Name: ")
    use_qty = int(input("Use Quantity: "))

    # Check for an already existing item by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("inventory").document(name).get()
    if not result.exists:
        print("Invalid Item Name")
        return

    # Convert data read from the firestore document to a dictionary
    data = result.to_dict()

    # Check for sufficient quantity.
    if use_qty > data["qty"]:
        print(f"Not enough inventory. Only {data['qty']} left.")
        return

    # Update the dictionary with the new quanity and then save the 
    # updated dictionary to Firestore.
    data["qty"] -= use_qty
    db.collection("inventory").document(name).set(data)

    # Save this in the log collection in Firestore
    log_transaction(db, f"Used {use_qty} {name}")

def search_inventory(db):
    '''
    Search the database in multiple ways.
    '''

    print("Select Query")
    print("1) Show All Inventory")        
    print("2) Show Unstocked Inventory")
    print("3) Show Popular Inventory with Low Inventory")
    choice = input("> ")
    print()

    # Build and execute the query based on the request made
    if choice == "1":
        results = db.collection("inventory").get()
    elif choice == "2":
        results = db.collection("inventory").where("qty","==",0).get()
    elif choice == "3":
        results = db.collection("inventory").where("popular","==",True). \
                                             where("qty","<=", 5).get()
    else:
        print("Invalid Selection")
        return
    
    # Display all the results from any of the queries
    print("")
    print("Search Results")
    print(f"{'Name':<20}  {'Price':<10}  {'Popular':<10}  {'Qty':<10}")
    for result in results:
        item = result.to_dict()
        print(f"{result.id:<20}  {item['price']:<10}  {str(item['popular']):<10}  {item['qty']:<10}")
    print()    

def log_transaction(db, message):
    '''
    Save a message with current timestamp to the log collection in the
    Firestore database.
    '''
    data = {"message" : message, "timestamp" : firestore.SERVER_TIMESTAMP}
    db.collection("log").add(data)    

def notify_stock_alert(results, changes, read_time):
    '''
    If the query of out of stock items changes, then display the changes.
    ADDED = New out of stock item added to the list since registration
    MODIFIED = An out of stock item was modified but still out of stock
    REMOVED = An out of stock item is no longer out of stock
    '''

    for change in changes:
        if change.type.name == "ADDED": 
            print()
            print(f"OUT OF STOCK ALERT!! ORDER MORE: {change.document.id}")
            print()
        elif change.type.name == "REMOVED":
            print()
            print(f"ITEM HAS BEEN RE-STOCKED!! READY TO USE: {change.document.id}")
            print()
    
def register_out_of_stock(db):
    '''
    Request a query to be monitored.  If the query changes, then the
    notify_stock_alert will be called.
    '''
    db.collection("inventory").where("qty","==",0).on_snapshot(notify_stock_alert)

def main():
    db = initialize_firestore()
    register_out_of_stock(db)
    choice = None
    while choice != "0":
        print()
        print("0) Exit")
        print("1) Add New Item")
        print("2) Add Quantity")
        print("3) Use Quantity")
        print("4) Search Inventory")
        choice = input(f"> ")
        print()
        if choice == "1":
            add_new_item(db)
        elif choice == "2":
            add_inventory(db)
        elif choice == "3":
            use_inventory(db)
        elif choice == "4":
            search_inventory(db)                        

if __name__ == "__main__":
    main()

