.. _standalone_integration:

========================================
Standalone Integration Tips and Features
========================================

Concurrency
-----------
Each time this script is executed, it creates an empty lock file (the location is determined by a path in the config.ini file). On a successful exit, the lock file is removed. Prior to creating the lock file, the script verifies that a lock file does not already exist. If it does, the script immediately exits without performing any additional action. This prevents multiple instances of this script being executed at the same time.

File Location
-------------
PhishMe recommends placing the supplied files in a subdirectory under /opt. All the configuration that takes places will be applied to the config.ini file. While you can deploy config.ini in the same directory as the provided python scripts, PhishMe recommends as a best practice that you place this file in your home directory, change the owner and group (chown user:usergroup config.ini), change the permissions to this file to be 600 (chmod 600 config.ini) and pass the full path to the script as an argument to the '-conf' flag. And of course, none of this should be owned or executed as root.

Monitoring
----------
Very little, if any, information will be written to standard out. To follow along with the integration script and see what it is doing use the following command. The location of this file can be changed in the config.ini, the example is using the typical default setting and assumes a linux or Mac host. This log file is automatically rolled when it reaches 5MB and only the most recent 10 files are kept.
tail -f /tmp/phishme.log

Scheduler
---------
PhishMe recommends executing this script at 15 minute intervals. An example crontab entry would be::

   */15 * * * * /path/to/python /opt/phishme/intelligence/phishme_to_product.py -conf /home/username/config.ini

If that doesn't work, you may need to change the working directory like so::

   */15 * * * * cd /opt/phishme/intelligence && /path/to/python /opt/phishme/intelligence/phishme_to_product.py -conf /home/username/config.ini

Synchronization
---------------
This integration uses a combination of the init_date in the config file and a UUID stored in the position field to know what data to request from PhishMe's Intelligence API. When first executed, the init_date is used to perform a backfill of PhishMe Intelligence from that date to the current time. As the final step of this backfill, the current time is provided to the PhishMe Intelligence API and a UUID is returned. This UUID is written to the config.ini as the position value. During each subsequent request to PhishMe, this UUID will be provided and if new data is returned, a new UUID will also be returned and written to config.ini. Operationally, this means that service interruptions can occur on either the client or the server side for any time duration and synchronization will be achieved after the next successful execution of the PhishMe Intelligence integration script.

.. _standalone_configuration:

===========================================
Standalone Integration General Requirements
===========================================

Hardware
--------

    * Storage: 1 GB
    * Memory: 2 GB
    * Processor: 1 core, 2.0 Ghz

Network
-------

    * Access to https://www.threathq.com on TCP port 443

Python Version(s)
-----------------

    * Python 2.7.6+ or 3.4+

Python Modules
--------------

    * `python-requests <http://docs.python-requests.org/en/master/user/install/>`_
    * **(For STIX only)** `lxml <http://lxml.de/>`_

.. rst-class:: html-toggle

Test Script
-----------

You may use the following code to verify that your python environment is properly prepared::

    def check_requests():
    try:
        import requests
    except ImportError as exception:
        print('Check python-requests: FAIL')
    else:
        print('Check python-requests: PASS')


    def check_version():
        import sys

        if sys.version_info[0] == 2:
            try:
                assert sys.version_info >= (2, 6, 7)
            except AssertionError as exception:
                print('Check python version: FAIL')
                return

        elif sys.version_info[0] == 3:
            try:
                assert sys.version_info >= (3, 4)
            except AssertionError as exception:
                print('Check python version: FAIL')
                return

        print('Python version check: PASS')

    if __name__ == '__main__':
        check_requests()
        check_version()

.. _general_configuration:

============================================
Standalone Integration General Configuration
============================================

The following will describe the standard contents of a *config.ini* file for a PhishMe Intelligence integration. Please
note that an individual integration *may* have additional sections; these will be discussed in a later section if
applicable. Unless otherwise advised, please do not alter values in your config.ini file.

.. rst-class:: html-toggle

Sample config.ini
-----------------

