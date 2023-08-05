Design
======


Job Management
--------------

Queues
~~~~~~

* enqueued
* running
* success
* failed


Workflow 1 - success
~~~~~~~~~~~~~~~~~~~~


1. A Pipeline is defined by jobs ``foo`` and ``bar`` happening one after the other
2. A Worker of type ``foo`` announces its availability
3. A Worker of type ``bar`` announces its availability
4. A job of type ``foo[id=1]`` is enqueued
5. A Worker of type ``foo`` consumes the job ``id=1``
6. The pipeline moves the job ``id=1`` of type ``foo`` is moved to status ``running``
7. The worker of type ``foo`` acknowledges working on ``id=1``
8. The pipelie sets job ``foo[id=1]`` to status ``acknowledged``
9. The worker of type ``foo`` pushes finished work working on ``id=1``, pipeline sets it to ``success``
10. A Worker of type ``foo`` announces its availability


Workflow 2 - failed
~~~~~~~~~~~~~~~~~~~


1. A Pipeline is defined by jobs ``foo`` and ``bar`` happening one after the other
2. A Worker of type ``foo`` announces its availability
3. A Worker of type ``bar`` announces its availability
4. A job of type ``foo[id=1]`` is enqueued
5. A Worker of type ``foo`` consumes the job ``id=1``
6. The pipeline moves the job ``id=1`` of type ``foo`` is moved to status ``running``
7. The worker of type ``foo`` acknowledges working on ``id=1``
8. The pipelie sets job ``foo[id=1]`` to status ``acknowledged``
9. The worker of type ``foo`` reports failure to work on ``job[id=1]``, pipeline sets it to ``failed``
10. A Worker of type ``foo`` announces its availability
