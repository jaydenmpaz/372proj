# Function definitions
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    return a / b

def is_even(val):
    if val % 2 == 0:
        return True
    else:
        return False

# Main function
def main():
    # Variable assignment and print
    prompt = "Hello, please enter 2 digits!"
    print(prompt)
    
    # Get numerical values from user input
    x = int(input())
    y = int(input())

    # Comparison expressions
    if x < y:
        print(x, "is less than", y)
    
    if x > y:
        print(x, "is greater than", y)
    
    if x == y:
        print(x, "is equal to", y)

    # Check if the numbers are even or odd
    if is_even(x):
        print(x, "is even")
    else:
        print(x, "is odd")

    if is_even(y):
        print(y, "is even")
    else:
        print(y, "is odd")

    # Calculate with all arithmetic operators
    sum_result = add(x, y)
    diff_result = sub(x, y)
    prod_result = mult(x, y)
    quot_result = div(x, y)

    # Print results
    print("Sum of", x, "and", y, "is", sum_result)
    print("Difference between", x, "and", y, "is", diff_result)
    print("Product of", x, "and", y, "is", prod_result)
    print("Quotient of", x, "and", y, "is", quot_result)

    return "Done!"

# Execute the main function
if __name__ == "__main__":
    main()