See below for config.ini example::

    [pm_api]
    base_url = https://www.threathq.com/apiv1
    user =
    pass =
    init_date = 2016-01-01
    position =
    results_per_page = 100
    max_retries = 3

    [pm_jitter]
    use = False
    execution_frequency = 15
    scheduler_offset =

    [pm_product]
    intelligence = True
    brand_intelligence = False

    [pm_format]
    cef = False
    json = True
    stix = False

    [local_proxy]
    use = False
    http =
    https =
    auth_basic_use = False
    auth_basic_user =
    auth_basic_pass =

    [local_file_lock]
    use = True
    lock_file = /tmp/phishme.lock

    [local_log]
    log_level = info
    log_file = /tmp/phishme.log

    [local_sqlite]
    use = False
    db =
    data_deduplication_use =
    data_deduplication_hours =

    [output_cef]
    use = False
    max_eps = 500
    syslog_use = False
    syslog_host =
    syslog_port =
    append_file_use = False
    append_file_location =
    multiple_file_use = True
    multiple_file_location =
    multiple_file_split_by_date = True

    [output_json]
    use = True
    append_file_use = False
    append_file_location =
    multiple_file_use = False
    multiple_file_location =
    multiple_file_split_by_date = True

    [output_stix]
    use = False
    append_file_use = False
    append_file_location =
    multiple_file_use = True
    multiple_file_location =
    multiple_file_split_by_date = True

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
    * - pm_api
      - base_url
      - The base URL for PhishMe's Intelligence API.
      - True
    * - pm_api
      - user
      - The username for your PhishMe Intelligence API credentials. These can be generated at
        https://www.threathq.com/p42/settings/apitokens.
      - True
    * - pm_api
      - ssl_verify
      - A Boolean value to control whether the SSL certificate used for a connection to the PhishMe Intelligence API
        should be verified
      - True
    * - pm_api
      - pass
      - The password for your PhishMe Intelligence API credentials. These can be generated at
        https://www.threathq.com/p42/settings/apitokens.
      - True
    * - pm_api
      - init_date
      - A date field presented in yyyy-mm-dd format. When an integration is executed for the first time, this date is
        used to perform a backfill operation of existing PhishMe Intelligence.
      - True
    * - pm_api
      - position
      - A UUID that will track your current position with PhishMe. This will initially be blank, but will be
        automatically populated by the script.
      - False
    * - pm_api
      - results_per_page
      - This value determines the maximum number of JSON Threat IDs that can be retrieved in a single request.
      - True
    * - pm_api
      - max_retries
      - This value determines the number of times the script will repeat a failed request before exiting.
      - True
    * - pm_api
      - expired_threat_days
      - This value sets the th
      - True
    * -
      -
      -
      -
    * - pm_jitter
      - use
      - A Boolean value to control whether to enable API access "jitter"
      - True
    * - pm_jitter
      - execution_frequency
      - How often this integration should be executed (minutes). This value will nearly always be 15
      - False
    * - pm_jitter
      - scheduler_offset
      - The actual offset to use (randomly set). This will be populated by the integration
      - False
    * -
      -
      -
      -
    * - pm_product
      - intelligence
      - A Boolean value to control whether the PhishMe Intelligence product is retrieved in an API request.
      - True
    * - pm_product
      - brand_intelligence
      - A Boolean value to control whether the PhishMe Brand Intelligence product is retrieved in an API request.
      - True
    * -
      -
      -
      -
    * - pm_format
      - cef
      - A Boolean value to control whether CEF formatted data is retrieved in an API request.
      - True
    * - pm_format
      - json
      - A Boolean value to control whether JSON formatted data is retrieved in an API request.
      - True
    * - pm_format
      - cef
      - A Boolean value to control whether STIX formatted data is retrieved in an API request.
      - True
    * -
      -
      -
      -
    * - local_proxy
      - use
      - A Boolean value to control whether a proxy is needed for API requests.
      - True
    * - local_proxy
      - http
      - The HTTP proxy address for your network.
      - False
    * - local_proxy
      - https
      - The HTTPS proxy address for your network.
      - False
    * - local_proxy
      - auth_basic_use
      - A Boolean value to control whether BASIC authentication is required for your proxy.
      - False
    * - local_proxy
      - auth_basic_user
      - The NTLM username for your proxy access.
      - False
    * - local_proxy
      - auth_basic_pass
      - The NTLM password for your proxy access.
      - False
    * -
      -
      -
      -
    * - local_file_lock
      - use
      - A Boolean value to control whether a lock file is used. This empty file is used to prevent concurrent executions
        of the script. In rare cases, this file may be left behind if the script exits unexpectedly.
      - True
    * - local_file_lock
      - lock_file
      - The full path including file name that will be used to create the lock file.
      - True
    * -
      -
      -
      -
    * - local_log
      - log_level
      - Level of logging to set for integration. One of (debug, info, warning, error, critical). Usually set to info.
        Usually set to info.
      - True
    * - local_log
      - log_file
      - The full path including file name where a log file will be written. This file will be automatically rolled when
        it reaches 5 MB, for a total of 10 log files. The oldest file is then purged.
      - True
    * -
      -
      -
      -
    * - integration_raw_cef
      - use
      - A Boolean value to control whether CEF should be processed.
      - True
    * - integration_raw_cef
      - append_file_use
      - A Boolean value to control whether CEF messages are appended to the same file.
      - False
    * - integration_raw_cef
      - append_file_location
      - The full path including file name where these CEF messages will be written.
      - False
    * - integration_raw_cef
      - multiple_file_use
      - A Boolean value to control whether CEF messages are written into individual files, split by Threat ID.
      - False
    * - integration_raw_cef
      - multiple_file_location
      - The full path to a directory where CEF messages should be written.
      - False
    * - integration_raw_cef
      - multiple_file_split_by_date
      - A Boolean value to control whether the CEF messages should be placed in sub-folders according to the first
        publish date of the Threat ID.
      - False
    * -
      -
      -
      -
    * - integration_raw_json
      - use
      - A Boolean value to control whether JSON should be processed.
      - True
    * - integration_raw_json
      - append_file_use
      - A Boolean value to control whether JSON messages are appended to the same file.
      - False
    * - integration_raw_json
      - append_file_location
      - The full path including file name where these JSON messages will be written.
      - False
    * - integration_raw_json
      - multiple_file_use
      - A Boolean value to control whether JSON messages are written into individual files, split by Threat ID.
      - False
    * - integration_raw_json
      - multiple_file_location
      - The full path to a directory where JSON messages should be written.
      - False
    * - integration_raw_json
      - multiple_file_split_by_date
      - A Boolean value to control whether the JSON messages should be placed in sub-folders according to the first
        publish date of the Threat ID.
      - False
    * -
      -
      -
      -
    * - integration_raw_stix
      - use
      - A Boolean value to control whether STIX should be processed.
      - True
    * - integration_raw_stix
      - append_file_use
      - A Boolean value to control whether STIX messages are appended to the same file.
      - False
    * - integration_raw_stix
      - append_file_location
      - The full path including file name where these STIX messages will be written.
      - False
    * - integration_raw_stix
      - multiple_file_use
      - A Boolean value to control whether STIX messages are written into individual files, split by Threat ID.
      - False
    * - integration_raw_stix
      - multiple_file_location
      - The full path to a directory where STIX messages should be written.
      - False
    * - integration_raw_stix
      - multiple_file_split_by_date
      - A Boolean value to control whether the STIX messages should be placed in sub-folders according to the first
        publish date of the Threat ID.
      - False

