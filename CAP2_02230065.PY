################################
# Jigme Thinley
# 1st year Electrical department
# 02230065
################################
# REFERENCES
# @https://chat.openai.com/
# @https://www.blackbox.ai/

import random #We import random module in order to generate random numbers for Accounts 
import os #we import os module to interact with the operating system

# Base Account class
class Account:
    # Constructor with correct __init__ method
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number #initialize account number 
        self.password = password # Initilaize password
        self.account_type = account_type #initialize account type
        self.balance = balance #initialize account balance, default is 0
    
    # Method to deposit amount
    def deposit(self, amount):
        self.balance += amount  #dipositing amount to the account balance 
        print(f"Deposited Ngultrum{amount}. New balance: Ngultrum{self.balance}") #Generating deposit receipt
    
    # Method to withdraw amount
    def withdraw(self, amount):
        if amount > self.balance: #Verifying if the withdrawal amount exceeds the account balance
            print("Insufficient funds.")#If the withdrawl amount exceeds the account balance 
        else:
            self.balance -= amount #deducting  withdrawal amount from account balance
            print(f"Withdrew Ngultrum{amount}. New balance: Ngultrum{self.balance}") #Generating withdrawl receipt
    
    # Method to check balance
    def check_balance(self):
        return self.balance #Returning the current balance

    # Method to transfer amount to another account
    def transfer(self, amount, recipient_account):
        if amount > self.balance: # verifying if transfer amount exceeds account balance
            print("Insufficient funds.")# if the transfer amount exceeds the account balance
        else:
            self.withdraw(amount) #Withdrawing the amount from current account
            recipient_account.deposit(amount) #Depositing the amount into recipient's account
            print(f"Transferred Ngultrum{amount} to account {recipient_account.account_number}")#Generating transfer receipt

    # Method to change account number
    def change_account_number(self, new_account_number):
        self.account_number = new_account_number # updating account number 

    # Method to change password
    def change_password(self, new_password):
        self.password = new_password # updating account password

# BusinessAccount class inheriting from Account
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0, business_name=""):
        super().__init__(account_number, password, "Business", balance) # Initialize the base Account class
        self.business_name = business_name #initialize business name

# PersonalAccount class inheriting from Account
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0, owner_name=""):
        super().__init__(account_number, password, "Personal", balance) # Initialize the base Account class
        self.owner_name = owner_name #initialize account holders name 

