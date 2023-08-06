.. _splunk_enterprise:

======
Splunk
======

.. image:: /integration_splunk_enterprise/splunk_logo.png
   :scale: 50%

.. rst-class:: html-toggle

Overview
--------

PhishMe Intelligence and Splunk partner to alert your Cyber Security Team when network communication is detected between
your endpoints and botnet infrastructures. PhishMe Intelligence provides a high-signal, context-rich source of threat
intelligence about the latest phishing and malware attacks hitting businesses, universities, and agencies every day.
PhishMe analyzes and verifies every threat before we publish the indicators so your team doesn’t waste time on false
positives.

This Add-on provided by PhishMe enables a seamless integration with Splunk Enterprise Security (Splunk ES), with just
minimal configuration. While this Add-on is produced with Splunk ES users in mind, Splunk ES is not a dependency.

The App provided by PhishMe seeks to fill a gap within Splunk ES. While Splunk ES does an excellent job at discovering
correlations between threatlist contents and enterprise data, it does not provide the context to an analyst reviewing an
alert. The App provided by PhishMe allows an analyst to perform a simple search for any IOC published by PhishMe and
quickly view all the context around that IOC. It also provides simple Drilldowns directly to PhishMe Active Threat
Reports or to view other IOCs related to the current search. The following table describes the features of PhishMe's
Intelligence products and respective Splunk App types.


.. list-table::
    :widths: 5 50 45
    :header-rows: 1
    :stub-columns: 1

    * -
      - PhishMe Intelligence
      - PhishMe Brand Intelligence
    * - Add-On
      - `PhishMe Intelligence Add-on for Splunk <https://splunkbase.splunk.com/app/3071/>`_
            * Retrieves PhishMe Intelligence from PhishMe API as JSON events.
            * Contains threatlist searches for seamless Splunk ES integration.
            * Splunk ES is *not* required.
      - `PhishMe Intelligence for Splunk <https://splunkbase.splunk.com/app/3111/>`_
            * Retrieves PhishMe Brand Intelligence from PhishMe API as JSON events.
            * Download: `PhishMe Intelligence Add-on for Splunk <https://splunkbase.splunk.com/app/3071/>`_
    * - App
      - `PhishMe Brand Intelligence Add-on for Splunk <https://splunkbase.splunk.com/app/3072/>`_
            * Contains simple search dashboard to discover context around any PhishMe Intelligence IOC.
            * Contains Pivot model for PhishMe Intelligence.
            * Requires PhishMe Intelligence Add-on for Splunk.
      -

.. rst-class:: html-toggle

Getting Started
---------------

Download and install Add-on from Splunkbase using links above.
Go to the Settings menu, then "Data inputs".

.. image:: /integration_splunk_enterprise/getting_started_1.jpeg

**If Add-On is PhishMe Intelligence Add-on for Splunk**

Select 'PhishMe Intelligence'

.. image:: /integration_splunk_enterprise/phishme_intelligence_1.jpeg

Edit the entry to add your API credentials (from https://www.threathq.com/p42/settings/apitokens). Choose which of the
following types of threat intelligence objects to ingest, which correspond to the major categories listed in the data
dictionaries.

    * JSON - raw
    * :ref:`JSON - Block set <block_set>`
    * :ref:`JSON - Executable set <executable_set>`
    * :ref:`JSON - Sender Email Address set <sender_email_set>`
    * :ref:`JSON - Sender Subject set <sender_subject_set>`

.. image:: /integration_splunk_enterprise/phishme_intelligence_2.jpeg

**(Splunk ES only)** Go to Search, Reports and Alerts, select this Add-on, and enable the Searches you want to use in
Splunk ES.

.. image:: /integration_splunk_enterprise/phishme_intelligence_3.jpeg

**(Splunk ES only)** Finally, in Splunk ES, enable the threatlists that correspond to the Searches that you enabled.

.. image:: /integration_splunk_enterprise/phishme_intelligence_4.jpeg

**If Add-On is PhishMe Brand Intelligence Add-on for Splunk**

Select 'PhishMe Brand Intelligence'.

.. image:: /integration_splunk_enterprise/phishme_brand_intelligence_1.jpeg

Edit the entry to add your API credentials (from https://www.threathq.com/p42/settings/apitokens). Choose which of the
following types of threat intelligence objects to ingest, which correspond to the major categories listed in the data
dictionaries.

    * JSON - raw
    * :ref:`JSON - Action URLs <action_urls>`
    * :ref:`JSON - Reported URLs <reported_urls>`
    * :ref:`JSON - Kits <kits>`
    * :ref:`JSON - Kit Files <kit_files>`
    * :ref:`JSON - Web Components <web_components>`
    * :ref:`JSON - Phish URL <phish_urls>`

.. image:: /integration_splunk_enterprise/phishme_brand_intelligence_2.jpeg

The API Username and Password are generated at https://www.threathq.com/p42/settings/apitokens. The 'Start Date'
dictates how much data will be loaded by the Add-on during its first successful execution. If a proxy is needed to
connect to PhishMe, please change the "Use Proxy?" value to True and fill out your proxy information in the following
two fields. You may also wish to change the index where this data will be stored. Don't forget to enable the modular
input after you've configured it. For PhishMe Intelligence blocklist items (that is, outbound network IOCs), there are 4
independent Search/threatlist combinations according to the Impact Rating assigned to the IOC. Simply enable the IOC
type and Impact Rating appropriate for your environment.

.. rst-class:: html-toggle

Features
--------

**PhishMe Intelligence Add-On for Splunk**

This Add-On ingests JSON data from PhishMe's API and indexes it. It also allows simple integration with Splunk ES, if
present. Without Splunk ES, you can build your own correlations with this data. The following screenshots show how this
data is structured:

.. image:: /integration_splunk_enterprise/phishme_intelligence_features_1.jpeg
   :scale: 15%

.. image:: /integration_splunk_enterprise/phishme_intelligence_features_2.jpeg
   :scale: 15%

.. image:: /integration_splunk_enterprise/phishme_intelligence_features_3.jpeg
   :scale: 15%

.. image:: /integration_splunk_enterprise/phishme_intelligence_features_4.jpeg
   :scale: 15%

.. image:: /integration_splunk_enterprise/phishme_intelligence_features_5.jpeg
   :scale: 15%

**PhishMe Intelligence for Splunk**

**Search Dashboard**

By default, Splunk ES does not show any context about the IOC that caused a Notable Event. If you wish to see the
additional context provided by PhishMe, the following Dashboard provides a simple interface for viewing these details.

.. image:: /integration_splunk_enterprise/phishme_intelligence_features_6.jpeg

**Pivot Model**

A pivot model is available for reporting or trending research across PhishMe Intelligence data.

.. image:: /integration_splunk_enterprise/phishme_intelligence_features_7.jpeg

**Workflow Action**

Two Event Actions are available for any of the events published by PhishMe. These Event Actions lead directly to the
relevant Active Threat Report for a deeper understanding of the overall malicious campaign or Threat Details page for
additional research.

.. image:: /integration_splunk_enterprise/phishme_intelligence_features_8.jpeg

.. rst-class:: html-toggle

Useful Queries
--------------

This query shows logs from the modular input.::

   index=_internal sourcetype="splunkd" source="/opt/splunk/var/log/splunk/splunkd.log" TA-phishmeintelligence NOT "CSV header"

This query shows Threat IDs and their date of first publication by PhishMe.::

   index=phishme | dedup id | table _time, id | sort id desc

