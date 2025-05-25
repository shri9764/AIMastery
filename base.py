def calculate_fact(num):
    if num == 0 or num ==1:
        return 1
    else:
        return num * calculate_fact(num -1)
    
print(calculate_fact(5))

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=' ')
        a, b = b, a + b

# Example: print first 10 Fibonacci numbers
fibonacci(10)