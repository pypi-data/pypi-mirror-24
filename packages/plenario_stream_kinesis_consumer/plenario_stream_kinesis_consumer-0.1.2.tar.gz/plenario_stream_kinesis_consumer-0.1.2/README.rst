Plenario ETL: Kinesis Consumer (JSON)
=====================================

A queue consumer that loads json data. This worker acts essentially as a
callback. It receives an augmented json payload from polling some
designated queue. The payload has been modified so that it is guaranteed
to have the metadata the worker needs to load it into the database. The
payload will also have an ``id`` that corresponds to an ongoing job
being tracked by the job manager. It is up to the worker to notify the
manager on success or *graceful* failure.

|Build Status|

Setup
-----

In order for the comsumer application to be runnable by the
MultiLangDaemon, the ``executableName`` provided by whichever
``*.properties`` file you're using must either be discoverable in your
environemnt's PATH variable, or it must be an absolute path.

    The MultiLangDaemon uses the environment that the jvm was launched
    in. On linux/unix systems the relevant environment variable that it
    uses to find the executable is PATH. You can test that your
    executable will be found using which (filling in the executable's
    name).

    -  https://forums.aws.amazon.com/thread.jspa?threadID=163698

.. code:: bash

    export PATH=$PATH:.

Test
----

.. code:: bash

    pytest

Running The Consumer
--------------------

bash
''''

.. code:: bash

    `worker/helper.py --print_command --properties .properties --java $(which java)`

.. |Build Status| image:: https://travis-ci.org/UrbanCCD-UChicago/plenario-stream-kinesis-consumer.svg
   :target: https://travis-ci.org/UrbanCCD-UChicago/plenario-stream-kinesis-consumer
