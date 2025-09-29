def calculate(num1, operator, num2):
    if operator == '+':
        return num1 + num2
    elif operator == "-":
        return num1 - num2 
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        return num1 / num2
    else: 
        return "invalid operator"
print(calculate(10, "+", 90))
print(calculate(20, "/", 30))
#niceu!