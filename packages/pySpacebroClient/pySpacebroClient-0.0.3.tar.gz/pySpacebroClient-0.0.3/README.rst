pySpacebroClient
==================

🌟 Connect easily to a [spacebro server](https://github.com/spacebro/spacebro).

a port of nodejs `spacebro-client <https://github.com/spacebro/spacebro-client/>`_


Why
---

No more custom socket.io server.

Easily connect with socket.io to other clients.

Spacebro offers an API to connect clients input and output together.

Installation
------------

.. code:: bash

  pip install pySpacebroClient

Usage
-----

1. Connect

.. code:: python

  from pySpacebroClient import SpacebroClient

  settings = {
      'host': 'spacebro.space',
      'port': 3333,
      'client': {
          'name': 'python-bro'
      },
      'channelName': 'mychannelname'
  }
  spacebroClient = SpacebroClient(settings)
  spacebroClient.wait()

2. Emit a message for an app called `node-bro`

.. code:: python

  from pySpacebroClient import SpacebroClient

  settings = {
      'host': 'spacebro.space',
      'port': 3333,
      'client': {
          'name': 'python-bro'
      },
      'channelName': 'mychannelname',
      'out': {
          'outMedia': {
              'eventName': 'outMedia',
              'description': 'Output media',
              'type': 'all'
          }
      },
      'connection': 'python-bro/outMedia => node-bro/inMedia'
  }
  spacebroClient = SpacebroClient(settings)
  spacebroClient.emit(settings.out.outMedia.eventName, {'value': 5})
  spacebroClient.wait()

3. Receive a message from an app called `chokibro`

.. code:: python

  from pySpacebroClient import SpacebroClient

  def on_inMedia(self, args):
      print('received', args)

  settings = {
      'host': 'spacebro.space',
      'port': 3333,
      'client': {
          'name': 'python-bro'
      },
      'channelName': 'mychannelname',
      'in': {
          'inMedia': {
              'eventName': 'inMedia',
              'description': 'Input media',
              'type': 'all'
          }
      },
      'connection': 'chokibro/outMedia => python-bro/inMedia'
  }
  spacebroClient = SpacebroClient(settings)
  spacebroClient.on(settings['in'].inMedia.eventName, self.on_inMedia)
  spacebroClient.wait()

test command
============

.. code:: bash

  python -m tests.test
