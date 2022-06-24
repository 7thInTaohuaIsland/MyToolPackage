import time
from functools import wraps

def logit_time(PATH_LOG):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            logfile=open(PATH_LOG,'a')
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            consume = end - start
            log_string1 = func.__name__ + " was called"
            log_string2 = 'comsumed time: {0}'.format(consume)
            logfile.write(log_string1 + '\n' + log_string2 + '\n')
            logfile.close()
            return result
        return wrapped_function
    return logging_decorator

if __name__=='__main__':
    PATH_LOG='/home/user/log_test.log'
    @logit_time(PATH_LOG)
    def func_multiply(a,b):
        time.sleep(5)
        return a*b


    @logit_time(PATH_LOG)
    def func_print(a):
        time.sleep(5)
        print(a)

    c=func_multiply(1,2)
    print(c)
    func_print(3)


