def return_mod(num, mod, pow):
    return (num ** pow) % mod

def modulo_function(num, mod, pow):
    for i in range(pow):
        print(str(num) + " ^ " + str(i) + " mod " + str(mod) + ": " + str(return_mod(num, mod, i)))
    print()

modulo_function(2, 17, 20)
modulo_function(3, 17, 20)
modulo_function(5, 17, 20)