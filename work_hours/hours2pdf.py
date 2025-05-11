import os
import subprocess
from datetime import datetime

# Define the work_hours directory in the user's home directory
HOME_DIR = os.path.expanduser('~')
WORK_HOURS_DIR = os.path.join(HOME_DIR, '.tmp_directory')

# Ensure the work_hours directory exists
os.makedirs(WORK_HOURS_DIR, exist_ok=True)

# Define file paths
FILE_NAME = os.path.join(WORK_HOURS_DIR, 'hours_2025.typ')
TEMP_FILE_NAME = os.path.join(WORK_HOURS_DIR, 'tmp_2025.txt')
PDF_OUTPUT_PATH = os.path.join(HOME_DIR, 'output/out_pdf.pdf')

def compile_typst():
    """Compile the Typst file into a PDF."""
    try:
        # Run the Typst compilation command
        subprocess.run(
            ['typst', 'compile', FILE_NAME, PDF_OUTPUT_PATH],
            check=True
        )
        print(f"PDF compiled successfully: {PDF_OUTPUT_PATH}")
    except FileNotFoundError:
        print("Typst is not installed or not in PATH. Ensure Typst is installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Typst compilation: {e}")

def add_task(_):
    """Add a new work task and update total hours."""
    total_hours = 0.0

    # Read the last total from the file, if it exists
    if os.path.exists(TEMP_FILE_NAME):
        with open(TEMP_FILE_NAME, 'r') as file:
            lines = file.readlines()
            if lines:
                try:
                    *_, last_total = lines[-1].strip().split(',')
                    total_hours = float(last_total)
                except ValueError:
                    print("Error parsing last total from file. Starting from 0.")

    date = input("Enter the date (MM-DD): ")
    try:
        datetime.strptime(date, '%m-%d')
    except ValueError:
        print("Invalid date format. Please try again.")
        return total_hours

    hours_input = input("Enter the number of hours worked (can be negative): ")
    hours_input = hours_input.replace(',', '.')
    try:
        hours_worked = float(hours_input)
    except ValueError:
        print("Invalid input for hours. Please enter a valid number.")
        return total_hours

    total_hours += hours_worked

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
        file.write('#set text(font: "Free Sans", size:10pt)\n')
        file.write('=== 2025\n')
        file.write('#table(\n')
        file.write('columns: 3,\n')
        file.write('stroke:none,\n')
        file.write('align: (left, center, right),\n')
        file.write('inset: 5pt,\n')
        file.write('[*dag*], [*timmar*], [*akkum*],\n')

        for task in tasks:
            date, hours_worked, total_hours = task.strip().split(',')
            file.write(f'[ {date} ],[ {hours_worked} ],[ {total_hours} ],\n')
        file.write(')')

        # Assuming the last total_hours is the cumulative total
        total_hours = float(total_hours.strip())
        file.write(f'\n\ntotalt 2025: *{total_hours:.2f}* timmar\n')

    print(f"Typst file generated: {FILE_NAME}")
    compile_typst()

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

        # Get the last total_hours from the last task
        last_task = tasks[-1]
        _, _, total_hours = last_task.strip().split(',')

    print(f"\nCurrent Total Hours Worked: {float(total_hours):.2f}")
    generate_typst_file()
    return float(total_hours)

def main():
    total_hours = 0.0  # Initialize total hours

    while True:
        print("\nChoose an option:")
        print("1. Add a new task")
        print("2. View all tasks and generate Typst file")
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
