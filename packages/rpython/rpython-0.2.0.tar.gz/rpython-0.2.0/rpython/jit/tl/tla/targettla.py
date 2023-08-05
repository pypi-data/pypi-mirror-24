import py
py.path.local(__file__)
from rpython.jit.tl.tla import tla


def entry_point(args):
    for i in range(len(argv)):
        if argv[i] == "--jit":
            if len(argv) == i + 1:
                print "missing argument after --jit"
                return 2
            jitarg = argv[i + 1]
            del argv[i:i+2]
            jit.set_user_param(jitdriver, jitarg)
            break

    if len(args) < 3:
        print "Usage: %s filename x" % (args[0],)
        return 2
    filename = args[1]
    x = int(args[2])
    w_x = tla.W_IntObject(x)
    bytecode = load_bytecode(filename)
    w_res = tla.run(bytecode, w_x)
    print w_res.getrepr()
    return 0

def load_bytecode(filename):
    from rpython.rlib.streamio import open_file_as_stream
    f = open_file_as_stream(filename)
    bytecode = f.readall()
    f.close()
    return bytecode

def target(driver, args):
    return entry_point

# ____________________________________________________________


if __name__ == '__main__':
    import sys
    sys.exit(entry_point(sys.argv))
