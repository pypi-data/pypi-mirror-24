.. _logrhythm:

=========
LogRhythm
=========

.. note:: This integration is part of the Python standalone integration. Please see :ref:`here <standalone_configuration>`
          and :ref:`here <general_configuration>` for additional information and email support@phishme.com to request
          the standalone integration.

.. image:: /standalone_integration_logrhythm/logrhythm_logo.png

.. rst-class:: html-toggle

Overview
--------

PhishMe's IOCs are processed into a series of flat files by type and impact (when applicable). These files are written
to a file share that is accessible to the LogRhythm Threat Intelligence manager. The LogRhythm Threat Intelligence
manager can be configured to process all or just some of these lists of indicators and has support for displaying this
content in a consistent manner.

.. rst-class:: html-toggle

Integration Setup Prerequisites
-------------------------------

    * Ability to write to file share accessible by LogRhythm's Threat Intelligence manager (Windows host).

.. rst-class:: html-toggle

Sample config.ini
-----------------

config.ini example::

    [integration_logrhythm]
    use = True
    output_dir = /tmp/phishme_intelligence_for_logrhythm

.. rst-class:: html-toggle

config.ini Descriptions
-----------------------

.. list-table::
    :widths:  10, 10, 70, 10
    :header-rows: 1

    * - Section
      - Key
      - Description
      - Required
    * - integration_logrhythm
      - use
      - A Boolean value to control whether the integration outputs to LogRhythm
      - True
    * - integration_logrhythm
      - output_dir
      - Filesystem directory to write newline-separated indicator files to (to be ingested by LogRhythm)
      - True

.. rst-class:: html-toggle

Features
--------

Screenshots pending.