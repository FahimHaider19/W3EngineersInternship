
#Task-3: create 10 lists, insert them into a set. If a list is duplicate in the set, print a message
import random

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