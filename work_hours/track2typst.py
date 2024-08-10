import os
from datetime import datetime

FILE_NAME = 'work_hours.typ'
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

def generate_typst_file():
    """Generate a Typst file from the data in the temp file."""
    if not os.path.exists(TEMP_FILE_NAME):
        print("No tasks recorded yet.")
        return

    with open(TEMP_FILE_NAME, 'r') as file:
        tasks = file.readlines()
    
    with open(FILE_NAME, 'w') as file:
        file.write('#set page (columns:3)\n')
        file.write('#set text(font: "Lato",\n')
        file.write('size:10pt)\n')
        file.write('=== Work hours!\n')
        file.write('#table(\n')
        file.write('columns: 3,\n')
        file.write('align: (left, center, right),\n')
        file.write('inset: 5pt,\n')
        file.write('[*dag*], [*timmar*], [*akkum*],\n')
          
        for task in tasks:
            date, hours_worked, total_hours = task.strip().split(',')
            file.write(f'[ {date}],[{hours_worked}],[{total_hours}],\n')
        file.write(')')

        total_hours = float(total_hours.strip())
        file.write(f'\n\ntotalt 2024: *{total_hours:.2f}* timmar\n')

    print(f"Typst file generated: {FILE_NAME}")

def view_tasks():
    """Display all recorded tasks and generate Typst file."""
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
    generate_typst_file()
    return total_hours

def main():
    # Initialize total hours from file
    total_hours = 0.0
    if os.path.exists(TEMP_FILE_NAME):
        total_hours = view_tasks()

    while True:
        print("\nWork Hours Tracker - Add a New Task")
        total_hours = add_task(total_hours)

        print("\nChoose an option:")
        print("1. Add another task")
        print("2. View all tasks and generate Typst file")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            continue
        elif choice == '2':
            total_hours = view_tasks()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    main()
