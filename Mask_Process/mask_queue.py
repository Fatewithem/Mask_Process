from queue import PriorityQueue

def priority():
    q = PriorityQueue()

    while not q.empty():
        next_item = q.get()
        print(next_item)
