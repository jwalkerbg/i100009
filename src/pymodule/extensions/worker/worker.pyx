# src/pymodule/cyth/worker.pyx

import time

def worker_func():
    print("Worker")
    for i in range(5):
        print(f"i = {i}")
    print("Worker finished")

def cython_benchmark(int n):
    cdef int i
    start_time = time.time()

    # Perform the sum of squares calculation in a Cythonized loop
    result = 0
    for i in range(n):
        cython_fibonacci(300)

    end_time = time.time()
    diff = ((end_time - start_time) * 1000.0)
    print(f"Cython function executed in {diff:03.6f} milliseconds")
    return diff

def cython_fibonacci(int n):
    cdef int a = 0, b = 1, temp, i
    for i in range(n):
        temp = a
        a = b
        b = temp + b
    return a
