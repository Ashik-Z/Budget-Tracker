from expense import Expense
import calendar
import datetime


def main():
    print("Welcome To The Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = max(0, float(input("Enter your budget for this month: ")))
    print(f"Your budget is set to ${budget:.2f}")


    # get user input for expense
    expense = get_user_expense()
    # print(f"User Entered Expense: {expense}")


    # write their expense to a file
    save_expense_to_file(expense, expense_file_path)


    # read file and summarize expenses
    summarize_expense(expense_file_path, budget)


def get_user_expense():
    print(f"Getting User Expense")
    expense_name = input("Enter the expense name: ")
    expense_amount = float(input("Enter the expense amount: "))
    expense_categories = [
        "Food(s)/Drink(s)",
        "Home",
        "Work",
        "Fun",
        "Healthcare",
        "Other"
    ]

    while True:
        print("Select a category: ")
        for i, category in enumerate(expense_categories):
            print(f"  {i+1}. {category}")
            
        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter the number corresponding to the category {value_range}: ")) - 1

        if selected_index in range(0, len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print(f"Invalid category. Please try again.")


        # break


def save_expense_to_file(expense: Expense, expense_file_path: str):
    print(f"Saving User Expense {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.category}, {expense.amount}\n")


def summarize_expense(expense_file_path: str, budget: float):
    print(f"Summarizing User Expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_category, expense_amount = line.strip().split(", ")
            line_expense = Expense(
                name=expense_name, category=expense_category, amount=float(expense_amount)
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key not in amount_by_category:
            amount_by_category[key] = 0.0
        amount_by_category[key] += expense.amount
    
    for category, total_amount in amount_by_category.items():
        print(f"  {category}: ${total_amount:.2f}")

    total_spent = sum([ex.amount for ex in expenses])
    print(f"Total Spent: ${total_spent:.2f}")
    if total_spent > budget:
        print(f"You are over budget by ${total_spent - budget:.2f}.")
    else:
        print(f"You are within budget by ${budget - total_spent:.2f}.")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    days_left = days_in_month - now.day

    daily_budget = (budget - total_spent) / days_left
    print(f"You can spend up to ${daily_budget:.2f} per day for the rest of the month.")



if __name__ == "__main__":
    main()