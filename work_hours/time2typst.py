import os

FILE_NAME = 'work_hours.typ'
TEMP_FILE_NAME = 'temp_work_hours.txt'

def generate_typst_file():
    """Generate a Typst file from the data in the temp file."""
    if not os.path.exists(TEMP_FILE_NAME):
        print("No tasks recorded yet.")
        return

    with open(TEMP_FILE_NAME, 'r') as file:
        tasks = file.readlines()
    
    if not tasks:
        print("No tasks recorded yet.")
        return

    with open(FILE_NAME, 'w') as file:
        # Typst file header
        file.write('#set page (columns:3)\n')
        file.write('#set text(font: "Lato",\n')
        file.write('size:10pt)\n')
        file.write('=== Work hours!\n')
        file.write('#table(\n')
        file.write('columns: 3,\n')
        file.write('align: (left, center, right),\n')
        file.write('inset: 5pt,\n')
        file.write('[*dag*], [*timmar*], [*akkum*],\n')
          
        # Write task entries
        for task in tasks:
            date, hours_worked, total_hours = task.strip().split(',')
            file.write(f'[ {date}],[{hours_worked}],[{total_hours}],\n')
        file.write(')')

        # Write total hours
        total_hours = float(total_hours.strip())
        file.write(f'\n\ntotalt 2024: *{total_hours:.2f}* timmar\n')

    print(f"Typst file generated: {FILE_NAME}")

def main():
    generate_typst_file()

if __name__ == '__main__':
    main()
