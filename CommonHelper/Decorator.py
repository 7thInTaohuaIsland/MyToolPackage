import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func()
        end_time = time.time()
        print(end_time - start_time)
    return wrapper