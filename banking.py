import random
import re
from datetime import datetime
users = {}
transactions = []
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_contact(contact):
    return re.match(r"^\d{10}$", contact)

def validate_password(password):
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password)

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

# Add user
def add_user():
    name = input("Enter name: ").strip()
    dob = input("Enter DOB (YYYY-MM-DD): ").strip()
    city = input("Enter city: ").strip()
    address = input("Enter address: ").strip()
    contact = input("Enter contact number: ").strip()
    email = input("Enter email ID: ").strip()
    password = input("Enter password: ").strip()
    balance = float(input("Enter initial balance (minimum 2000): ").strip())

    if not validate_email(email):
        print("Invalid email format!")
        return
    if not validate_contact(contact):
        print("Invalid contact number! Must be 10 digits.")
        return
    if not validate_password(password):
        print("Password must be at least 8 characters long with one uppercase letter and one number.")
        return
    if balance < 2000:
        print("Initial balance must be at least 2000.")
        return

    account_number = generate_account_number()
    while account_number in users:
        account_number = generate_account_number()

    users[account_number] = {
        "name": name,
        "dob": dob,
        "city": city,
        "password": password,
        "balance": balance,
        "contact": contact,
        "email": email,
        "address": address,
        "active": True,
    }
    print(f"User added successfully! Account Number: {account_number}")
def show_users():
    if users:
        for account_number, user in users.items():
            print(f"""
            Account Number: {account_number}
            Name: {user['name']}
            DOB: {user['dob']}
            City: {user['city']}
            Balance: {user['balance']}
            Contact: {user['contact']}
            Email: {user['email']}
            Address: {user['address']}
            Active: {'Yes' if user['active'] else 'No'}
            """)
    else:
        print("No users found.")
def login():
    account_number = input("Enter account number: ").strip()
    password = input("Enter password: ").strip()

    user = users.get(account_number)
    if user and user['password'] == password:
        if not user['active']:
            print("Account is deactivated.")
            return
        print(f"Welcome, {user['name']}!")
        while True:
            print("""
            1. Show Balance
            2. Show Transactions
            3. Credit Amount
            4. Debit Amount
            5. Transfer Amount
            6. Activate/Deactivate Account
            7. Change Password
            8. Update Profile
            9. Logout
            """)
            choice = input("Enter choice: ").strip()
            if choice == '1':
                print(f"Your balance is: {user['balance']}")
            elif choice == '2':
                show_transactions(account_number)
            elif choice == '3':
                credit_amount(account_number)
            elif choice == '4':
                debit_amount(account_number)
            elif choice == '5':
                transfer_amount(account_number)
            elif choice == '6':
                toggle_account_status(account_number)
            elif choice == '7':
                change_password(account_number)
            elif choice == '8':
                update_profile(account_number)
            elif choice == '9':
                print("Logged out successfully!")
                break
            else:
                print("Invalid choice!")
    else:
        print("Invalid account number or password.")
def show_transactions(account_number):
    user_transactions = [t for t in transactions if t["account_number"] == account_number]
    if user_transactions:
        for t in user_transactions:
            print(f"{t['type']} of {t['amount']} on {t['date']}")
    else:
        print("No transactions found.")
def credit_amount(account_number):
    amount = float(input("Enter amount to credit: ").strip())
    users[account_number]['balance'] += amount
    transactions.append({"account_number": account_number, "type": "Credit", "amount": amount, "date": datetime.now()})
    print("Amount credited successfully!")
def debit_amount(account_number):
    amount = float(input("Enter amount to debit: ").strip())
    if users[account_number]['balance'] >= amount:
        users[account_number]['balance'] -= amount
        transactions.append({"account_number": account_number, "type": "Debit", "amount": amount, "date": datetime.now()})
        print("Amount debited successfully!")
    else:
        print("Insufficient balance!")

def transfer_amount(account_number):
    target_account = input("Enter target account number: ").strip()
    if target_account not in users:
        print("Target account not found!")
        return
    amount = float(input("Enter amount to transfer: ").strip())
    if users[account_number]['balance'] >= amount:
        users[account_number]['balance'] -= amount
        users[target_account]['balance'] += amount
        transactions.append({"account_number": account_number, "type": "Transfer Out", "amount": amount, "date": datetime.now()})
        transactions.append({"account_number": target_account, "type": "Transfer In", "amount": amount, "date": datetime.now()})
        print("Amount transferred successfully!")
    else:
        print("Insufficient balance!")

def toggle_account_status(account_number):
    users[account_number]['active'] = not users[account_number]['active']
    status = "activated" if users[account_number]['active'] else "deactivated"
    print(f"Account {status} successfully!")
def change_password(account_number):
    new_password = input("Enter new password: ").strip()
    if validate_password(new_password):
        users[account_number]['password'] = new_password
        print("Password changed successfully!")
    else:
        print("Invalid password!")
def update_profile(account_number):
    city = input("Enter new city: ").strip()
    address = input("Enter new address: ").strip()
    contact = input("Enter new contact number: ").strip()
    email = input("Enter new email ID: ").strip()

    if validate_email(email) and validate_contact(contact):
        users[account_number].update({"city": city, "address": address, "contact": contact, "email": email})
        print("Profile updated successfully!")
    else:
        print("Invalid email or contact number!")
def main():
    while True:
        print("""
        Banking System
        1. Add User
        2. Show Users
        3. Login
        4. Exit
        """)
        choice = input("Enter choice: ").strip()
        if choice == '1':
            add_user()
        elif choice == '2':
            show_users()
        elif choice == '3':
            login()
        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
