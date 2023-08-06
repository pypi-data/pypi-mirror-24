A package for creating and enqueueing stressypy jobs
====================================================

``rqpop`` uses the python package ``stressypy`` to create a certain number of cpu-stressing jobs for a variably
distributed amount of time, the distribution type and seed being specified by the user.
It creates ``stressypy``'s ``JobBlock`` objects which contain pertinent information for queueing these test jobs to
test queueing algorithms by enqueueing a certain number of randomly 'sized' jobs, which simulates the real job influx
of a webservice, for example. The jobs are enqueued with RQ (Redis Queue).

JobBlocks:
++++++++++
refer to https://github.com/salbrandi/stressypy#jobblock-attributes for documentation on JobBlock objects


Installation
++++++++++++

``rqpop`` can be installed with ``pip install rqpop`` and will auto-install all dependencies.

Alternatively, it can be cloned manually from the url: https://github.com/salbrandi/rqpop.git
or the tarfile can be downloaded from the url: https://github.com/salbrandi/rqpop/archive/0.1.tar.gz
and setup with ``python setup.py install``

| In order to run rqpop, you must have a REDIS server running and RQ ``rqworkers`` listening on the default queue:
|
| Documentation for quickly setting up a REDIS server can be found here: https://redis.io/topics/quickstart
| Full REDIS documentaiton here: https://redis.io/documentation
|
| Documentation for RQ (Redis Queue) cna be found here: http://python-rq.org/
| but for most users a worker can be started, listening on the default queue with simply the ``rqworker`` command.

Directions
++++++++++

``rqpop`` runs using the command ``rqpop queue`` with the number of jobs desired and the max time allowed being passed as arguments.
The seed for the distribution of job 'sizes' can be specified with ``--seed``, the minimum and maximum cpu with ``--mnc`` and ``--mxc``
respectively, the minimum time with ``--mnt`` and the queue with ``--q``.
The default distribution type is a log normal distribution, but the type can be specified using ``--distribution``.

Distributions supported are:

- Log Normal: ``normal`` - default
- Box: ``box``
- Spike/Dirac/Delta: ``spike``
- Exponential/Power: ``power``

Examples
--------
* ``rqpop queue 10 12 --seed 0 --distribution normal``:
    creates and enqueues 10 jobs normally distributed with seed 0 and a max time of 12 seconds


* ``rqpop queue 21456 --seed 1023041 --distribution power --mnc 2 --mxc 10 -q high``:
    creates and enqueues 21, 456 jobs exponentially distributed with seed 1023041, min cores 2, max cores 10 on the queue 'high

