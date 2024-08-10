import os
from datetime import datetime

TEMP_FILE_NAME = 'temp_work_hours.txt'

def add_task(total_hours):
    """Add a new work task and update total hours."""
    date = input("Enter the date (MM-DD): ")
    try:
        # Validate date format
        datetime.strptime(date, '%m-%d')
    except ValueError:
        print("Invalid date format. Please try again.")
        return total_hours
    
    try:
        hours_worked = float(input("Enter the number of hours worked (can be negative): "))
    except ValueError:
        print("Invalid input for hours. Please enter a valid number.")
        return total_hours

    total_hours += hours_worked

    # Append new entry to temp file
    with open(TEMP_FILE_NAME, 'a') as file:
        line = f"{date},{hours_worked},{total_hours}\n"
        file.write(line)
    print("Task added successfully!")
    return total_hours

def view_tasks():
    """Display all recorded tasks."""
    if not os.path.exists(TEMP_FILE_NAME):
        print("No tasks recorded yet.")
        return 0.0

    total_hours = 0.0

    with open(TEMP_FILE_NAME, 'r') as file:
        tasks = file.readlines()
        if not tasks:
            print("No tasks recorded yet.")
            return 0.0

        print("\nRecorded Tasks:")
        for i, task in enumerate(tasks, 1):
            date, hours_worked, total = task.strip().split(',')
            print(f"{i}. Date: {date}, Hours: {hours_worked}, Total: {total}")

        total_hours = float(total.strip())

    print(f"\nCurrent Total Hours Worked: {total_hours:.2f}")
    return total_hours

def main():
    # Initialize total hours from file
    total_hours = 0.0
    if os.path.exists(TEMP_FILE_NAME):
        total_hours = view_tasks()

    # Prompt to add a new task on first run
    total_hours = add_task(total_hours)

    while True:
        print("\nChoose an option:")
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            total_hours = add_task(total_hours)
        elif choice == '2':
            total_hours = view_tasks()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    main()
