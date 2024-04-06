import math

def parabola(base):
    return pow(base, 2)

def exponential(power):
    return pow(math.e, power)

def integral(a, b, steps, func):                    # a and b are lower and upper bounds, respectively; steps is number of samples; func is a function passed as a parameter
    dx = (b - a) / steps                            # change in x
    x_vals = [a + (i * dx) for i in range(steps)]   # x values used by function
    total = 0

    for i, val in enumerate(x_vals):
        total = total + (func(val) * dx)            # evaluates func at every x_val[i] and multiplies it by dx, finally summing. this gives us the riemann sum for the function.
    return total

def derivative(x, func):                 # x is point where we take derivative, func is our function -- correct to about 5 decimals
    return  (func(x + math.pow(10, -10)) - func(x)) / math.pow(10, -10)

print(integral(1, 4, 100000, parabola))
print(integral(0, math.e, 100000, exponential)) 

print()
print(derivative(math.e, parabola))