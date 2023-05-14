

def myfunc(i):
    i = 4
    print(f'func:   {id(i)}')
    print(f'func:   {i=}')

x = 0
#print(f'before: {id(x)}')
#print(f'before: {x=}')

#myfunc(x)
#print(f'after:  {id(x)}')
#print(f'after:  {x=}')

def func1(l):
    l.append(2)
    print(f'func:   {id(l)}')
    print(f'func:   {l=}')

mylist = []
mylist.append(1)
print(f'before: {id(mylist)}')
print(f'before: {mylist=}')
func1(mylist)
print(f'after:  {id(mylist)}')
print(f'after:  {mylist=}')
