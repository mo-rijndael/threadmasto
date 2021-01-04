Threadmasto
===========

Threadmasto is a universal modular reposter with bridge-based configuation.

Bridge-based?
-------------

Yes, main unit in Threadmasto is a bridge, which binds one source to one destination.
It gives us very flexible architecture, for example, Threadmasto can work as aggregator, even in one social network.

How to install?
---------------

Just clone this repository. You also need python >= 3.6, module `requests`, and Threadmasto modules dependencies.
I highly recommend you use separate python venv_ for this shit.

.. _venv: https://docs.python.org/3/library/venv.html

Then you need to configure content modules, go to `doc/configuration <doc/configuration.rst>`_ for details.

There is no module I need, what should I do?
--------------------------------------------

1. You can open issue, but there is no guarantee that I will develop it.
2. If you know Python, or know somebody who knows, there is `docs for module developers <doc/writing_modules.rst>`

You can also make pull-request with your module.

*I have big plan for module system, so make sure I can contact to you(module developer) in future*

Something is missing in docs, I don't understand it!
----------------------------------------------------

Open an issue. I'll explain it for you, and update documentation.
