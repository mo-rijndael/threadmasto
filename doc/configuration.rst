Basic concepts
==============

Sources and destinations
------------------------

Threadmasto is a crossposter, so, it copies content from some source to destination.
Sources and destinations are usually "pointers" to account in social network.

*if you want to implement your own source or destination, wait until I'll write docs for developers*

Bridges
-------

Bridge is main unit in Threadmasto. It holds one source, one destination and when was last source checking.
Bridges allows Threadmasto to work in agregator mode, or republish one source do many different platforms.

*here should be schematic example, but not now*

Modular architecture
--------------------

All sources and destinations are in dynamic-loaded modules, so there is no need to modify Threadmasto code to add/update code of source or destination.

Configuring
===========

All configs are stored as YAML files in `modconf.d/` directory. There can be many YAML files, but one definition should be entirely in one file.

Define source
-------------

Sources are defined in section `sources` in YAML file. Every source has a name to bind it to bridge, and type field.
Also, source can take configuration, just write corresponding YAML in definition.

.. code-block:: yaml
        sources:
                my_source:
                        type: test
                        parameter: value
        

Define destinations
-------------------

Destinations are defined same as sources, but in section `destinations`. Source and destination can have same names.

.. code-block:: yaml
        destinations:
                my_destination:
                        type: test
                        parameter: value

Define bridge
-------------

And finally, lets bind our sources and destinations. Bridges should be defined in section `bridges` as list of objects.
Every bridge must contain fields:
1. `source` - name of source
2. `destination` - name of destination
3. `interval` - bridge will be activated every <interval> seconds

.. code-block:: yaml
        bridges:
                - source: my_source
                  destination: my_destination
                  interval: 30 # every 30 seconds

example configuration also can be found in `modconf.d/example.yml`
