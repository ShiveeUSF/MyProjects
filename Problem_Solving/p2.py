'''
Write a program that asks the user how many Fibonnaci numbers to generate and then generates them.
Take this opportunity to think about how you can use functions.
Make sure to ask the user to enter the number of numbers in the sequence to generate.
Hint: The Fibonnaci seqence is a sequence of numbers where the next number in the sequence is the sum of the previous two numbers in the sequence. The sequence looks like this: 1, 1, 2, 3, 5, 8, 13)
'''

def fib(n):
    a=1
    b=1
    print(a)
    n-=1
    while True:
        if n>0:
            print(b)
            n-=1
        if n==0: break
        a,b=b,a+b

n=input('How many Fibo')
n=int(n)
fib(n)


