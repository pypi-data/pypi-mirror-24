==========================================
PhishMe Brand Intelligence Data Dictionary
==========================================

Purpose
-------

This dictionary describes the nomenclature for the PhishMe Brand Intelligence product.

Important Terms
---------------

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Phishing
     - The act of attempting to steal login credentials or personally identifiable information (PII) via a webpage
       designed to trick a victim into believing they're interacting with a legitimate website.
   * - Phishing site
     - Fake webpage(s) designed to trick a victim into providing credentials and PII. This can be either a legitimate
       website that has been compromised or a website specifically registered for the purpose of phishing.
   * - Phishing kit
     - A collection of files, typically distributed within a zip archive. Extracting the contents of this archive
       creates a phishing site. Typically, the only necessary configuration is modifying the drop email address to an
       email address controlled by the criminal.
   * - Drop email
     - An email address used within a phishing kit or site that will receive victim information when a victim submits
       that information to the phishing site.
   * - Exit URL
     - The last URL a phishing kit will send a victim to. This is often the legitimate web site of the brand being
       imitated by the phishing site. This is not necessarily the same as the location where a victim's browser will
       land, as there may be some intermediate redirection on the part of the legitimate website. For example, the Exit
       URL may be a portion of legitimate site no longer in use, so the legitimate brand will automatically redirect the
       victim to the legitimate site's home page or login page.

Meta Intelligence
-----------------

This data is exclusively added by PhishMe and is not available from other sources.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Threat ID
     - A unique identifier across all phishing attacks recorded by PhishMe.
   * - Brand
     - The brand being imitated by this phishing attack. Typically an online service provider.
   * - Feeds
     - A list of feeds where PhishMe discovered this threat. If contractually allowed, the feed will be named. If not,
       the name shown will be PhishMe. If the threat was provided privately by your organization, you will see the name
       of your organization.
   * - Confirmed Date
     - The time when this phish was confirmed as being a phishing threat.
   * - First Seen Date
     - The first time this phishing URL was ingested by PhishMe.
   * - Last Seen Date
     - The most recent time this phishing URL was ingested by PhishMe. Note, if a phishing URL already processed by
       PhishMe is seen again, retrieval of content found at that phishing URL is not performed. Only this timestamp is
       updated.
   * - Phishing Page HTML Title
     - The text from the raw HTML used to display the phishing URL, typically found within the <title> </title> tags.
       This is the text displayed by a browser at the top of the browser or tab.
   * - Screenshot (URL)
     - A screenshot captured of the phishing URL. If you were to visit the phishing URL directly, you should expect the
       same visual experience as you see in this screenshot.
   * - ThreatHQ (URL)
     - A direct URL to www.threathq.com for this specific Threat ID.

Language
--------

The primary language used in the visible portions of the phishing site, as determined by an NLP library.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Family
     - Family classification for this language.
   * - ISO Code
     - Two-letter code for this language.
   * - Name
     - The primary language used within this phishing threat.
   * - Native Name
     - Non-English name for this language.
   * - Probability
     - The statistical likelihood the assigned language is correct.

Reported URL
------------

This is the original URL reported to PhishMe. It might be the same as the Phishing URL or it might be a re-director of
some type, either a compromised site or a shortened URL like bit.ly or tinyurl.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Domain
     - The domain extracted from the Reported URL.
   * - Host
     - The host name plus the domain name extracted from the Reported URL. This is the same as the FQDN.
   * - Path
     - The relative URI for this URL
   * - Protocol
     - The standard method of information transfer and processing.
   * - URL
     - The original URL as reported to PhishMe.
   * - WHOIS
     - WHOIS information for the registered domain in the Reported URL.

Phishing URL
------------

These components represent the current location of a phishing page, whether hosted on a compromised website or a domain
specifically registered for phishing purposes.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Domain
     - The domain extracted from the full URL.
   * - Host
     - The host name plus the domain name extracted from the full URL. This is the same as the FQDN.
   * - IPv4
     - The IPv4 address of the hostname used to host the phishing site as resolved by DNS lookup.
   * - Path
     - The relative URI for this URL
   * - Protocol
     - The standard method of information transfer and processing.
   * - URL
     - The full URL to the landing page of the phishing website.
   * - WHOIS
     - A WHOIS record for the domain as recorded when this threat was initially confirmed as a phish.

Action URL
----------

This is the next URL to be called when the victim submits their information to the phishing site. It might lead directly
to a second page of the phishing site, it might be an intermediate PHP script that submits credentials to the criminal,
it might lead to an exit URL, or it may be some combination of these things. Note: each page of a phishing attack will
have an action URL, PhishMe is only capturing the Action URL for the first page.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Domain
     - The domain extracted from the Action URL.
   * - Host
     - The host name plus the domain name extracted from the Action URL. This is the same as the FQDN.
   * - IPv4
     - The IPv4 address of the hostname used to host the phishing site as resolved by DNS lookup.
   * - Path
     - The relative URI for this URL
   * - Protocol
     - The standard method of information transfer and processing.
   * - URL
     - The full URL to the landing page of the phishing website.
   * - WHOIS
     - A WHOIS record for the domain as recorded when this threat was initially confirmed as a phish.

