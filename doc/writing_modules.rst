Writing your own modules
========================

There is can be situation, when Threadmasto doesn't have module you need. But you can write it by yourself!

Module structure
----------------

First of all, module is just Python class. It contains configuration and provides interface for Threadmasto core.

Imports
~~~~~~~

You have to import some classes from core, to communicate properly. Like this:

.. code-block:: python

        # if configuration of module is invalid, you should raise this
        from exceptions import InvalidConfig
        # types, mostly needed for sources, but destinations can use it for type-hints
        from publication import Publication, FileAttach, FileType, Poll
        # Abstract classes for inherritance and registering
        from . import Source, Destination

Interfaces, you should provide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initialization
""""""""""""""

Both sources and destinations should provide init method

.. code-block:: python

        def __init__(self, raw: dict):
                ...

In raw argument you'll get configuration for your module. For example, for this YAML:

.. code-block:: yaml

        sources:
                my_source:
                        type: your_type
                        parameter1: value1
                        parameter2: value2
                        group_of_parameters:
                                member1:
                                        - 1
                                        - 2
                                        - 3
                                member2: 42

You'll get that dict:

.. code-block:: python

        {       # you don't need to check type, Threadmasto already done it
                "type": "your_type",
                "parameter1": "value1",
                "parameter2": "value2",
                "group_of_parameters": {
                                "member1": [1, 2, 3],
                                "member2": 42
                        }
        }

Source interface
""""""""""""""""

To mark class as Source, inherrit from ``Source`` abstract class and decorate with ``Source.register(type: str)``. This type will be used later in ``type`` field in config.

.. code-block:: python

        @Source.register("my")
        class MySource(Source):
                ...

Sources must provide only one method:

.. code-block:: python

        # you will get timestamp, and should return publications, which are posted after this timestamp.
        # Source should not contain it in self state. Source is just pointer.
        def get(self, after_timestamp: float) -> List[Publication]:
                ...

We learn how to construct Publication object little later.

Destination interface
"""""""""""""""""""""

Destinations are marked same as sources - inherrit from ``Destination`` and decorate with ``Destination.register(type: str)``.

.. code-block:: python

        @Destination.register("my")
        class MyDestination(Destination):
                ...

Interface of destination contains one method too:

.. code-block:: python

        def publish(self, post: Publication):
                ...

Now, let's learn how to use built-in types.

Types
~~~~~

exceptions.InvalidConfig
""""""""""""""""""""""""

If user gives you invalid configuration, you should raise this.

.. code-block:: python

        raise InvalidConfig("message, that tells, what's wrong")

there is optional ``file`` argument, but in totally most cases Threadmasto can set if for you.

publication.Publication
"""""""""""""""""""""""

Object, which represents.... publication! Wow!

.. code-block:: python

        # I'll explain attachments system below
        Publication(plain_text: str, attachments: list)

Attachment list can contains FileAttach and Poll objects

publication.FileType
""""""""""""""""""""

When we work with files, every files has a type. There are four types in enum, which is suitable for most attachments in social networks:

- ``FileType.IMAGE``
- ``Filetype.VIDEO``
- ``FileType.AUDIO``
- ``FileType.CUSTOM`` - for any other file.

publication.FileAttach
""""""""""""""""""""""

Represents file, attached to Publication. Can be created using link to internet, or via path to file.

.. code-block:: python

        # first argument is type from FileType
        FileAttach(FileType.IMAGE, link="https://example.com/image.jpg")
        # or
        FileAttach(FileType.IMAGE, file_name="/path/to/file.jpg")

Using FileAttach is very simple. It provides two properties: ``file_name`` and ``fd``. First returns path to file, second returns file object, opened in ``w+b`` mode (reading and writing in binary mode). If FileAttach was created using link, it will be downloaded to temporary file.

.. code-block:: python

        print(attach.file_name) # /tmp/<random_name>
        print(attach.fd.read()) # b'<file content>'

publication.Poll
""""""""""""""""

Another popular attachment, which is not file is poll. Poll object just holds data. Title of poll, list of variants, and optionally can be marked as anonymous or multi-choice.

.. code-block:: python

        # Poll are not anonymous and not multiple by default
        poll = Poll("Yes?", ["yes", "no"], anonymous=True, multiple=True)
        if poll.anonymous:
                print("The   p r i v a c y")

That's all! I hope your module will be very nice
