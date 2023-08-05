Carbontube v0.1.1
=================

This is an old experiment I made with ZeroMQ + Gevent to build a DSL to easily define worker pipelines that are easily scalable across multiple boxes.
It is focused on optimizing units of work that share common, intense I/O activities.


Quickstart, get the demo running in 10 minutes
---------------------------------------------

OS Dependencies:

- python-dev (``apt-get install python-dev``)
- libevent-dev (``brew install libevent`` or ``apt-get install libevent-dev``
- libzmq-dev (``brew install libzmq`` or ``apt-get install libzmq-dev``)
- redis running on ``localhost:6379``

.. code:: bash

   $ git clone git@github.com:gabrielfalcao/carbontube.git
   $ cd carbontube
   $ mkvirtualenv carbontube
   $ pip install -r development.txt
   $ make pipeline-simple

   # now open another terminal and run the web server
   $ cd carbontube && workon carbontube
   $ make web


   # last step, in another terminal enqueue jobs
   $ cd carbontube && workon carbontube
   $ make enqueue-jobs



First, a tale
-------------

Tina is the CTO of a video app startup. She wants to optimize the
utilization of cloud boxes and extend the longevity of her company's
seed investment runway.

The choice is made: Every part of the video processing code will be
strategically executed in different boxes, cluster of GPU-optimized
boxes doing the video processing, small clusters of I/O optimized
boxes will parse files and store in long-term persistence.


The requirements
----------------

- Each step of the pipeline is encumbered by one and one job only
- A central pipeline must distribute jobs equally across workers
- Individual steps are not responsible about persisting jobs in case of failure
- In case of failure the pipeline should re-schedule the job
- The pipeline must have a pluggable storage mechanism to back the fail-recovery


The Tools
---------

- ZeroMQ ``pull`` workers execute each step of the pipeline, and
  ``publish`` events in regards to its state, real-time logs,
  availability and success/fail score.
- ZeroMQ ``push`` server that is aware of the capabilities of its
  subject steps.
- A web interface that listens for events published by steps and
  pipeline, showing real-time stats of pipeline health and
  availability.


Enter Carbontube...
-------------------


Defining pipeline phases
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from carbontube import Phase


    class EncodeVideo(Phase):
        job_type = 'encode-video'

        def execute(self, job):
            video_path = job.get('video_path')
            encoding_options = job.get('encoding_options')

            if not process_video(video_path, encoding_options):
                raise IOError('could not process video {video_title} with options {encoding_options}'.format(**job))

            video_uri = copy_video_to_cloud_storage(video_path)
            return {'video_uri': video_uri}


    class SplitIntoSegments(Phase):
        job_type = 'split-video'

        def execute(self, job):
            # ... some I/O



Defining the execution order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: python


    class VideoEncoderPipeline(Pipeline):
        name = 'video-encoder-pipeline'

        phases = [
            EncodeVideo,
            SplitIntoSegments,
        ]

        def initialize(self):
            self.backend = RedisStorageBackend(self.name, redis_uri='redis://cache1.internal.tinaapp.video:6379')




Deploying the encoder step
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash


   $ export HOSTNAME="encoder1.pipelines.internal.tinaapp.video"
   $ carbontube phase tinas-pipeline.py encode-video \
       --concurrency=4 \
       --pull-bind="tcp://${HOSTNAME}:3000" \
       --push-connect="tcp://${HOSTNAME}:4000" \
       --pub-connect="tcp://${HOSTNAME}:7000"


Deploying the file-split step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash


   $ export HOSTNAME="file-io1.pipelines.internal.tinaapp.video"
   $ carbontube phase tinas-pipeline.py split-video \
       --concurrency=8 \
       --pull-bind="tcp://${HOSTNAME}:3000" \
       --push-connect="tcp://${HOSTNAME}:4000" \
       --pub-connect="tcp://${HOSTNAME}:7000"


Deploying the pipeline manager server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash


   $ export HOSTNAME="video-pipeline.internal.tinaapp.video"
   $ carbontube pipeline tinas-pipeline.py video-encoder-pipeline \
         --pull-bind="tcp://${HOSTNAME}:5050" \
         --sub-bind="tcp://${HOSTNAME}:6000"


Feeding with jobs
~~~~~~~~~~~~~~~~~

**In Python**

.. code:: python


    from carbontube.clients import PipelineClient

    properly_formatted = {
        "name": "video-encoder-pipeline",
        "instructions": {
             "video_path": /tmp/video1.mp4",
        },
    }
    client = PipelineClient('tcp://video-pipeline.internal.tinaapp.video:5050')
    client.connect()
    ok, payload_sent = client.enqueue_job(properly_formatted)
    if ok:
        print "PUBLISHED JOB", payload_sent


**From the command-line**

.. code:: bash


   $ carbontube enqueue \
       tcp://video-pipeline.internal.tinaapp.video:5050 \
       video-encoder-pipeline \
       "{\"video_path\": '/tmp/video1.mp4'}"
