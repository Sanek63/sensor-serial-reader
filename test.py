import sys


def print_f():
    print('1, 2, 3')


sys.stdout.write("Download progress: %d%%   \r" % (progress) )
sys.stdout.flush()
