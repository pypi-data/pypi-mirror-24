.. _cb_response:

============
 CB Response
============

.. note:: This integration is part of the Python standalone integration. Please see :ref:`here <standalone_configuration>`
          and :ref:`here <general_configuration>` for additional information and email support@phishme.com to request
          the standalone integration.

.. rst-class:: html-toggle

Overview
--------

PhishMe Intelligence and Carbon Black partner to alert your Cyber Security Team when network communication is detected
between your endpoints and botnet infrastructures. PhishMe Intelligence provides a high-signal, context-rich source of
threat intelligence about the latest phishing and malware attacks hitting businesses, universities, and agencies every
day. PhishMe analyzes and verifies every threat before we publish the indicators so your team doesn’t waste time on false positives.

.. rst-class:: html-toggle

Network Requirement(s)
----------------------

    * Access to Carbon Black master server on TCP port 443.

.. rst-class:: html-toggle

Software Requirement(s)
-----------------------

    * Permission to write to a file system readable by the Carbon Black master server.

.. rst-class:: html-toggle

Sample config.ini
-----------------

config.ini example::

    [integration_carbon_black]
    use = False
    ssl_verify = False
    host_with_protocol =
    api_token =
    feed_name =
    feed_id = 34
    sqlite_location = /tmp/cb.db
    sqlite_data_retention_days = 30
    cb_feed = /tmp/phishme_intelligence_for_carbon_black.json
    impact_major = 100
    impact_moderate = 75
    impact_minor = 35
    impact_none = 0
    excluded_md5_use = True
    excluded_md5 = []

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
    * - integration_carbon_black
      - use
      - A Boolean value to control whether the integration outputs to CB Response
      - True
    * - integration_carbon_black
      - ssl_verify
      - A Boolean value to control whether the SSL certificate used for a connection to CB Response should be
        verified
      - True
    * - integration_carbon_black
      - host_with_protocol
      - The destination hostname or IPv4 address (with protocol) of the CB Response instance
      - True
    * - integration_carbon_black
      - api_token
      - CB Response API Token to use to connect to CB Response
      - True
    * - integration_carbon_black
      - feed_name
      - Name of CB Response feed to write PhishMe Intelligence JSON feed to
      - True
    * - integration_carbon_black
      - feed_id
      - Numeric ID of CB Response feed to write PhishMe Intelligence JSON feed to
      - True
    * - integration_carbon_black
      - sqlite_location
      - Filesystem location of SQLite database used to manage PhishMe Intelligence indicators written to JSON CB
        Response feed.
      - True
    * - integration_carbon_black
      - sqlite_data_retention_days
      - Number of days to retain PhishMe Intelligence Indicators in SQLite database
      - True
    * - integration_carbon_black
      - cb_feed
      - Filesystem location to write JSON CB Response feed to
      - True
    * - integration_carbon_black
      - impact_major
      - Numeric value to indicate Major impact PhishMe Intelligence indicators in CB Response feed
      - True
    * - integration_carbon_black
      - impact_moderate
      - Numeric value to indicate Moderate impact PhishMe Intelligence indicators in CB Response feed
      - True
    * - integration_carbon_black
      - impact_minor
      - Numeric value to indicate Minor impact PhishMe Intelligence indicators in CB Response feed
      - True
    * - integration_carbon_black
      - impact_none
      - Numeric value to indicate None impact PhishMe Intelligence indicators in CB Response feed
      - True
    * - integration_carbon_black
      - excluded_md5_use
      - Boolean to indicate whether MD5 values are being specified for exclusion
      - True
    * - integration_carbon_black
      - excluded_md5
      - List of MD5 indicators to exclude from JSON CB Response feed.
      - True