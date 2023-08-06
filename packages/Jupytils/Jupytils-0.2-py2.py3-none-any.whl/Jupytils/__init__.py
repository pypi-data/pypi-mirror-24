#
#
Jupytils_debug=1;

def log(*args, debug=False, **kwargs):
    if (not debug or 'debug' in kwargs and not kwargs(debug) ):
        return;

    for a in args:
        print(a, end=' ')
    for k,v in kwargs.items():
        print ("%s = %s" % (k, v))

log("This will load or reload Jupytils; This message in Future Versions", debug=Jupytils_debug)

from Jupytils.jcommon import *

#
LoadJupytils()
