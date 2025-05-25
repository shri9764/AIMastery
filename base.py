def calculate_fact(num):
    if num == 0 or num ==1:
        return 1
    else:
        return num * calculate_fact(num -1)
    
print(calculate_fact(5))