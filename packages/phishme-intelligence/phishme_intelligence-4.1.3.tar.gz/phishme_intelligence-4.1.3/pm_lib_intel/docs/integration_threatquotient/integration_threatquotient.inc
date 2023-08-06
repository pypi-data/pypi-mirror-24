.. _threatq:

================
ThreatQ Platform
================

.. image:: /integration_threatquotient/threatquotient_logo.png
   :scale: 50%

.. rst-class:: html-toggle

Overview
--------

This ThreatQ integration with PhishMe Intelligence maps PhishMe Intelligence into the ThreatQ platform. PhishMe
Intelligence provides accurate and timely alerts so that you can be ready to take fast action when under attack.
PhishMe Analysts and Researchers work to analyze and verify phishing threats delivering ransomware, key loggers, RATs,
and other types of crimeware. This high-fidelity data is delivered in multiple forms to effectively prepare and respond
to attacks.

The PhishMe Intelligence integration for the ThreatQ platform supports the ingesting of PhishMe Intelligence into
ThreatQ as Events, Files and Indicators (see below for more details on mapping). Relationships (links) are created
between a Event and it's File and Indicators. Attribute values for all of these times are used to help preserve context.
These values can be searched and integrated into a company's existing investigations and indicators can be exported to
other tools for further usage.


.. rst-class:: html-toggle

Setting up Integration
----------------------

Login to your ThreatQ platform instance; click the gear icon in the upper-right hand corner of the interface and go to
** Threat Q Configuration > Incoming Feeds**.

.. image:: /integration_threatquotient/threatquotient_setup_1.png

In the Incoming Feeds window scroll down to the PhishMe Intelligence feed and expand the Feed Settings interface.

.. image:: /integration_threatquotient/threatquotient_setup_2.png

Under the Connection settings set the API ID and API Key (API credentials can be generated
`with your PhishMe Intelligence account <https://www.threathq.com/p42/settings/apitokens>`_).

.. image:: /integration_threatquotient/threatquotient_setup_3.png

Under the Settings settings make sure Indicator Status is set to Active and update frequency is set to Every Hour.

.. image:: /integration_threatquotient/threatquotient_setup_4.png

Toggle the slider button to activate the PhishMe Intelligence feed (turn the slider green).

.. image:: /integration_threatquotient/threatquotient_setup_5.png

.. rst-class:: html-toggle

Data Mapping
------------

==================================  ====================
PhishMe Intelligence Item           ThreatQ Platform Mapping
==================================  ====================
Threat ID general information       Event
Active Threat Report for Threat ID  File
WatchList IPv4                      Indicator with type IP Address
WatchList Email Addresses           Indicator with type Email Address
WatchList URL                       Indicator with type URL
WatchList Domain                    Indicator with type FQDN
Malware Artifacts                   Indicators with types MD5, SHA-1, SHA-256, SHA-384, SHA-512 and Fuzzy Hash (ssdeep)
==================================  ====================

.. rst-class:: html-toggle

Screenshots
-----------

Screenshots pending.

