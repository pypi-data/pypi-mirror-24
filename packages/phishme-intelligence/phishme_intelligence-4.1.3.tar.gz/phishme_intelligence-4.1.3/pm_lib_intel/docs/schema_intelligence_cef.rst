.. _schema_intelligence_cef:

===================================
PhishMe Intelligence Structure: CEF
===================================

===================  =======
CEF                  PhishMe
===================  =======
deviceVendor         "PhishMe"
deviceProduct        "Intelligence"
deviceVersion        "1.0"
deviceEventClassid   "malicious_file","watchlist_domain","watchlist_ip","watchlist_url"
name                 "Malicious File","Watchlist Domain","Watchlist IP","Watchlist URL"
severity             "10","7","4", or "0" according to Impact Rating
category             Impact Rating
externalId           Threat ID
deviceCustomDate1    First Published
destinationAddress   Watchlist IPv4
fileName             Malware Artifact File Name
fileHash             Malware Artifact File MD5
deviceCustomString1  Malware Family
deviceCustomString2  Brand
deviceCustomString3  Infrastructure Type
deviceCustomString4  Watchlist Domain or Watchlist URL, according to deviceEventClassid
deviceCustomString5  Threat Detail URL for this Threat ID
deviceCustomString6  Active Threat Report URL
===================  =======