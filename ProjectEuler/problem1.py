# find sum of all multiples of 3 or 5 below 1000

def sum_three_five():
    sum = 0
    for i in range(1000):
        if i % 3 == 0 or i % 5 == 0:
            sum = sum + i
    
    return sum

def sum_three_five_recursive(num, sum):
    if num == 0:
        return sum
    elif num % 3 == 0 or num % 5 == 0:
        return sum_three_five_recursive(num - 1, sum + num)
    else:
        return sum_three_five_recursive(num - 1, sum)


print(sum_three_five_recursive(99, 0))