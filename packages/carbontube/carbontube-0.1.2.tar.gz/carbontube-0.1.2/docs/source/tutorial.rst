.. _Tutorial:


.. highlight:: bash



Basic Usage
===========

Instalation
-----------

.. code:: bash

    pip install carbontube


Defining Phases
--------------

.. code:: python

    import os
    import uuid
    import hashlib

    from carbontube import Phase, Pipeline
    from carbontube.storage import RedisStorageBackend


    class GenerateFile(Phase):
        job_type = 'generate-file'

        def execute(self, instructions):
            size = instructions.get('size')
            if not size:
                return

            path = '/tmp/example-{0}.disposable'.format(uuid.uuid4())
            data = '\n'.join([str(uuid.uuid4()) for _ in range(size)])
            open(path, 'wb').write(data)
            return {'file_path': path}


    class HashFile(Phase):
        job_type = 'calculate-hash'

        def execute(self, instructions):
            if 'file_path' not in instructions:
                return

            file_path = instructions['file_path']
            if not os.path.exists(file_path):
                msg = "Failed to hash file {0}: does not exist".format(file_path)
                self.logger.warning(msg)
                raise RuntimeError(msg)

            data = open(file_path, 'rb').read()
            return {'hash': hashlib.sha1(data).hexdigest(), 'file_path': instructions['file_path']}


    class RemoveFile(Phase):
        job_type = 'delete-file'

        def execute(self, instructions):
            path = instructions.get('file_path')
            if path and os.path.exists(path):
                os.unlink(path)
                return {'deleted_path': path}

            raise RuntimeError('file already deleted: {0}'.format(path))


    class Example1(Pipeline):
        name = 'example-one'

        phases = [
            GenerateFile,
            RemoveFile
        ]

        def initialize(self):
            self.backend = RedisStorageBackend(self.name, redis_uri='redis://127.0.0.1:6379')


Running the servers
-------------------

.. code:: bash

    # run the pipeline
    carbontube pipeline examples/simple.py example-one \
        --sub-bind=tcp://127.0.0.1:6000 \
        --job-pull=tcp://127.0.0.1:5050

    # then execute the phases separately, they will bind to random
    # local tcp ports and announce their address to the pipeline
    # subscriber
    carbontube phase examples/simple.py generate-file \
        --sub-connect=tcp://127.0.0.1:6000
    carbontube phase examples/simple.py calculate-hash \
        --sub-connect=tcp://127.0.0.1:6000
    carbontube phase examples/simple.py delete-file \
        --sub-connect=tcp://127.0.0.1:6000


Feeding the pipeline with jobs
------------------------------


in the console
~~~~~~~~~~~~~~

.. code:: bash

    carbontube enqueue tcp://127.0.0.1:5050 example1 "{\"size\": 10}"


in python
~~~~~~~~~

.. code:: python

    from carbontube.clients import PipelineClient
    client = PipelineClient("tcp://127.0.0.1:5050")
    client.connect()

    job = {
        'name': 'example1'
        'instructions': {}
    }
    ok, payload = client.enqueue_job(job)
    if ok:
        print "JOB ENQUEUED!"
    else:
        print "PIPELINE'S BUFFER IS BUSY, TRY AGAIN LATER"
