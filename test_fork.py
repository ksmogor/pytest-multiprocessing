import os


def test_multiple_children():

    for i in range(4):
        print(f"Forking new child from {os.getpid()}.")
        ret = os.fork()
        if ret == 0:
            print(f"Hello form child {os.getpid()}! Failing test")
            assert False

    print("All forked.")
    assert True
