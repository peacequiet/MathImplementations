# By considering the terms in the Fibonacci sequence whose values do not exceed four million, find the sum of the even-valued terms.

# def fibonacci_sum():
#     current = 0
#     array
#     while current < 4000000:

# TODO: debug
# def iter_fib(num):
#     count = 1
#     current = None
#     prev = None
#     sum = 0
#     while count != num:
#         if count == 1:
#             current = 1
#             prev = None
#             sum += current
#         elif count == 2:
#             current = 2
#             prev = 1
#             sum += current
#         else:
#             prev, current = current, current + prev
#             sum += current
#         count += 1
#     return sum

def fibonacci(num):
    if num == 1:
        return 1
    if num == 2:
        return 2
    else:
        return fibonacci(num - 1) + fibonacci(num - 2)

print(fibonacci(3))