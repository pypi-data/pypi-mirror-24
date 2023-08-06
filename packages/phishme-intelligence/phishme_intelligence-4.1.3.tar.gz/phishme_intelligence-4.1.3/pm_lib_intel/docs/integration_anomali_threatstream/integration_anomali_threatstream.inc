.. _anomali_threatstream:

====================
Anomali Threatstream
====================

.. image:: /integration_anomali_threatstream/anomali_logo.png

**How to get it:** Contact Anomali support

.. rst-class:: html-toggle

Overview
--------

This Anomali ThreatStream integration with PhishMe Intelligence maps PhishMe Intelligence into the ThreatStream
platform.  PhishMe Intelligence provides accurate and timely alerts so that you can be ready to take fast action when
under attack. PhishMe Analysts and Researchers work to analyze and verify phishing threats delivering ransomware, key
loggers, RATs, and other types of crimeware. This high-fidelity data is delivered in multiple forms to effectively
prepare and respond to attacks.

The PhishMe Intelligence integration for Anomali Threatstream supports the ingesting of PhishMe Intelligence into
ThreatStream as a collection of Observables iTypes. Tags are used to associate Observables and preserve as much context
as possible. These Observables can then be searched and integrated into a company’s existing investigations and exported
to other tools for further usage.

 .. rst-class:: html-toggle

Requirements
------------

All PhishMe Intelligence customers who use Anomali ThreatStream will need to reach out to Anomali support to get
PhishMe Intelligence activated within their ThreatStream instance. Anomali will provide specific guidance for any other
steps that are required.

.. rst-class:: html-toggle

Data Mapping
------------

=========================     ==========================
PhishMe Intelligence Item     ThreatStream iType Mapping
=========================     ==========================
WatchList IPv4                Malware C&C IP
WatchList URL                 Malware C&C URL
WatchList Domain              Malware C&C Domain Name
Malware MD5, SHA1, SHA256     Malware File Hash
Malware ssdeep                Malware SSDeep Hash
=========================     ==========================

.. rst-class:: html-toggle

Screenshots
-----------

Observables within ThreatStream:

.. image:: /integration_anomali_threatstream/anomali_screenshot_1.png

Association between an Observable and other Observables via tags:

.. image:: /integration_anomali_threatstream/anomali_screenshot_2.png
