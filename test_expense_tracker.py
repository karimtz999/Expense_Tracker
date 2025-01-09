import subprocess

def run_command(command):
    """
    Helper function to run a shell command and return its output.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Test adding an expense
def test_add_expense():
    print("Testing: Add Expense")
    output = run_command('python expense_tracker.py add --description "Test Lunch" --amount 15.5 --category "Food"')
    assert "Expense added successfully" in output
    print(output)

# Test listing expenses
def test_list_expenses():
    print("Testing: List Expenses")
    output = run_command('python expense_tracker.py list')
    assert "Test Lunch" in output
    print(output)

# Test setting a budget
def test_set_budget():
    print("Testing: Set Budget")
    output = run_command('python expense_tracker.py set-budget --month 1 --amount 100')
    assert "Budget set for month 1" in output
    print(output)

# Test showing summary (without exceeding budget)
def test_summary_within_budget():
    print("Testing: Summary Within Budget")
    output = run_command('python expense_tracker.py summary --month 1')
    assert "Total expenses for month 1" in output
    assert "Warning" not in output
    print(output)

# Test summary (exceeding budget)
def test_summary_exceeding_budget():
    print("Testing: Summary Exceeding Budget")
    run_command('python expense_tracker.py add --description "Expensive Dinner" --amount 120 --category "Food"')
    output = run_command('python expense_tracker.py summary --month 1')
    assert "Warning" in output
    print(output)

# Main test runner
if __name__ == "__main__":
    print("Running Expense Tracker Tests...\n")
    test_add_expense()
    test_list_expenses()
    test_set_budget()
    test_summary_within_budget()
    test_summary_exceeding_budget()
    print("\nAll tests passed!")
