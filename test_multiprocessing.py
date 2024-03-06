from multiprocessing import Pool, Process, SimpleQueue
import os
from multiprocessing.pool import ExceptionWithTraceback


def f(x):
    assert x != 0, " We don't want to see any 0 args here!"
    return x*x

def test_doc_example():
    res = []
    with Pool(5) as p:
        res = p.map(f, [1, 2, 3])
        #res = p.map(f, [1, 2, 3, 0]) # This raises assert exception on map function

    assert [1,4,9] == res

def worker(name):
    print(f'hello from {name}[{os.getpid()}]', name)
    assert False, "Testing assertion in subprocess - it require additional exception passing to parent process (MQ or PIPE)"

def test_process_worker():
    p = Process(target=worker, args=('bob',))
    print(f"Staring subprocess from parent {os.getpid()}")
    p.start()
    p.join()
    assert True

def worker_exception(name: str, queue: SimpleQueue):
    try:
        print(f'hello from {name}[{os.getpid()}]', name)
        assert False, "Testing assertion in subprocess"
        queue.put((False, None))  # empty result (like void)

    except Exception as e:
        queue.put((True, ExceptionWithTraceback(e, e.__traceback__)))  # exception result
        return


def test_process_raport_exception():
    q = SimpleQueue()
    p = Process(target=worker_exception, args=('bob', q))
    print(f"Staring subprocess from parent {os.getpid()}")
    p.start()

    ret = q.get()
    if ret[0]:
        raise ret[1]

    p.join()

    assert True
