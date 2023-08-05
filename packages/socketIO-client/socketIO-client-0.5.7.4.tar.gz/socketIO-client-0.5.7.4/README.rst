.. image:: https://travis-ci.org/invisibleroads/socketIO-client.svg?branch=0.5.7.4
    :target: https://travis-ci.org/invisibleroads/socketIO-client

socketIO-client
===============
Here is a `socket.io <http://socket.io>`_ client library for Python. You can use it to write test code for your socket.io server.

Please note that this version implements `socket.io protocol 0 <https://github.com/learnboost/socket.io-spec>`_, which is compatible with `gevent-socketio <https://github.com/abourget/gevent-socketio>`_. If you want to communicate using `socket.io protocol 1 <https://github.com/automattic/socket.io-protocol>`_, please use `socketIO-client 0.8.0 <https://pypi.python.org/pypi/socketIO-client>`_ or higher.


Installation
------------
Install the package in an isolated environment. ::

    VIRTUAL_ENV=$HOME/.virtualenvs/crosscompute
    virtualenv $VIRTUAL_ENV
    source $VIRTUAL_ENV/bin/activate
    pip install -U socketIO-client==0.5.7.4


Test
----
Install additional packages if you want to run the tests. ::

    VIRTUAL_ENV=$HOME/.virtualenvs/crosscompute
    export NODE_PATH=$VIRTUAL_ENV/lib/node_modules
    export NPM_CONFIG_PREFIX=$VIRTUAL_ENV
    npm install -g socket.io@0

Launch test server and run tests.::

    cd ~/Documents
    git clone https://github.com/invisibleroads/socketIO-client
    git checkout -t 0.5.7.4
    cd socketIO-client
    node serve-tests.js  # Start socket.io server in terminal one
    nosetests  # Run tests in terminal two


Usage
-----
Activate isolated environment. ::

    VIRTUAL_ENV=$HOME/.virtualenvs/crosscompute
    source $VIRTUAL_ENV/bin/activate
    export NODE_PATH=$VIRTUAL_ENV/lib/node_modules
    export NPM_CONFIG_PREFIX=$VIRTUAL_ENV

Start your socket.io server. ::

    node serve-tests.js

For debugging information, run these commands first. ::

    import logging
    logging.basicConfig(level=logging.DEBUG)

Emit. ::

    from socketIO_client import SocketIO, LoggingNamespace

    with SocketIO('localhost', 8000, LoggingNamespace) as socketIO:
        socketIO.emit('aaa')
        socketIO.wait(seconds=1)

Emit with callback. ::

    from socketIO_client import SocketIO, LoggingNamespace

    def on_bbb_response(*args):
        print('on_bbb_response', args)

    with SocketIO('localhost', 8000, LoggingNamespace) as socketIO:
        socketIO.emit('bbb', {'xxx': 'yyy'}, on_bbb_response)
        socketIO.wait_for_callbacks(seconds=1)

Define events. ::

    from socketIO_client import SocketIO, LoggingNamespace

    def on_connect():
        print('connect')

    def on_disconnect():
        print('disconnect')

    def on_reconnect():
        print('reconnect')

    def on_aaa_response(*args):
        print('on_aaa_response', args)

    socketIO = SocketIO('localhost', 8000, LoggingNamespace)
    socketIO.on('connect', on_connect)
    socketIO.on('disconnect', on_disconnect)
    socketIO.on('reconnect', on_reconnect)

    # Listen
    socketIO.on('aaa_response', on_aaa_response)
    socketIO.emit('aaa')
    socketIO.wait(seconds=1)

Define events in a namespace. ::

    from socketIO_client import SocketIO, BaseNamespace

    class Namespace(BaseNamespace):

        def on_aaa_response(self, *args):
            print('on_aaa_response', args)
            self.emit('bbb')

    socketIO = SocketIO('localhost', 8000, Namespace)
    socketIO.emit('aaa')
    socketIO.wait(seconds=1)

Define standard events. ::

    from socketIO_client import SocketIO, BaseNamespace

    class Namespace(BaseNamespace):

        def on_connect(self):
            print('[Connected]')

        def on_reconnect(self):
            print('[Reconnected]')

        def on_disconnect(self):
            print('[Disconnected]')

    socketIO = SocketIO('localhost', 8000, Namespace)
    socketIO.wait(seconds=1)

