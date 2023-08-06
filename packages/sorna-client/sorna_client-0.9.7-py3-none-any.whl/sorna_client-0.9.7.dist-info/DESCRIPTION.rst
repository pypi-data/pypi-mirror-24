Sorna Client
============

|PyPI| |Python Versions| |Travis Build Status| |AppVeyor Build Status|
|Code Coverage|

The API client library for `Sorna <http://sorna.io>`__

Usage
-----

You should set the access key and secret key as environment variables to
use the API. Grab your keypair from
`cloud.sorna.io <https://cloud.sorna.io>`__ or your cluster admin.

.. code:: sh

    export SORNA_ACCESS_KEY=...
    export SORNA_SECRET_KEY=...

    # optional (for local clusters)
    export SORNA_ENDPOINT="https://my-precious-cluster/"

Command-line Interface
----------------------

Use ``sorna.cli`` module with ``run`` command.

To run the code specified in the command line directly, use ``-c``
option to pass the code string.

.. code:: console

    $ python -m sorna.cli run python3 -c "print('hello world')"
    ∙ Client session token: d3694dda6e5a9f1e5c718e07bba291a9
    ✔ Kernel (ID: zuF1OzMIhFknyjUl7Apbvg) is ready.
    hello world
    ✔ Cleaned up the kernel.

You can even run a C code on-the-fly. (Note that we put a dollar sign
before the single-quoted code argument so that the shell to interpret
``'\n'`` as actual newlines.)

.. code:: console

    $ python -m sorna.cli run c -c $'#include <stdio.h>\nint main() {printf("hello world\\n");}'
    ∙ Client session token: abc06ee5e03fce60c51148c6d2dd6126
    ✔ Kernel (ID: d1YXvee-uAJTx4AKYyeksA) is ready.
    hello world
    ✔ Cleaned up the kernel.

For larger programs, you may upload multiple files and then build &
execute them. The below is a simple example to run `a sample C
program <https://gist.github.com/achimnol/df464c6a3fe05b21e9b06d5b80e986c5>`__.

.. code:: console

    $ git clone https://gist.github.com/achimnol/df464c6a3fe05b21e9b06d5b80e986c5 sorna-c-example
    Cloning into 'sorna-c-example'...
    Unpacking objects: 100% (5/5), done.
    $ cd sorna-c-example
    $ python -m sorna.cli run c main.c mylib.c mylib.h
    ∙ Client session token: 1c352a572bc751a81d1f812186093c47
    ✔ Kernel (ID: kJ6CgWR7Tz3_v2WsDHOwLQ) is ready.
    ✔ Uploading done.
    ✔ Build finished.
    myvalue is 42
    your name? LABLUP
    hello, LABLUP!
    ✔ Cleaned up the kernel.

Please refer the ``--help`` manual provided by the ``run`` command.

You may use a shortcut command ``lcc`` and ``lpython`` instead of typing
the full Python module path like:

.. code:: console

    $ lcc main.c mylib.c mylib.h

Synchronous API
---------------

.. code:: python

    from sorna.kernel import Kernel

    kern = Kernel.get_or_create('lua5', client_token='abc')
    result = kern.execute('print("hello world")', mode='query')
    print(result['console'])
    kern.destroy()

You need to take care of ``client_token`` because it determines whether
to reuse kernel sessions or not. Sorna cloud has a timeout so that it
terminates long-idle kernel sessions, but within the timeout, any kernel
creation requests with the same ``client_token`` let Sorna cloud to
reuse the kernel.

Asynchronous API
----------------

.. code:: python

    import asyncio
    from sorna.asyncio.kernel import AsyncKernel

    async def main():
        kern = await AsyncKernel.get_or_create('lua5', client_token='abc')
        result = await kern.execute('print("hello world")', mode='query')
        print(result['console'])
        await kern.destroy()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

All the methods of ``AsyncKernel`` objects are exactly same to the
synchronous version, except that they are coroutines.

Additionally, ``AsyncKernel`` offers async-only method ``stream_pty()``.
It returns a ``StreamPty`` object which allows you to access a
pseudo-tty of the kernel. ``StreamPty`` works like an async-generator
and provides methods to send stdin inputs as well as resize the
terminal.

.. |PyPI| image:: https://badge.fury.io/py/sorna-client.svg
   :target: https://pypi.python.org/pypi/sorna-client
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/sorna-client.svg
   :target: https://pypi.org/project/sorna-client/
.. |Travis Build Status| image:: https://travis-ci.org/lablup/sorna-client.svg?branch=master
   :target: https://travis-ci.org/lablup/sorna-client
.. |AppVeyor Build Status| image:: https://ci.appveyor.com/api/projects/status/5h6r1cmbx2965yn1/branch/master?svg=true
   :target: https://ci.appveyor.com/project/achimnol/sorna-client/branch/master
.. |Code Coverage| image:: https://codecov.io/gh/lablup/sorna-client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/lablup/sorna-client


