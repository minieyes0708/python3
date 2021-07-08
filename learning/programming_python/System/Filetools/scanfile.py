def scanner(name, function):
    file = open(name, 'r')      # create a file object
    while True:
        line = file.readline()  # call file methods
        if not line: break      # untile end-of-file
        function(line)          # call a function object
    file.close()