Define different namespaces on a single socket. ::

    from socketIO_client import SocketIO, BaseNamespace

    class ChatNamespace(BaseNamespace):

        def on_aaa_response(self, *args):
            print('on_aaa_response', args)

    class NewsNamespace(BaseNamespace):

        def on_aaa_response(self, *args):
            print('on_aaa_response', args)

    socketIO = SocketIO('localhost', 8000)
    chat_namespace = socketIO.define(ChatNamespace, '/chat')
    news_namespace = socketIO.define(NewsNamespace, '/news')

    chat_namespace.emit('aaa')
    news_namespace.emit('aaa')
    socketIO.wait(seconds=1)

Connect via SSL. ::

    from socketIO_client import SocketIO

    # Skip server certificate verification
    SocketIO('https://localhost', verify=False)

Specify params, headers, cookies, proxies thanks to the `requests <http://docs.python-requests.org>`_ library. ::

    from socketIO_client import SocketIO

    SocketIO('localhost', 8000, params={
        'q': 'qqq',
    }, headers={
        'Authorization': 'Bearer xyz',
    }, cookies={
        'a': 'aaa',
    }, proxies={
        'https': 'https://proxy.example.com:8080',
    })

Wait forever. ::

    from socketIO_client import SocketIO

    socketIO = SocketIO('localhost', 8000)
    socketIO.wait()

Don't wait forever. ::

    from socketIO_client import SocketIO
    from socketIO_client.exceptions import ConnectionError

    try:
        socket = SocketIO('localhost', 8000, wait_for_connection=False)
        socket.wait()
    except ConnectionError:
        print('The server is down. Try again later.')


License
-------
This software is available under the MIT License.


Credits
-------
- `Guillermo Rauch <https://github.com/rauchg>`_ wrote the `socket.io specification <https://github.com/LearnBoost/socket.io-spec>`_.
- `Hiroki Ohtani <https://github.com/liris>`_ wrote `websocket-client <https://github.com/liris/websocket-client>`_.
- `rod <http://stackoverflow.com/users/370115/rod>`_ wrote a `prototype for a Python client to a socket.io server <http://stackoverflow.com/questions/6692908/formatting-messages-to-send-to-socket-io-node-js-server-from-python-client>`_.
- `Alexandre Bourget <https://github.com/abourget>`_ wrote `gevent-socketio <https://github.com/abourget/gevent-socketio>`_, which is a socket.io server written in Python.
- `Paul Kienzle <https://github.com/pkienzle>`_, `Zac Lee <https://github.com/zratic>`_, `Josh VanderLinden <https://github.com/codekoala>`_, `Ian Fitzpatrick <https://github.com/ifitzpatrick>`_, `Lucas Klein <https://github.com/lukasklein>`_, `Rui Chicoria <https://github.com/rchicoria>`_, `Travis Odom <https://github.com/burstaholic>`_, `Patrick Huber <https://github.com/stackmagic>`_, `Brad Campbell <https://github.com/bradjc>`_, `Daniel <https://github.com/dabidan>`_, `Sean Arietta <https://github.com/sarietta>`_ submitted code to expand support of the socket.io protocol.
- `Bernard Pratz <https://github.com/guyzmo>`_, `Francis Bull <https://github.com/franbull>`_ wrote prototypes to support xhr-polling and jsonp-polling.
- `Eric Chen <https://github.com/taiyangc>`_, `Denis Zinevich <https://github.com/dzinevich>`_, `Thiago Hersan <https://github.com/thiagohersan>`_, `Nayef Copty <https://github.com/nayefc>`_, `Jörgen Karlsson <https://github.com/jorgen-k>`_, `Branden Ghena <https://github.com/brghena>`_, `Tim Landscheidt <https://github.com/scfc>`_, `Khairi Hafsham <https://github.com/khairihafsham>`_ suggested ways to make the connection more robust.
- `Merlijn van Deen <https://github.com/valhallasw>`_, `Frederic Sureau <https://github.com/fredericsureau>`_, `Marcus Cobden <https://github.com/leth>`_, `Drew Hutchison <https://github.com/drewhutchison>`_, `wuurrd <https://github.com/wuurrd>`_, `Adam Kecer <https://github.com/amfg>`_, `Alex Monk <https://github.com/Krenair>`_, `Vishal P R <https://github.com/vishalwy>`_, `John Vandenberg <https://github.com/jayvdb>`_, `Thomas Grainger <https://github.com/graingert>`_ proposed changes that make the library more friendly and practical for you!
