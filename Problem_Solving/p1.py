'''

Implement a queue with 2 stacks. ↴ Your queue should have an enqueue and a dequeue method and it should be "first in first out" (FIFO).

Optimize for the time cost of mm calls on your queue. These can be any mix of enqueue and dequeue calls.

Assume you already have a stack implementation and it gives O(1)O(1) time push and pop.

'''

class Stack():

    def __init__(self):
        return 1

    def isEmpty(self):
        return 1


stack_one=Stack()
stack_two=Stack()

def enqueue(obj):
    if (stack_one.isEmpty() and stack_two.isEmpty()): # both are empty
        stack_one.push(obj)

    elif (not stack_one.isEmpty() and stack_two.isEmpty()): # stack 1 has elements
                stack_one.push(obj)

    elif (stack_one.isEmpty() and not stack_two.isEmpty()):  # stack 2 has elements
        while(not stack_two.isEmpty()):
            stack_one.push(stack_two.pop())

        stack_one.push(obj)

def dequeue():

    if (stack_one.isEmpty() and not stack_two.isEmpty()):
        return stack_two.pop()
    elif (not stack_one.isEmpty() and stack_two.isEmpty()):
        while(not stack_one.isEmpty()):
            stack_two.push(stack_one.pop())
        return stack_two.pop()


class Queue():

    def __init__(self):
        self.stack1=Stack()
        self.stack2=Stack()

    def enqueue(self,obj):
        pass

    def dequeue(self):
        pass








