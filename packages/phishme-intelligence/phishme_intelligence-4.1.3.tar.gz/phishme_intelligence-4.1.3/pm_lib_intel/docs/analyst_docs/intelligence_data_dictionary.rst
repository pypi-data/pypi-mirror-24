====================================
PhishMe Intelligence Data Dictionary
====================================

Purpose
-------

This dictionary describes the nomenclature for the PhishMe Intelligence product.

Meta Intelligence
-----------------

This data is exclusively added by PhishMe and is not available from other sources.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Threat ID
     - A unique identifier across all malware attacks recorded by PhishMe.
   * - Brand
     - The brand being imitated by this malware campaign.
   * - First Published
     - The first time this campaign was published by PhishMe.
   * - Last Published
     - The last time this campaign was published by PhishMe.
   * - Feeds
     - A list of feeds where PhishMe discovered this threat. If contractually allowed, the feed will be named. If not,
       the name shown will be PhishMe. If the threat was provided privately by your organization, you will see the name
       of your organization.
   * - Active Threat Report (URL)
     - A direct URL to a human-readable document intended to provide a more accessible explanation for the sum of a
       malware campaign’s significance.
   * - ThreatHQ (URL)
     - A direct URL to www.threathq.com for this specific Threat ID.

Subject Line(s)
---------------

This is the subject line of all malicious emails determined to be part of this campaign.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Subject
     - Email subject line.
   * - Count
     - Count of the instances of each item named above.

Sender Domains
--------------

This is the domain name of the sending address or the TO: field. These are highly likely to be spoofed and should not be relied on as the true sender.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Domain
     - Sender domain name.
   * - Count
     - Count of the instances of each item named above.

Sender Email(s)
---------------

These are the email addresses being used to deliver the mail. Due to the nature of mail headers, some of these email addresses may be spoofed.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Email
     - The possibly spoofed email address used in the delivery of the email.
   * - Count
     - Count of the instances of each item named above.

Sender IP(s)
------------

These are the IP addresses being used to deliver the mail. Due to the nature of mail headers, some of these IPs may be spoofed.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - IP Address
     - One of possibly many IPs used in the delivery of the email.
   * - Count
     - Count of the instances of each item named above.

Sender Name(s)
--------------

This is the friendly name of the sender of the email.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Name
     - The friendly name of the email sender.
   * - Count
     - Count of the instances of each item named above.

Malware Family
--------------

These are the malware family with a description of their primary function.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Name
     - Malware family name.
   * - Description
     - Primary function of this malware family.

Malware Artifacts
-----------------

These are all the files placed on an endpoint during the course of a malware infection.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Antivirus Vendor Detections
     - A list of antivirus vendors and whether or not they detected the malware artifact (per VirusTotal)
   * - Vendor Name
     - Name of vendor (per VirusTotal)
   * - Detected?
     - Whether the vendor detected the malware artifact (per VirusTotal)
   * - File Name
     - The file name of any file discovered during a malware infection.
   * - File Extension
     - The extension of the file, typically denoting the file type, but may be spoofed.
   * - MD5
     - The MD5 hash of the file named above.
   * - SHA-1
     - The SHA-1 hash of the file named above.
   * - SHA-224
     - The SHA-224 hash of the file named above.
   * - SHA-256
     - The SHA-256 hash of the file named above.
   * - SHA-384
     - The SHA-384 hash of the file named above.
   * - SHA-512
     - The SHA-512 hash of the file named above.
   * - ssdeep
     - The ssdeep hash of the file named above (http://ssdeep.sourceforge.net/)
   * - Malware Family Name
     - Malware family name.
   * - Malware Family Description
     - Primary function of this malware family.
   * - Type
     - Describes the means by which the malware artifact was introduced to the infected environment. Note: this is not a
       closed set, so new items may be added at any time.
   * - Role
     - Additional context for purpose of the infected binary within infected endpoint.

Watch List
----------

Each web location described in the set of watchlist indicators associated with a threat ID has a series of description
fields meant to provide detail about the nature of that indicator. Each of these corresponds to a finite set of possible
entries at any given time. The categories used to describe this information are as follows.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Watchlist Domain
     - A domain name indicator of compromise. Note: This category contains both second-level domains and fully qualified
       domains (FQDN). Where applicable, our analysts add an entry for both the FQDN and the second-level domain name.
       In some cases, the second-level domain may receive a lesser Impact Rating.
   * - Watchlist IPv4
     - An IPv4 address indicator of compromise.
   * - Watchlist URL
     - An URL indicator of compromise.
   * - Watchlist Type
     - Domain, IPv4, or URL.
   * - Impact Rating
     - Imparts the risk presented by communication with this indicator. This values are borrowed from the STIX Impact
       Rating Vocabulary, but their application is enhanced by the guidelines found
       :ref:`at this link <block_set_impact>`
   * - Infrastructure Type
     - Used to classify how the location is used by malware. Possible values for this field and their meanings are
       presented :ref:`at this link <block_set_role>`. Note: this is not a closed set, so new values may be added by
       PhishMe analysts at any time.
   * - Infrastructure Type Description
     - Further description about what the Infrastructure Type means. Possible values for this field and their meanings
       are presented :ref:`at this link <block_set_role_description>`. Note: this is not a closed set, so new values may
       be added by PhishMe analysts at any time.
   * - Infrastructure Type Subclass
     - Based on factors specific to the different roles assumed by network indicators, some roles have subclass
       modifiers that provide more detail about the defining characteristics of that role.
   * - ASN
     - The number which refers to a network operator.
   * - Organization
     - The long form name of the organization responsible for this ASN.
   * - Country Code
     - Two-letter country code. http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Current_codes
   * - Last Updated
     - The date when this item was added to this malware campaign.

Extracted Strings
-----------------

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - String
     - Strings which represent identifying factors unique to this incident or malware type.

Registry & System Changes
-------------------------

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Modifications
     - A list of items, both registry and file system, which were added, modified, or removed from the system during the
       course of an analysis.

