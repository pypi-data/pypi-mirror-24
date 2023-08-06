SiBus Lib - Library for creating SiBus clients and servers
========================================================

Vous pouvez l'installer avec pip:

    pip install sibus_lib

Exemple d'usage:

    >>> from sibus_lib import sibus_init
    >>> from sibus_lib import BusCore

    >>> logger, cfg_data = sibus_init("bus.core")
    >>> buscore = BusCore()
    >>> buscore.start()

Ce code est sous licence WTFPL.
