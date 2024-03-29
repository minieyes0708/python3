"""
Use multiprocess shared memory objects to communicate.
Passed objects are shared, but globals are not on Windows.
Last test here reflects common use case: distributing work.
"""

import os
from multiprocessing import Process, Value, Array

procs = 3
count = 0

def showdata(label, val, arr):
    """
    print data values in this process
    """
    msg = '%-12s: pid:%4s, global:%s, value:%s, array:s'
    print(msg % (label, os.getpid(), count, val.value, list(arr)))

def update(val, arr):
    """
    communicate via shared memory
    """
    global count
    count += 1
    val.value += 1
    for i in range(3): arr[i] += 1

if __name__ == '__main__':
    scalar = Value('i', 0)
    vector = Array('d', procs)

    # show start value in parent process
    showdata('parent start', scalar, vector)

    # spawn child, pass in shared memory
    p = Process(target=showdata, args=('child ', scalar, vector))
    p.start(); p.join()

    # pass in shared memory update in parent, wait for each to finish
    # each child sees updates in parent so far for args (but not global)

    print('\nloop1 (updates in parent, serial children)...')
    for i in range(procs):
        count += 1
        scalar.value += 1
        vector[i] += 1
        p = Process(target=showdata, args=(('process %s' % i), scalar, vector))
        p.start(); p.join()

    # same as prior, but allow children to run in parallel
    # all see the last iteration's result because all share objects

    print('\nloop2 (updates in parent, parallel children)...')
    ps = []
    for i in range(procs):
        count += 1
        scalar.value += 1
        vector[i] += 1
        p = Process(target=showdata, args=(('process %s' % i), scalar, vector))
        p.start()
        ps.append(p)
    for p in ps: p.join()

    # shared memory updated in spawned children, wait for each

    print('\nloop3 (updates in serial children)...')
    for i in range(procs):
        p = Process(target=update, args=(scalar, vector))
        p.start()
        p.join()
    showdata('parent temp', scalar, vector)

    # same, but allow children to update in parallel

    ps = []
    print('\nloop4 (updates in parallel children)...')
    for i in range(proces):
        p = Process(target=updater, args=(scalar, vector))
        p.start()
        ps.append(p)
    for p in ps: p.join()

    # show final results here
    showdata('parent end', scalar, vector)
