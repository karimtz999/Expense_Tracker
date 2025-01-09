import argparse
import json
from datetime import datetime
import os

DATA_FILE = "expenses.json"

# Load expenses from file
def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Save expenses to file
def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

# Add an expense
def add_expense(description, amount, category=None):
    expenses = load_expenses()
    new_id = 1 if not expenses else expenses[-1]["id"] + 1
    expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": float(amount),
        "category": category or "Uncategorized",
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")

# Update an expense
def update_expense(expense_id, description=None, amount=None, category=None):
    expenses = load_expenses()
    for expense in expenses:
        if expense["id"] == expense_id:
            if description:
                expense["description"] = description
            if amount:
                expense["amount"] = float(amount)
            if category:
                expense["category"] = category
            save_expenses(expenses)
            print(f"Expense updated successfully (ID: {expense_id})")
            return
    print(f"Expense with ID {expense_id} not found.")

# Delete an expense
def delete_expense(expense_id):
    expenses = load_expenses()
    expenses = [e for e in expenses if e["id"] != expense_id]
    save_expenses(expenses)
    print(f"Expense deleted successfully")

# List all expenses
def list_expenses():
    expenses = load_expenses()
    print(f"{'ID':<4} {'Date':<12} {'Description':<20} {'Amount':<10} {'Category':<15}")
    for e in expenses:
        print(f"{e['id']:<4} {e['date']:<12} {e['description']:<20} ${e['amount']:<10.2f} {e['category']:<15}")

# Show expense summary
def show_summary(month=None):
    expenses = load_expenses()
    total = 0
    filtered_expenses = expenses
    if month:
        filtered_expenses = [e for e in expenses if datetime.strptime(e["date"], "%Y-%m-%d").month == month]
    total = sum(e["amount"] for e in filtered_expenses)
    if month:
        print(f"Total expenses for month {month}: ${total:.2f}")
    else:
        print(f"Total expenses: ${total:.2f}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Add expense
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("--description", required=True)
    parser_add.add_argument("--amount", type=float, required=True)
    parser_add.add_argument("--category")

    # Update expense
    parser_update = subparsers.add_parser("update")
    parser_update.add_argument("--id", type=int, required=True)
    parser_update.add_argument("--description")
    parser_update.add_argument("--amount", type=float)
    parser_update.add_argument("--category")

    # Delete expense
    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("--id", type=int, required=True)

    # List expenses
    subparsers.add_parser("list")

    # Summary
    parser_summary = subparsers.add_parser("summary")
    parser_summary.add_argument("--month", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount, args.category)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount, args.category)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        show_summary(args.month)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
