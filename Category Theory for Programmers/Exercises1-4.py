# 1. Implement, as best as you can, the identity function in your favorite language
def id(func):
    return func

def hello_world():
    return "hello world"

# 2. Implement the composition function in your favorite language. It takes two functions as arguments and returns a function that is their composition.

def compose(func1, func2):
    return func1(func2)

print(id(13))
print(compose(id, hello_world))