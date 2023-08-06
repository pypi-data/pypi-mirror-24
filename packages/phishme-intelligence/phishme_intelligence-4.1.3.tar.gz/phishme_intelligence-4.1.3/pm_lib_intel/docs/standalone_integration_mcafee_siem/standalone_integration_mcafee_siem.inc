.. _mcafee_siem:

===========
McAfee SIEM
===========

.. note:: This integration is part of the Python standalone integration. Please see :ref:`here <standalone_configuration>`
          and :ref:`here <general_configuration>` for additional information and email support@phishme.com to request
          the standalone integration.

.. image:: /standalone_integration_mcafee_siem/mcafee_siem_logo.png

.. rst-class:: html-toggle

Overview
--------

PhishMe's IOCs are inserted into the McAfee SIEM in one of two ways. It is possible to ingest the data into McAfee SIEM
as you would any other structured log data. You can also use Cyber Threat Manager with McAfee SIEM 9.5 or newer to set
up a Cyber Threat Feed for the PhishMe IOCs. This Cyber Threat Feed can be used to automatically populate Watchlists and
with the Backtrace feature to search existing events for any IOC matches and perform a number of custom actions based on
that match.

.. rst-class:: html-toggle

Integration Setup Prerequisites
-------------------------------

    * Access to McAfee Event Receiver on UDP port (typically 514).
    * McAfee Event Receiver configured for PhishMe Intelligence data source.

.. rst-class:: html-toggle

Sample config.ini
-----------------

config.ini example::

    [integration_mcafee_siem]
    use = False
    max_eps = 500
    host_without_protocol = localhost
    port = 514


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
    * - integration_mcafee_siem
      - use
      - A Boolean value to control whether the integration outputs to McAfee SIEM
      - True
    * - integration_mcafee_siem
      - max_eps
      - The maximum number of events per second that should be output. This value acts as a throttle and has no
        caching feature, so unknown issues may arise if set too low.
      - False
    * - integration_mcafee_siem
      - host_without_protocol
      - The destination hostname or IPv4 address of the syslog messages.
      - False
    * - integration_mcafee_siem
      - port
      - The destination port number of the syslog messages.
      - False

.. rst-class:: html-toggle

Features
--------

Screenshots pending.
