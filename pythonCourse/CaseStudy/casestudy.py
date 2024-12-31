import threading
import time
import csv
from threading import Lock
class Customer:
    def __init__(self, customer_id, name, account_balance, account_type):
        self.customer_id = customer_id
        self.name = name
        self.account_balance = float(account_balance)
        self.account_type = account_type
        self.transaction_history = []
        self.lock = Lock()
    def deposit(self, amount):
        with self.lock:
            if amount > 0:
                self.account_balance += amount
                self.transaction_history.append(f"Deposited {amount}")
                print(f"Deposit successful. New balance: {self.account_balance}")
                self.apply_interest()
                print(f"Interest applied. New balance: {self.account_balance}")
            else:
                print("Deposit amount must be positive.")
    def withdraw(self, amount):
        with self.lock:
            if amount <= 0:
                print("Withdrawal amount must be positive.")
            elif amount > self.account_balance:
                print("Insufficient funds.")
            else:
                self.account_balance -= amount
                self.transaction_history.append(f"Withdrew {amount}")
                print(f"Withdrawal successful. New balance: {self.account_balance}")
    def view_transactions(self):
        print(f"Transaction history for {self.name}:")
        for transaction in self.transaction_history:
            print(transaction)
    def apply_interest(self):
        if self.account_type == "Savings":
            interest = self.account_balance * 0.05
            self.account_balance += interest
            #self.transaction_history.append(f"Interest Applied: {interest}")
def read_customers_from_file(file_name):
    customers = []
    try:
        with open(file_name, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                customer = Customer(customer_id=row[0], name=row[1], account_balance=row[2], account_type=row[3])
                customers.append(customer)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found. Please check the file path and try again.")
    except Exception as e:
        print(f"Error reading file: {e}")
    return customers
def display_menu():
    print("\nBanking System Menu:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. View Transaction History")
    print("4. Exit")
def periodic_interest_application(customers):
        while True:
           time.sleep(10)
           for customer in customers:
              customer.apply_interest()
def banking_system():
    customers = read_customers_from_file('C:/Users/KONDRUTHANMAI/Documents/GitHub/pythoncourse/pythonCourse/casestudy/data.csv')
    interest_thread = threading.Thread(target=periodic_interest_application, args=(customers,))
    interest_thread.daemon = True
    interest_thread.start()
    customer_id = input("Enter your customer ID: ")
    selected_customer = None
    for customer in customers:
        if customer.customer_id == customer_id:
            selected_customer = customer
            break
    if selected_customer is None:
        print("Customer ID not found.")
        return
    while True:
        display_menu()
        choice = input("Choose an option (1-4): ")
        if choice == '1':
            amount = float(input("Enter deposit amount: "))
            selected_customer.deposit(amount)
        elif choice == '2':
            amount = float(input("Enter withdrawal amount: "))
            selected_customer.withdraw(amount)
        elif choice == '3':
            selected_customer.view_transactions()
        elif choice == '4':
            print("Exiting Banking System.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
if __name__ == "__main__":
    banking_system()