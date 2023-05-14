import queue

q = queue.Queue()
q.put('a')
q.put('b')
q.put('c')
q.put('d')

print(f'{q.get()}')
print(f'{q.get()}')
print(f'{q.get()}')
print(f'{q.get()}')

print('all items removed')
print(f'{q.get()}')
print('done')