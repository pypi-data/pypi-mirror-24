.. _Intro:

Introduction
============


.. danger:: This project is **ENTIRELY EXPERIMENTAL** at the
            moment. Use at your own will or if you want to contribute
            to it

CarbonTube is an easy python DSL for describing phases of execution of a
pipeline.

Even more, the phases can be scaled up independently and spread in a
network.


This is NOT a DATA pipeline framework
-------------------------------------

This framework allows you to describe workers using a simple DSL.
Each worker produces a given ``job_type``.

A pipeline is a sequence of job types that will be coordinate with any
idle workers that announce their availability.

This gives you the advantage of scaling your infrastructure
horizontally and vertically with very little effort.


Features
--------

- Describe phase workers using python classes and get them running within minutes
- Describe pipelines that can juggle with any available phases
- Easily scale phases individually in a pipeline
- Easily scale pipelines onto clusters
- Empower sys-admins to take quick action and increase the number of
  phases on demand, be it with new machines, new docker instances or
  even one-off spawned processes.
- On-demand live web interface with live pipeline cluster information
- Redis queue and metrics persistence
