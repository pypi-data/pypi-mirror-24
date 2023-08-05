TODO
====


BY PRIORITY:
------------

* use a sorted set for the queues, they should be sorted by unix timestamp of the enqueuing moment.
* add a push socket to the phases and an option for actively connecting to multiple pull-bind sockets
* add full unit and functional test coverage
* update base storage to reflect the new interface defined at pyredis
  * create UI for moving jobs from failed to available so they can be reschedulled
* create UI to push jobs to a pipeline
* create UI to show average consumption speed of each queue for job type
* ensure that all storages, servers, models and utilities are exposed in the api docs
* storage backend should not force relationship between the job_type queues and the pipeline
* ensure that pipeline server checks if the available workers cached
  by the storage backend are still online
