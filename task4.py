#Task-4: Define a function that takes indefinite number of input and assigns them to a tuple and dictionary according to their type
#        Then print values from the tuple and dictinary parallelly
def merge(*tpl, **dct) : 
    for l, d in zip(tpl, dct) : 
        print(l, "=>", dct[d])

merge("x", "y", a="A", b="B", c="C")