.. include:: /integration_anomali_threatstream/integration_anomali_threatstream.inc

.. include:: /standalone_integration_arcsight/standalone_integration_arcsight.inc

.. include:: /standalone_integration_cb_response/standalone_integration_cb_response.inc

.. include:: /integration_centripetal_networks/integration_centripetal_networks.inc

.. include:: /standalone_integration_crits/standalone_integration_crits.inc

.. include:: /integration_eclecticiq/integration_eclecticiq.inc

.. include:: /integration_fireeye_security_orchestrator/integration_fireeye_security_orchestrator.inc

.. include:: /integration_ibm_qradar/integration_ibm_qradar.inc

.. include:: /standalone_integration_logrhythm/standalone_integration_logrhythm.inc

.. include:: /standalone_integration_mcafee_siem/standalone_integration_mcafee_siem.inc

.. include:: /integration_paloalto_minemeld/integration_paloalto_minemeld.inc

.. include:: /integration_phantom/integration_phantom.inc

.. include:: /integration_recorded_future/integration_recorded_future.inc

.. include:: /integration_splunk_enterprise/integration_splunk_enterprise.inc

.. include:: /integration_threatconnect/integration_threatconnect.inc

.. include:: /integration_threatquotient/integration_threatquotient.inc

.. include:: /standalone_integration_tippingpoint_ips/standalone_integration_tippingpoint_ips.inc


