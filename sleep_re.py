import timeit

start = timeit.timeit()
for i in range(154998):
    print("hello")
end = timeit.timeit()
print(end - start)
