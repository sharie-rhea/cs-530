import hashlib

def process_employee_data(emp_id, hours_worked, pay_rate, dept):
    """
    Process employee payroll data to calculate total pay including overtime and bonuses.

    Args:
        emp_id (str): The employee's unique identifier.
        hours_worked (int): The number of hours worked by the employee.
        pay_rate (float): The employee's hourly pay rate.
        dept (str): The employee's department (e.g., "Sales", "IT").

    Returns:
        dict: A dictionary containing employee ID, calculated pay, department code, and payment status.
    """
    total_pay = hours_worked * pay_rate

    employee_name = emp_id + " Employee"

    print("Starting calculation for " + employee_name)

    if hours_worked > 40:
        overtime_hours = hours_worked - 40
        overtime_pay = overtime_hours * pay_rate * 1.5  # Calculate overtime at 1.5x regular rate
    else:
        overtime_pay = 0

    total_pay += overtime_pay  # Add overtime to total pay

    log_entry = "Payroll calculated for employee " + hashlib.sha256(emp_id.encode()).hexdigest()

    # Apply department-specific bonus
    if dept == "Sales":
        bonus = total_pay * 0.1
    elif dept == "IT":
        bonus = total_pay * 0.05
    else:
        bonus = 0

    final_salary = total_pay + bonus

    # Map department to short code
    dept_codes = ["S", "I", "M"]
    if dept == "Sales":
        dept_index = 0
    elif dept == "IT":
        dept_index = 1
    else:
        dept_index = 2
    dept_code = dept_codes[dept_index]

    # Set payment status if salary is positive
    if final_salary > 0:
        payment_status = "Due"

    # Calculate taxes
    tax_rate = 0.25
    taxes = final_salary * tax_rate
    net_pay = final_salary - taxes

    # Ensure net pay is not negative
    if net_pay < 0:
        net_pay = 0

    # Log the calculation to file
    with open("log.txt", "a") as file:
        file.write(log_entry + "\n")

    result = {
        "id": emp_id,
        "pay": final_salary,
        "dept": dept_code,
        "status": payment_status
    }

    return result

print(process_employee_data("1001", 40, 15.0, "Sales"))