ASN
---

http://en.wikipedia.org/wiki/Autonomous_System_Number

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - ASN
     - The number which refers to a network operator.
   * - Organization (long)
     - The long form name of the organization responsible for this ASN.
   * - Continent Code
     - Two-letter continent code. Watch out for 'AQ'.
   * - Continent Name
     - Continent name.
   * - Country Code
     - Two-letter country code. http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Current_codes
   * - Country Name
     - Country name.
   * - Last Updated
     - The timestamp when ASN information was retrieved about the IP address to which it is associated with.
   * - Metro Code
     - Telephone metro code.
   * - Time Zone
     - Time zone.
   * - ISP
     - ISP
   * - Latitude
     - Latitude of ISP.
   * - Longitude
     - Longitude of ISP.
   * - Organization (Short)
     - The short form name of the organization responsible for this ASN.
   * - Postal Code
     - Postal or zip code.
   * - Subdivision ISO Code
     - Two-letter state code.
   * - Subdivision Name
     - State name.
   * - User Type
     - Type of user.

Web Components
--------------

These are the web components used to build a phishing website within a victim's browser. This collection of files can
include files like javascript, cascading style sheets, or images hosted by the legitimate website of the targeted brand.
These cases are excellent opportunities for the targeted brand to retrieve referral logs which will reveal the victim's
IP as they access a phishing site. Criminals may choose to reference these files hosted by the legitimate website for
simplicity or to keep the look and feel of their phishing site equivalent to the legitimate site they're imitating.
These files are downloadable as a single encrypted archive.


.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Domain
     - The domain to the resource being used in the phishing site.
   * - Host
     - The host to the resource being used in the phishing site.
   * - Path
     - The relative URI for this URL
   * - Protocol
     - The standard method of information transfer and processing.
   * - URL
     - The full URL to the resource being used in the phishing site.
   * - MD5
     - The MD5 of the retrieved resource.
   * - File Extension
     - The extension of the file, typically denoting the file type, but may be spoofed.
   * - File Name
     - The file name of the resource.
   * - File Size
     - The file size of the resource, in bytes.
   * - SHA-1
     - The SHA-1 hash of the retrieved resource.
   * - SHA-224
     - The SHA-224 hash of the retrieved resource.
   * - SHA-256
     - The SHA-256 hash of the retrieved resource.
   * - SHA-384
     - The SHA-384 hash of the retrieved resource.
   * - SHA-512
     - The SHA-512 hash of the retrieved resource.

Phish Kits
----------

These are the phishing kits retrieved during our processing of a phishing site. These kits are downloadable from the
PhishMe Intelligence portal as a single encrypted archive.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - File Name
     - The file name of the archive containing files to create a phishing site.
   * - File Size
     - The file size of the phishing kit, in bytes.
   * - MD5
     - The MD5 hash of the retrieved resource.
   * - SHA-1
     - The SHA-1 hash of the retrieved resource.
   * - SHA-224
     - The SHA-224 hash of the retrieved resource.
   * - SHA-256
     - The SHA-256 hash of the retrieved resource.
   * - SHA-384
     - The SHA-384 hash of the retrieved resource.
   * - SHA-512
     - The SHA-512 hash of the retrieved resource.

Phish Kits: Drop Email Addresses
--------------------------------

Email addresses found within a phishing kit. These are typically drop email addresses, but may include any email
addresses found within the body of the phishing kit. Reasons for the presence of a non-drop email address include
contact info for the phishing kit creator, contact info for the author of a particular script within the phishing site,
or the spoofed "from" email address that will be used to create the email to the criminal.

.. list-table::
   :widths: 20 80
   :stub-columns: 1

   * - Email
     - The email address discovered within this phishing kit.
   * - Type
     - Values include "Drop", "From", "Inactive Drop", or "Other".
   * - MD5
     - The MD5 of the phishing kit that contained this email address.
   * - File Extension
     - The extension of the file, typically denoting the file type, but may not truthfully represent the contents of the file.
   * - File Name
     - The file name of the resource.
   * - File Path
     - The relative path within the phishing kit to the file where the email address is located.
   * - File MD5
     - The MD5 hash of the file where the email was discovered.
   * - File SHA-1
     - The SHA-1 hash of the file where the email was discovered.
   * - File SHA-224
     - The SHA-224 hash of the file where the email was discovered.
   * - File SHA-256
     - The SHA-256 hash of the file where the email was discovered.
   * - File SHA-384
     - The SHA-384 hash of the file where the email was discovered.
   * - File SHA-512
     - The SHA-512 hash of the file where the email was discovered.
   * - Obfuscation Method
     - The method used to store the email address within a phishing kit. Options include plaintext, hex, NUXI
       (reverse hex), base 64, PHP arrays, PHP variable concatenation, or some combination of these methods.