# Function to save accounts to a file
def save_account(account):
    accounts = load_accounts() # Load existing accounts from file
    accounts[account.account_number] = account # Update or add the account
    with open('accounts.txt', 'w') as f: ## Opening accounts file in write mode
        for acc in accounts.values():# Iterating through all accounts using for loop
            f.write(f"{acc.account_number},{acc.password},{acc.account_type},Ngultrum {acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  # Writing account details to file

# Function to load accounts from a file
def load_accounts():
    accounts = {}  # Initialize empty dictionary to store accounts
    if os.path.exists('accounts.txt'):  # verifying whether the accounts file exists
        with open('accounts.txt', 'r') as f: # Opening accounts file in read mode
            for line in f: # Iterating through each line in the file
                parts = line.strip().split(',')  # Splitting line
                account_number, password, account_type, balance = parts[:4]  # Retrieving account details
                balance = float(balance.split()[1]) # Converting account balance back to float after removing the prefix 'Ngultrum' 
                if account_type == "Business":  # verifying if account is a business account
                    business_name = parts[4] # Retrieving business name
                    accounts[account_number] = BusinessAccount(account_number, password, balance, business_name) # Creating BusinessAccount object
                elif account_type == "Personal":  # verifying if account type is personal account
                    owner_name = parts[5] #Retrieving owner's name
                    accounts[account_number] = PersonalAccount(account_number, password, balance, owner_name)  # Creating PersonalAccount object
    return accounts # return accounts dictionary

# Function to create a new account
def create_account():
    account_number = str(random.randint(100000000, 999999999))# Generating a random 9-digit account number
    password = str(random.randint(1000, 9999)) # Generating a random 4-digit password
    account_type = input("Enter account type (Business/Personal): ")# Prompt user to enter account type
    
    if account_type == "Business":  # verifying if account type is business
        business_name = input("Enter business name: ")  # Prompt user to enter business name
        account = BusinessAccount(account_number, password, business_name=business_name)# Creating BusinessAccount object
    else: #if account type is personal
        owner_name = input("Enter holder name: ") # Prompt user to enter account owner's name 
        account = PersonalAccount(account_number, password, owner_name=owner_name)  # Creating PersonalAccount object

    save_account(account) # to save the new account to file
    print(f"Account created! Your account number is {account_number} and password is {password}")  # generating  account creation receipt

# Function to login to an account
def login(accounts):
    account_number = input("Enter account number: ") #prompt user to enter account number 
    password = input("Enter password: ") #prompt user to enter account password
    
    account = accounts.get(account_number)  # to retrieve account from accounts dictionary
    if account and account.password == password: # verifying whether account exists and if the password is correct
        print(f"Welcome, {account.account_type} account holder!") # to print the welcome message
        return account  # Returning the logged-in account
    else: # if account does not exists or if the password entered is incorrect
        print("Invalid account number or password.") # Printing error message for invalid login
        return None # returning None for invalid login

# Function to delete an account
def delete_account(account):
    accounts = load_accounts() # to load existing accounts from file
    if account.account_number in accounts:  # to check whether account exists
        del accounts[account.account_number] # To delete the account from dictionary
        with open('accounts.txt', 'w') as f: # Opening accounts file in write mode
            for acc in accounts.values(): # Iterating through all remaining accounts
                f.write(f"{acc.account_number},{acc.password},{acc.account_type},{acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  # Writing account details to file
        print("Account deleted successfully.")  # generating account deletion receipt
    else:
        print("Account not found.")

# Function to change account details
def change_account_details(account):
    print("\n1. Change Account Number\n2. Change Password") # generating options to change the account details
    choice = input("Enter choice: ") #prompt user to enter their choice
    
    if choice == '1': #to change account number 
        new_account_number = input("Enter new account number: ") #prompt user to enter new account number 
        accounts = load_accounts() # to load existing accounts from file
        if new_account_number in accounts: # verifying if new account number already exists or not 
            print("Account number already exists.") #if the account number already exists 
        else:
            old_account_number = account.account_number  # to store old account number
            account.change_account_number(new_account_number) # to change account numbers
            save_account(account) # Saving account with new account number
            # To delete old account
            if old_account_number in accounts:
                del accounts[old_account_number] # to delete old account from dictionary
                with open('accounts.txt', 'w') as f:  # Opening accounts file in write mode
                    for acc in accounts.values(): # Iterating through remaining accounts
                        f.write(f"{acc.account_number},{acc.password},{acc.account_type},{acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  # Writing account details to file
            print("Account number changed successfully.") # Printing confirmation message
    elif choice == '2': #  to change account password
        new_password = input("Enter new password: ") #prompt the user to enter new password
        account.change_password(new_password) # to change account password
        save_account(account) # Saving account with new password
        print("Password changed successfully.") # Printing confirmation message
    else:
        print("Invalid choice.")

# Main function
def main():
    while True: #infinite loop
        print("\n1. Create Account\n2. Login\n3. Exit") # Generating options 
        choice = input("Enter choice: ") #prompt user to enter their choice 
        
        if choice == '1': # to create account 
            create_account() # Calling create_account function
        elif choice == '2': # To login
            accounts = load_accounts()  # Loading existing accounts
            account = login(accounts)  # Logging in
            if account: # verifying whether the login was successful
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transfer\n5. Delete Account\n6. Change Account Details\n7. Logout") # Printing options
                    trans_choice = input("Enter choice: ") #prompt user to enter their choice 
                    
                    if trans_choice == '1': # to deposit the amount
                        amount = float(input("Enter amount to deposit: ")) #prompt the user to enter the amount to deposit
                        account.deposit(amount) # Depositing amount
                        save_account(account)# Saving updated account details
                    elif trans_choice == '2': #to withdraw
                        amount = float(input("Enter amount to withdraw: "))#prompt the user to enter the amount to withdraw
                        account.withdraw(amount) # withdrawing amount
                        save_account(account)# Saving updated account details
                    elif trans_choice == '3': #to check account balance 
                        print(f"Balance: Ngultrum {account.check_balance()}") # Printing current balance
                    elif trans_choice == '4': #to transfer the amount 
                        recipient_number = input("Enter recipient account number: ") #prompt the user to enter the recipent account number 
                        recipient = accounts.get(recipient_number)  # Getting recipient account
                        if recipient: # verifying if recipient account exists
                            amount = float(input("Enter amount to transfer: ")) #prompt the user to enter the amount to transfer
                            account.transfer(amount, recipient)  #transfering amount 
                            save_account(account)# Saving sender's updated account details
                            save_account(recipient) # Saving recipient's updated account details
                        else:
                            print("Recipient account does not exist.")
                    elif trans_choice == '5': #to delete account
                        delete_account(account)
                        break #exiting loop
                    elif trans_choice == '6':#to change account details 
                        change_account_details(account)
                    elif trans_choice == '7': # to logout 
                        save_account(account) # saving account details 
                        print("Logged out.")
                        break #exiting loop
        elif choice == '3': #to exit the program
            print("Thank You!")
            break #exiting loop
        else:
            print("Invalid choice. Try again.")

# Ensures the main function runs when the script is executed
if __name__ == "__main__":
    main() #calling main function
