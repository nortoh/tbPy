import time

def calculate_time(func):

    def inner(*args, **kwargs):

        begin_time = time.time()

        func(*args, **kwargs)

        end_time = time.time()
        time_taken = end_time - begin_time
        print(f'Executed {func.__name__} in {time_taken}s')
    
    return inner
