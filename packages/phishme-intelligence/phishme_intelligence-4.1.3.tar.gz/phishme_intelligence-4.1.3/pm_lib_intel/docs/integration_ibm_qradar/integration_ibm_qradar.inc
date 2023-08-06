.. _qradar:

==========
IBM QRadar
==========

**Included Content:** QRadar App

**How to get it:** `IBM Security App Exchange <https://exchange.xforce.ibmcloud.com/hub/extension/4a57fd0a91c70d9be6a2705f40462477>`_

.. rst-class:: html-toggle

Overview
--------

PhishMe's IOCs are inserted into QRadar SIEM via an app installed in QRadar. These IOCs and their context are stored
directly in Reference Collections within QRadar. Both Offenses and Reports are populated with this additional context
that is stored in Reference Tables. To maximize efficiency, all content provided in this integration first queries a
Reference Set to determine if a match is present, before querying a corresponding Reference Table to gather all context.
Rules are available to create Offenses when matching data is observed within your environment. Reports can also be
scheduled to show all activity matching an IOC in QRadar or it can be limited to only events occurring prior to the IOC
being populated to the Reference Collections. This gives you protection looking into the past, as well as the future.

This integration leverages a standard created in conjunction with Ready for IBM Security Intelligence. Additional
information about this program can be found `here <https://ibm.biz/rfisi_threat_intel>`_.

.. rst-class:: html-toggle

Features
--------

**Reference Sets**

The following Reference Sets are created and populated with IOCs:

    * PhishMe_Intelligence_Malware_Hostnames
    * PhishMe_Intelligence_Malware_IPs
    * PhishMe_Intelligence_Malware_URLs
    * PhishMe_Intelligence_Malware_Hashes_MD5

.. image:: /integration_ibm_qradar/reference_sets_1.jpeg

**Reference Tables**

The following Reference Tables are created to hold extensive context about the IOCs in the above Sets. The main key in
each Reference Table is the same value as is present in the corresponding Reference Set of similar name. The reason for
the Reference Sets to exist is for the reduced lookup time to find an entry in a Set. In both Rules and Advanced Query
Language (AQL), a look up against a Reference Table should be performed only when a successful look up occurs against
the corresponding Reference Set.

.. image:: /integration_ibm_qradar/reference_tables_1.jpeg

**Rule Example**

The following rule tests are an example of ways you could do advanced correlation using IOC context. This rule will test
each source or destination IP for matches against any of our IOCs; if matched it will analyze the context to determine
the impact. Using the Reference Set first narrows the results down much more efficiently than reviewing the table for
each IP.

.. image:: /integration_ibm_qradar/rule_example_1.png

**AQL Examples**

Watchlist Domain::

    SELECT
      "Destination Host Name",
      LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'Identifier', "Destination Host Name")) AS 'Threat ID',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'Provider', "Destination Host Name") AS 'Provider',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'Impact Rating', "Destination Host Name") AS 'Impact Rating',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'Brand', "Destination Host Name") AS 'Brand',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'Malware Family', "Destination Host Name") AS 'Malware Family',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'Infrastructure Type', "Destination Host Name") AS 'Infrastructure Type',
      DATEFORMAT(LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'First Seen Date', "Destination Host Name")),'YYYY-MM-dd HH:mm:ss') AS 'First Seen Date',
      DATEFORMAT(LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'Last Seen Date', "Destination Host Name")),'YYYY-MM-dd HH:mm:ss') AS 'Last Seen Date',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'Threat Details', "Destination Host Name") AS 'Threat Details',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hostnames_Data', 'Active Threat Report', "Destination Host Name") AS 'Active Threat Report'
    FROM
      events
    WHERE
      REFERENCESETCONTAINS ('PhishMe_Intelligence_Malware_Hostnames', "Destination Host Name")

Watchlist IP::

    SELECT
      destinationip,
      LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'Identifier', destinationip)) AS 'Threat ID',
      REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'Provider', destinationip) AS 'Provider',
      REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'Impact Rating', destinationip) AS 'ImpactRating',
      REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'Brand', destinationip) AS 'Brand',
      REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'Malware Family', destinationip) AS 'Malware Family',
      REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'Infrastructure Type', destinationip) AS 'Infrastructure Type',
      DATEFORMAT(LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'First Seen Date', destinationip)),'YYYY-MM-dd HH:mm:ss') AS 'First Seen Date',
      DATEFORMAT(LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'Last Seen Date', destinationip)),'YYYY-MM-dd HH:mm:ss') AS 'Last Seen Date',
      REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'Threat Details', destinationip) AS 'Threat Details',
      REFERENCETABLE('PhishMe_Intelligence_Malware_IPs_Data', 'Active Threat Report', destinationip) AS 'Active Threat Report'
    FROM
      events
    WHERE
      REFERENCESETCONTAINS('PhishMe_Intelligence_Malware_IPs', destinationip)
      AND
      'ImpactRating' == 'Major'

Watchlist URL::

    SELECT
      URL,
      LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'Identifier', URL)) AS 'Threat ID',
      REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'Provider', URL) AS 'Provider',
      REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'Impact Rating', URL) AS 'Impact Rating',
      REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'Brand', URL) AS 'Brand',
      REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'Malware Family', URL) AS 'Malware Family',
      REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'Infrastructure Type', URL) AS 'Infrastructure Type',
      DATEFORMAT(LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'First Seen Date', URL)),'YYYY-MM-dd HH:mm:ss') AS 'First Seen Date',
      DATEFORMAT(LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'Last Seen Date', URL)),'YYYY-MM-dd HH:mm:ss') AS 'Last Seen Date',
      REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'Threat Details', URL) AS 'Threat Details',
      REFERENCETABLE('PhishMe_Intelligence_Malware_URLs_Data', 'Active Threat Report', URL) AS 'Active Threat Report'
    FROM
      events
    WHERE
      REFERENCESETCONTAINS ('PhishMe_Intelligence_Malware_URLs', URL)

Malicious MD5::

    SELECT
      "File Hash",
      LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_Hashes_MD5_Data', 'Identifier', "File Hash")) AS 'Threat ID',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hashes_MD5_Data', 'Provider', "File Hash") AS 'Provider',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hashes_MD5_Data', 'Brand', "File Hash") AS 'Brand',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hashes_MD5_Data', 'Malware Family', "File Hash") AS 'Malware Family',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hashes_MD5_Data', 'Infrastructure Type', "File Hash") AS 'Infrastructure Type',
      DATEFORMAT(LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_Hashes_MD5_Data', 'First Seen Date', "File Hash")),'YYYY-MM-dd HH:mm:ss') AS 'First Seen Date',
      DATEFORMAT(LONG(REFERENCETABLE('PhishMe_Intelligence_Malware_Hashes_MD5_Data', 'Last Seen Date', "File Hash")),'YYYY-MM-dd HH:mm:ss') AS 'Last Seen Date',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hashes_MD5_Data', 'Threat Details', "File Hash") AS 'Threat Details',
      REFERENCETABLE('PhishMe_Intelligence_Malware_Hashes_MD5_Data', 'Active Threat Report', "File Hash") AS 'Active Threat Report'
    FROM
      events
    WHERE
      REFERENCESETCONTAINS ('PhishMe_Intelligence_Malware_Hashes_MD5', "File Hash")
