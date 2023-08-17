import random

#Task-1: print 1-10
for i in range(1,11):
    print(i, end=" ")

print()
print()


#Task-2: print a dictionary as key=>value format
cities = {
    'New York': 'United States',
    'Paris': 'France',
    'Tokyo': 'Japan',
    'Sydney': 'Australia',
    'London': 'United Kingdom',
    'Rome': 'Italy',
    'Cairo': 'Egypt',
    'Rio de Janeiro': 'Brazil',
    'Beijing': 'China',
    'Moscow': 'Russia'
}

for key, value in cities.items():
    print(key + ' => ' + value)
    
print()
print()



#Task-3: create 10 lists, insert them into a set. If a list is duplicate in the set, print a message
list = []
SET = set()
for i in range(10):
    list.append([random.randint(0, 40) for _ in range(random.randint(5, 10))])
    # list.append([1,2,3])
    print(f"List{i+1}=> ", list[i])

for i in range(10):
    t=tuple(list[i])
    if t in SET:
        print(t, end=" ")
        print('exists more than 1 time')
    else:
        SET.add(tuple(list[i]))        

print("SET=>",SET)
print()
print()



#Task-4: Define a function that takes indefinite number of input and assigns them to a tuple and dictionary according to their type
#        Then print values from the tuple and dictinary parallelly
def merge(*tpl, **dct) : 
    for l, d in zip(tpl, dct) : 
        print(l, "=>", dct[d])

merge("x", "y", a="A", b="B", c="C")

