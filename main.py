import calendar
from datetime import datetime
from pathlib import Path


#GET VALID YEAR 
def get_valid_year() -> int:
    while True:
        try :
            year = int(input("Enter Year (e.g., 2026): ").strip())
            if(year>0) :
                return year
            print("⚠️Please Enter Positive year")
        except ValueError:
            print("⚠️Invalid Input, Please Enter Valid Year Number")

#GET VALID MONTH
def get_valid_month() -> int:
    while True:
        try : 
            month = int((input("Enter Month(1-12): ")).strip())
            if (1 <= month <=12):
                return month
            print("⚠️ Enter Month number,It must be in between 1 to 12")
        except ValueError:
            print("⚠️ Invalid Input, Please Enter Valid Month Number")

#GET VALID DATE
def get_valid_date() -> str:
    while True:
        try:
            date_str = input("Enter Date(dd-mm-yyyy):").strip()
            datetime.strptime(date_str, "%d-%m-%Y")
            return date_str
        except ValueError:
            print("⚠️ Invalid format, Use dd-mm-yyyy (e.g 02-06-2026)")

#VIEW FULL CALENDAR OR SPECIFIC MONTH
def view_calendar(year: int,month : int | None = None):
    if (month == None):
        print(f"\n--- Calendar for {year} ---")
        print(calendar.calendar(year))
    else :
        print(f"\n{calendar.month(year,month)}")

#ADD REMINDER
def add_reminder(file_path : Path):
    date_str = get_valid_date()
    Event = (input("Enter Event Discription: ")).strip()
    if (Event == ""):
        print("⚠️ Event discription cannot be empty")
    else :
        try:
            with file_path.open("a" , encoding="utf-8") as MY_File:
                MY_File.write(f"{date_str} | {Event}")
                print("Reminder is successfully Updated")
        except IOError:
            print("⚠️  Failed to save reminder")

#VIEW REMINDER
def view_reminder(file_path : Path)->None:
    reminders = read_reminder(file_path)
    if reminders == []:
        print("\n No reminders found!")
    else:
        print("\n--- All Reminders ---")
        print(reminders)

#READ REMINDER
def read_reminder(file_path: Path) -> list[str]:
    """Read reminders from file."""
    if not file_path.exists():
        return []
    try:
        return [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except IOError:
        print("⚠️ Error reading reminders file.")
        return []
    
#DELETE REMINDER
def delete_reminder(file_path : Path):
    reminders = read_reminder(file_path)
    if reminders == []:
        print("\nNo reminders to delete!")
        return
    else:
        print("\n--- Select Reminder to Delete ---")
        for i, r in enumerate(reminders, 1):
            print(f"{i}. {r}")
    
    try:
        num = int(input("\nEnter number to delete: ").strip())
        match num:
            case n if 1 <= n <= len(reminders):
                removed = reminders.pop(n - 1)
                if write_reminders(file_path, reminders):
                    print(f"🗑️ Deleted: {removed}")
            case _:
                print("⚠️ Invalid number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")


def write_reminders(file_path: Path, reminders: list[str]) -> bool:
    """Write reminders to file."""
    try:
        file_path.write_text("\n".join(reminders) + "\n" if reminders else "", encoding="utf-8")
        return True
    except IOError:
        print("⚠️ Error writing to reminders file.")
        return False

    
def main() -> None:
    """Main application loop."""
    file_path = Path("reminders.txt")
    year = get_valid_year()
    view_calendar(year)
    
    menu = f"""
===== Calendar & Reminder App ({year}) =====
1. View Month
2. Add Reminder
3. View All Reminders
4. Delete Reminder
5. Full Year Calendar
6. Exit"""

    while True:
        print(menu)
        choice = input("Choose (1-6): ").strip()
        
        match choice:
            case "1":
                view_calendar(year, get_valid_month())
            case "2":
                add_reminder(file_path)
            case "3":
                view_reminder(file_path)
            case "4":
                delete_reminder(file_path)
            case "5":
                view_calendar(year)
            case "6":
                print("👋 Goodbye!")
                break
            case _:
                print("⚠️ Invalid choice! Select 1-6.")


if __name__ == "__main__":
    main()