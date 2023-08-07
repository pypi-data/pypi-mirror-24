Gevent version of python-consul
===============================

While the python-consul doc advises to use the monkey patch approach when using gevent with python-consul you might run into trouble using other software alongside python-consul, say kafka-python for instance.

So this is a more careful approach using grequests versions of put, get, post etc.

Example usage
-------------

.. code:: python
	  
    from consulgevent import Consul

    # and then go on as usual
    consul = Consul()
    # ... and so on
