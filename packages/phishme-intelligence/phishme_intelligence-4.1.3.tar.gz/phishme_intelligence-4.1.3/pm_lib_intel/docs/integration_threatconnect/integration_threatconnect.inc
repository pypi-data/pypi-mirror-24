.. _threatconnect:

=============
ThreatConnect
=============

.. image:: /integration_threatconnect/threatconnect_logo.png
   :scale: 50%

**How to get it:** Contact your ThreatConnect Customer Success Engineer

.. rst-class:: html-toggle

Overview
--------

This ThreatConnect integration with PhishMe Intelligence maps PhishMe Intelligence into the ThreatConnect platform.
PhishMe Intelligence provides accurate and timely alerts so that you can be ready to take fast action when under attack.
PhishMe Analysts and Researchers work to analyze and verify phishing threats delivering ransomware, key loggers, RATs,
and other types of crimeware. This high-fidelity data is delivered in multiple forms to effectively prepare and respond
to attacks.

The PhishMe Intelligence integration for ThreatConnect supports the ingesting of PhishMe Intelligence into ThreatConnect
as Threats or Incidents, Documents, and Indicators. Associations are preserved between Threats/Incidents, Indicators and
Documents. Attributes and tags are used to preserve context. These Threats/Incidents, Indicators and Documents can then
be searched and integrated into a company’s existing investigations and exported to other tools for further usage.

.. rst-class:: html-toggle

Requirements
------------

   * Active ThreatConnect Application Programming Interface (API) User

.. note:: The current version of our ThreatConnect integration is 1.1.1

.. note::  All ThreatConnect dependencies will be provided by default to subscribing ThreatConnect Public Cloud
           customers. Private Instance customers can enable these settings during configuration under the Account
           Settings menu within their Private Instance of ThreatConnect.

.. rst-class:: html-toggle

Parameter Definition
--------------------

.. list-table::
    :widths: 40 60
    :header-rows: 1

    * - Name
      - Description
    * - PhishMe Intelligence Access ID
      - *Required* - This parameter is the ThreatConnect API Access ID created via the ThreatConnect Web UI.
    * - PhishMe Intelligence API Secret Key
      - *Required* - This parameter is the ThreatConnect API Secret Key created via the ThreatConnect Web UI.
    * - ThreatConnect Default Org Name
      - *Required* - This parameter is the organization name with which the incoming Indicators will be associated (we
        would recommend “PhishMe” or “PhishMe Intelligence” as the organization name for ease of use).
    * - PhishMe Intelligence API Username
      - *Required* – Username of PhishMe Intelligence API credentials that will be used
    * - PhishMe Intelligence API Password
      - *Required* – Password of PhishMe Intelligence API credentials that will be used. You can generate API
        credentials by going to https://www.threathq.com/p42/settings/apitokens.
    * - PhishMe Intelligence Initial Ingestion Date (YYYY-MM-DD)
      - *Required* – How far back to perform the initial ingestion of PhishMe Intelligence. PhishMe recommends 1 to 3
        months.
    * - PhishMe Intelligence Position
      - This parameter tracks the position this integration is at in PhishMe Intelligence after initial ingestion.
        This value could be accessed or populated for troubleshooting so it is exposed.
    * - ThreatConnect Group Type to Use
      - *Required* – Which ThreatConnect Group type to use for organizing each PhishMe Intelligence Threat ID. Choices
        are Threat or Incident (default is Threat)

.. rst-class:: html-toggle

Data Mapping
------------

.. note:: Indicators below are provided with the context that is part of PhishMe Intelligence as supported by
          ThreatConnect. Associations are generated between the Threat ID (Threat)/Document (Active Threat Report) and
          the WatchList/Malware Artifacts items (Indicators).

==================================  ====================
PhishMe Intelligence Item           ThreatConnect Mapping
==================================  ====================
Threat ID general information       Threat or Indicator
Active Threat Report for Threat ID  Document
WatchList IPv4                      Indicator of type Address
WatchList Email Addresses           Indicator of type EmailAddress
WatchList URL                       Indicator of type URL
WatchList Domain                    Indicator of type Host
Malware Artifacts                   Indicator of type File
==================================  ====================

.. rst-class:: html-toggle

Screenshots
-----------

Threats or Indicators correspond to campaigns, which are the high-level organization element for PhishMe Intelligence.
Threats or Indicators are generally associated with a Document and are associated with whatever Indicators were
generated as the result of the analysis of a particular campaign.


.. image:: /integration_threatconnect/screenshot_1.jpeg
.. image:: /integration_threatconnect/screenshot_2.png

Documents contain the Active Threat Report for a campaign and are associated with the Threat or Incident and Indicators
that make up the campaign.

.. image:: /integration_threatconnect/screenshot_3.png

Indicators are email addresses, URLs, IP addresses and files associated with a campaign. They are associated with one or
more Threats or Incidents.

.. image:: /integration_threatconnect/screenshot_4.jpeg


