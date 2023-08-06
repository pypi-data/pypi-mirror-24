.. _rest_api_reference:

==================
REST API Reference
==================

This is documentation for the PhishMe Intelligence REST API. Most customers will not have to access this directly and
should instead use an existing PhishMe Intelligence integration (see :ref:`integrations`) or build a custom integration
using our Python module (see :ref:`library_reference` and :ref:`library_usage`).

Getting Started
---------------

**Request credentials**

Login to https://threathq.com and go to the Settings menu on the left navigation bar. Choose the API Tokens tab and
select Add a New Token. Make sure to save the password, as it will not be accessible again.

**Verify proxy**

.. note:: With any of our integrations, or if you're creating it on your own, do not set a polling interval to less than
          15 minutes.

If you'll be accessing the API from behind a proxy, you'll need to incorporate it into your code::

    import requests
    host = 'https://www.threathq.com/apiv1/feed/'
    proxies = {
      "http": "http://10.10.1.10:3128",
      "https": "http://10.10.1.10:1080",
    }
    r = requests.get(host, proxies=proxies)

**Support**

We have dedicated staff to assist you with achieving successful implementations. Please contact us at support@phishme.com.

General Info
------------

**Base API URL**

https://www.threathq.com/apiv1

**Typical Responses**

The API response format is a JSON object containing the following two properties unless a formatted document or binary
object is requested:

* **success**: A boolean representing the success or failure of the request.
* **data**: The requested data provided in the response.

**HTTP Status Codes**

PhishMe's API follows the specifications outlined in `RFC-2616 Section 10 <http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html>`_,
which outline the HTTP status codes a client can receive on making a web request. While not all situations can be documented,
the following represents the most commonly received status codes that may be received by a client of our API along with
their definitions. In cases of non-200 responses, our API will attempt to provide a meaningful error message in JSON.

============= ===========
HTTP Response Description
============= ===========
200           Successful Request
400           Bad request due to malformed syntax
401           Failed to authorize
404           Requested data not found
5xx           Server error
============= ===========

Feed
----

.. _feed:

**GET /feed/{feed_id}**

**Description**: The ThreatHQ® API allows you to request information about specific data feeds available to you. When
submitting phishing URLs or other data to the system, you can then associate the data with a particular feed to keep the
data private or make it public. You will only be able to see feeds and threats discovered from feeds that your
organization has READ access to. The WRITE permission must be true if you wish to submit potential threats on a given
feed through the API or ThreatHQ® . The OWNER permission indicates that this feed is provided by your organization.

**Response Description**: A JSON list of feeds to which your account has access.

**Parameters:**

========= ==== ========= =======
Parameter Type Data Type Details
========= ==== ========= =======
feed_id   path integer   Optional - If provided, specific feed details will be returned. If omitted, information about all feeds available to you will be returned.
========= ==== ========= =======

**Python Sample Code**::

    import requests
    host = 'https://www.threathq.com/apiv1/feed/'
    r = requests.get(host, auth=auth)
    print r.json()

    # Response
    {
        "success" : true,
        "data" : [ {
        "id" : 30,
        "permissions" : {
            "READ" : true,
            "OWNER" : false,
            "WRITE" : false
        },
        "displayName" : "PhishMe"
        }, ... ]
    }

Screenshot
----------

**GET /screenshot/{threat_id}**

**Description**: The ThreatHQ® API allows you to request PhishMe Brand Intelligence screenshots.

**Response Description**: A PNG image in bytecode.

**Parameters:**

========= ==== ========= =======
Parameter Type Data Type Details
========= ==== ========= =======
threat_id path integer   Required - The numeric id of the desired PhishMe Brand Intelligence.
========= ==== ========= =======

**Python Sample Code**::

    import requests
    host = 'https://www.threathq.com/apiv1/screenshot/6258068'
    auth=('api_username', 'api_token')
    r = requests.get(host, auth=auth)
    f = open('screenshot.png', 'wb')
    f.write(r.content)
    f.close()

T3
--

**GET /t3/malware/{threat_id}/{format}**

**Description**: The ThreatHQ® API allows you to retrieve individual PhishMe Intelligence reports, in a variety of
formats for direct integration with your SIEM, firewall, IDS, and other edge devices. Currently supported formats are
CEF, HTML, PDF, and STIX.

**Response Description**: A single object representation of a PhishMe Intelligence report in one of a variety of formats.

**Parameters:**

========= ==== ========= =======
Parameter Type Data Type Details
========= ==== ========= =======
format    path string    Required - The format to be returned ['cef', 'html', 'pdf', 'stix'].
threat_id path integer   Required - The Threat ID to return.
========= ==== ========= =======

**GET /t3/phish/{threat_id}/{format}**

**Description**: The ThreatHQ® API allows you to retrieve individual PhishMe Brand Intelligence reports, in a variety of
formats for direct integration with your SIEM, firewall, IDS, and other edge devices. Currently supported formats are
CEF and STIX.

**Response Description**: A single object representation of a PhishMe Brand Intelligence report in one of a variety of
formats.

**Parameters:**

========= ==== ========= =======
Parameter Type Data Type Details
========= ==== ========= =======
format    path string    Required - The format to be returned ['cef', 'stix'].
threat_id path integer   Required - The Threat ID to return.
========= ==== ========= =======

**GET /t3/{format}**

**Description**: The ThreatHQ® API allows you to retrieve aggregated PhishMe Intelligence and/or PhishMe Brand
Intelligence reports, in a variety of formats for direct integration with your SIEM, firewall, IDS, and other edge
devices. Currently supported formats are CEF, HTML, and PDF.

**Response Description**: An aggregated object representation of a PhishMe Intelligence or PhishMe Brand Intelligence
report, in one of a variety of formats.

**Parameters:**

============== ===== ========= =======
Parameter      Type  Data Type Details
============== ===== ========= =======
beginTimestamp query integer   Optional - The seconds since epoch from which we should start returning data. If omitted, the current time minus 24 hours is used as the default.
endTimestamp   query integer   Optional - The seconds since epoch from which we should end returning data. If omitted, the current time is used as the default.
format         path  string    Required - The format to be returned ['cef', 'stix', 'pdf'].
============== ===== ========= =======

**Python Sample Code**::

    import requests
    host = 'https://www.threathq.com/apiv1/t3/cef'
    payload = {'beginTimestamp': 1404950400, 'endTimestamp': 1405382400}
    auth=('api_username', 'api_token')
    r = requests.post(host, params=payload, auth=auth)
    f = open('2014-07-10_2014-07-15_mrti.cef', 'wb')
    f.write(r.content)
    f.close()

Threat
------

**POST /threat/phish**

**Description**: The ThreatHQ® API allows you to submit suspicious URLs for analysis as part of PhishMe Brand
Intelligence. See :ref:`Feed <feed>` to determine the correct feed for phish submission by your organization.

**Response Description**: A JSON object containing information indicating whether the URL was successfully submitted to
the system.  Once the URL has been processed, analyzed and confirmed as a phishing website it will become visible
through the /threat/search endpoint.

**Parameters:**

========= ===== ========= =======
Parameter Type  Data Type Details
========= ===== ========= =======
feed      query integer   Optional - The numeric id of the feed you wish to submit this suspicious URL to. If omitted, the default is the public PhishMe feed.
phishURL  query string    Required - The url that you wish to submit to the system. This must be prefixed with one of "http://, https://, hxxp:// or hxxps://" and be a valid URL in order be accepted by the API.
========= ===== ========= =======

**Python Sample Code**::

    import requests
    host = 'https://www.threathq.com/apiv1/threat/phish'
    auth=('api_username', 'api_token')
    payload = {'phishURL': 'http://downloadpdf.lixter.com/secure/cecaccountstatement/PDF.html'}
    r = requests.post(host, params=payload, auth=auth)
    print r.json()

    # Response
    {
      "success" : true,
      "data" : {
        "urlCount" : 1
      }
    }

**GET /threat/malware/{threat_id}**

**Description**: The ThreatHQ® API allows you to request details about an individual PhishMe Intelligence campaign.

**Response Description**: A JSON object representing a single PhishMe Intelligence campaign. A schema is located here:
:ref:`schema_intelligence_json`

**Parameters:**

========= ==== ========= =======
Parameter Type Data Type Details
========= ==== ========= =======
threat_id path integer   Required - The numeric id of the PhishMe Intelligence.
========= ==== ========= =======

**Python Sample Code**::

    import requests
    host = 'https://www.threathq.com/apiv1/threat/malware/2000'
    auth=('api_username', 'api_token')
    r = requests.get(host, auth=auth)
    print r.json()

    # Response
    {
      "success" : true,
      "data" : {
        "id" : 2000,
        "blockSet" : [ {
          "blockType" : "IPv4 Address",
          "impact" : "Minor",
          "data" : "124.217.198.156"
        }, {
          "blockType" : "URL",
          "impact" : "Major",
          "data" : "http://iloveberniemovie.ru/it.png"
        }, {
          "blockType" : "Domain Name",
          "impact" : "Major",
          "data" : "iloveberniemovie.ru"
        } ],
        "campaignBrandSet" : [ ],
        "extractedStringSet" : [ {
          "data" : ".Type = 1"
        }, {
          "data" : "Set yD85t9TF = CreateObject(\u0022WScript.Shell\u0022)"
        },
        ...
        ],
        "domainSet" : [ {
          "totalCount" : 4,
          "domain" : "aussie-models.com"
        }, {
          "totalCount" : 1,
          "domain" : "comune.brez.tn.it"
        }, {
          "totalCount" : 1,
          "domain" : "rdt.lelycenter.com"
        }, {
          "totalCount" : 2,
          "domain" : "simgt.it"
        }, {
          "totalCount" : 1,
          "domain" : "tx.rr.com"
        } ],
        "executableSet" : [ {
          "fileName" : "Guida.doc",
          "type" : "Attachment",
          "dateEntered" : 1409757764246,
          "md5Hex" : "aedd44bf6df7130601c4e5af52dfd838"
        }, {
          "fileName" : "it.png",
          "type" : "Download",
          "dateEntered" : 1409757764246,
          "md5Hex" : "4c61f9942e16c774646613869de9093f"
        } ],
        "senderIpSet" : [ {
          "totalCount" : 1,
          "ip" : "2.229.113.86"
        },
        ...
        ],
        "spamUrlSet" : [ ],
        "subjectSet" : [ {
          "totalCount" : 1,
          "subject" : "Aggiornamento: 319030972"
        },
        ...
        ],
        "createdOn" : 1409757764246,
        "lastUpdated" : 1409757764246,
        "lastPublished" : 1409757764463,
        "firstPublished" : 1409757764463,
        "label" : "ItalianWarning",
        "description" : "Word Doc, VB Downloader",
        "filename" : "2014-09-03.ItalianWarning",
        "feeds" : [ {
          "id" : 23,
          "permissions" : {
            "WRITE" : false,
            "READ" : true,
            "OWNER" : false
          },
          "displayName" : "PhishMe"
        } ]
      }
    }

**GET /threat/phish/{threat_id}**

**Description**: The ThreatHQ® API allows you to request details about an individual PhishMe Brand Intelligence report.

**Response Description**: A JSON object representing a single PhishMe Brand Intelligence report. A schema is located here:
:ref:`schema_brand_intelligence_json`

**Parameters:**

========= ==== ========= =======
Parameter Type Data Type Details
========= ==== ========= =======
threat_id path string    Required - The numeric id of the PhishMe Brand Intelligence.
========= ==== ========= =======

**Python Sample Code**::

    import requests
    host = 'https://www.threathq.com/apiv1/threat/phish/6360283'
    auth=('api_username', 'api_token')
    r = requests.get(host, auth=auth)
    print r.json()

    # Response
    {
      'success': True,
      'data': {
        'phishingURL': 'http://accezzlogzsin.a78.org/verify.htm',
        'reportedURLs': ['http://accezzlogzsin.a78.org/verify.htm'],
        'isConfirmedPhishingWebsite': 'YES',
        'screenshot': {
          'url': 'https://www.threathq.com/apiv1/screenshot/6360283'
        },
        'actionURLs': ['http://accezzlogzsin.a78.org/verified.php'],
        'ipDetail': {
          'countryName': 'United States',
          'ip': '93.188.160.75',
          'isp': 'Hostinger International Limited',
          'countryIsoCode': 'US',
          'lookupOn': 1416410397799,
          'longitude': -97.0,
          'continentName': 'North America',
          'userType': 'hosting',
          'latitude': 38.0,
          'organization': 'Hostinger International Limited',
          'asnOrganization': 'Hostinger International Limited',
          'asn': 47583,
          'continentCode': 'NA'
        },
        'confirmedDate': 1416410398164,
        'processingState': 'ANALYZED',
        'brands': [{
          'text': 'Generic Threat',
          'id': 915
        }],
        'feeds': [{
          'displayName': 'ThreatHQ',
          'id': 20,
          'permissions': {
            'WRITE': True,
            'READ': True,
            'OWNER': True
          }
        }],
        'id': 6360283
      }
    }

**POST /threat/search**

**Description**: The ThreatHQ® API enables users to search for specific threats. This search interface will only return
confirmed PhishMe Intelligence or PhishMe Brand Intelligence threats.

**Response Description**: A JSON object representing a combination of PhishMe Intelligence or PhishMe Brand Intelligence.
See :ref:`schema_brand_intelligence_json` or :ref:`schema_intelligence_json` for more details.

**Parameters:**

.. list-table::
    :widths: 10, 5, 5, 70, 10
    :header-rows: 1

    * - Parameter
      - Type
      - Data Type
      - Details
      - JSON Element Searched
    * - threatType
      - query
      - string
      - Optional - Choose whether to search for phishing attacks, malware campaigns, or both. If omitted, the default
        value is 'all'. Possible values are ['all', 'malware', 'phish'].
      -
    * - page
      - query
      - integer
      - Optional - Choose whether to search for phishing attacks, malware campaigns, or both. If omitted, the default
        value is 'all'. Possible values are ['all', 'malware', 'phish'].
      -
    * - resultsPerPage
      - query
      - integer
      - Optional - Choose whether to search for phishing attacks, malware campaigns, or both. If omitted, the default
        value is 'all'. Possible values are ['all', 'malware', 'phish'].
      -
    * - threatId
      - query
      - string
      - Optional - The unique identifier for a threat, the format of this value is a prefix of either a "p\_" for phish
        (PhishMe Brand Intelligence) or "m\_" for malware (PhishMe Intelligence) followed by the threatNativeId value.
        This may be specified multiple times.
      - [id]
    * - threatNativeId
      - query
      - integer
      - Optional - The numeric native id of a given threat. The threatNativeId and threatType make up a unique key
        for any individual threat.
      - [id]
    * - beginTimestamp
      - query
      - integer
      - Optional - The seconds since epoch from which we should start returning data.
      -
    * - endTimestamp
      - query
      - integer
      - Optional - The seconds since epoch from which we should end returning data.
      -
    * - extractedString
      - query
      - integer
      - Optional - Search for extracted strings discovered within malware campaigns.
      - [extractedStringSet][][data]
    * - malwareSenderName
      - query
      - integer
      - Optional - Search for the sender name of malware campaigns.
      - [senderNameSet][][name]
    * - malwareSubject
      - query
      - string
      - Optional - Search the message subject associated with malware campaigns.
      - [subjectSet][][subject]
    * - dropMail
      - query
      - string
      - Optional - Search drop mail addresses associated with threats.
      - [kits][][observedEmails][][email]
    * - phishingASN
      - query
      - integer
      - Optional - Search the ASN associated with a phishing threat.
      - [ipDetail][asn]
    * - phishingASNCountryCode
      - query
      - string
      - Optional - Search the country code associated with phishing threats.
      - [ipDetail][countryIsoCode]
    * - phishingASNOrganization
      - query
      - string
      - Optional - Search the ASN organization associated with phishing threats.
      - [ipDetail][asnOrganization]
    * - brand
      - query
      - string
      - Optional - This may be specified multiple times. Search for brands associated with a threat. This search
        criteria must match the exact brand name used to categorize a threat within PhishMe.
      - [campaignBrandSet][][brand][][text]
    * - kitMD5
      - query
      - string
      - Optional - May be specified multiple times. Search for threats associated with the provided kit md5.
      - [kits][][md5]
    * - malwareArtifactMD5
      - query
      - string
      - Optional - May be specified multiple times. Search for threats associated with the provided malware artifact
        md5.
      - [executableSet][][md5Hex]
    * - webComponentMD5
      - query
      - string
      - Optional - May be specified multiple times. Search for threats associated with the provided web component md5.
      - [webComponents][][md5]
    * - allMD5
      - query
      - string
      - Optional - May be specified multiple times. Search for threats associated with the provided md5.
      -
    * - hasKit
      - query
      - boolean
      - Optional - Search for threats which have an associated kit. Expected values are ['true', 'false'].
      -
    * - urlSearch
      - query
      - string
      - Optional - A specific url to search for, this supports exact and partial matching of urls.
      -
    * - threatUrlSearch
      - query
      - string
      - Optional - This may be specified multiple times. A specific url to search for, this supports exact matching if
        the url is enclosed in double quotes and partial matching otherwise.
      - [blockSet][][data_1][url]
    * - reportedUrlSearch
      - query
      - string
      - Optional -  This may be specified multiple times. A specific url to search for, this supports exact matching if
        the url is enclosed in double quotes and partial matching otherwise.
      - [reportedURLs_1][url]
    * - actionUrlSearch
      - query
      - string
      - Optional -  This may be specified multiple times. A specific url to search for, this supports exact matching if
        the url is enclosed in double quotes and partial matching otherwise.
      - [actionURLs_1][url]
    * - malwareWatchListUrlSearch
      - query
      - string
      - Optional -  This may be specified multiple times. A specific url to search for, this supports exact matching if
        the url is enclosed in double quotes and partial matching otherwise.
      - [blockSet][][data_1][url]
    * - threatIp
      - query
      - string
      - Optional - This may be specified multiple times. The IP address of the phishing threat.
      - [ipDetail][ip]
    * - malwareSenderIp
      - query
      - string
      - Optional - This may be specified multiple times. The IP address of the sender of a malware campaign.
      - [senderIpSet][][ip]
    * - malwareWatchListIp
      - query
      - string
      - Optional - This may be specified multiple times. The IP address of a watch list item associated with a malware
        campaign.
      - [blockSet][][ipDetail][ip]
    * - ip
      - query
      - string
      - Optional - This may be specified multiple times. The IP address associated with a phishing or malware campaign.
      -
    * - threatDomain
      - query
      - string
      - Optional - This may be specified multiple times. The domain name associated with a phishing threat.
      - [phishingURL_1][domain]
    * - reportedDomain
      - query
      - string
      - Optional - This may be specified multiple times. The domain name associated with a reported url of a phishing
        threat.
      - [reportedURLs_1][domain]
    * - malwareDomain
      - query
      - string
      - Optional - This may be specified multiple times. The domain name associated with a reported url of a phishing
        threat.
      - [domainSet][domain]
    * - malwareWatchListDomain
      - query
      - string
      - Optional - This may be specified multiple times. The domain name of a watch list item associated with a malware
        campaign
      - [blockSet][][data_1][domain]
    * - domain
      - query
      - string
      - Optional - This may be specified multiple times. The domain name associated with a phishing or malware campaign.
      -
    * - kitFile
      - query
      - string
      - Optional - This may be specified multiple times. The filename associated with a phishing or malware campaign.
      - [kits][][kitName]
    * - malwareFile
      - query
      - string
      - Optional - This may be specified multiple times. The filename associated with a phishing or malware campaign.
      - [executableSet][][fileName]
    * - webComponentFile
      - query
      - string
      - Optional - This may be specified multiple times. The filename associated with a phishing or malware campaign.
      - [webComponents][][resourceURL][url]
    * - file
      - query
      - string
      - Optional - This may be specified multiple times. The filename associated with a phishing or malware campaign.
      -
    * - phishingTitle
      - query
      - string
      - Optional - This may be specified multiple times. The title text of a phishing web page.
      - [title]
    * - language
      - query
      - string
      - Optional - This may be specified multiple times. The detected language of a phishing web page.
      - [language][languageDefinition][family]
    * - malwareFamily
      - query
      - string
      - Optional -  The malware family associated with a malware campaign.
      - [malwareFamilySet][familyName]
    * - watchlistEmailAddress
      - query
      - string
      - Optional - This may be specified multiple times. The email address of a watch list item associated with a
        malware campaign.
      - [blockSet][][data_1][email]

**Python Sample Code**::

    import requests
    host = 'https://www.threathq.com/apiv1/threat/search'
    auth=('api_username', 'api_token')
    r = requests.post(host, auth=auth)
    print r.json()

    # Response
    {
      "success" : true,
      "data" : {
        "page" : {
        "currentPage" : 0,
        "currentElements" : 1,
        "totalPages" : 201673,
        "totalElements" : 201673
        },
        "threats" : [ {
          "id" : 6184170,
          "brands" : [ {
            "id" : 1253,
            "text" : "Lloyds Bank"
          } ],
          "feeds" : [ {
            "id" : 21,
            "permissions" : {
              "OWNER" : false,
              "WRITE" : false,
              "READ" : true
            },
            "displayName" : "APWG"
          } ],
          "screenshot" : {
            "url" : "https://www.threathq.com/apiv1/screenshot/6184170"
          },
          "confirmedDate" : 1411414666131,
          "ipDetail" : {
            "ip" : "62.109.4.150",
            "lookupOn" : 1411412768313,
            "latitude" : 55.7522,
            "longitude" : 37.6156,
            "timeZone" : "Europe/Moscow",
            "continentName" : "Europe",
            "continentCode" : "EU",
            "countryName" : "Russia",
            "countryIsoCode" : "RU",
            "subdivisionName" : "Moscow",
            "subdivisionIsoCode" : "MOW",
            "asn" : 29182,
            "asnOrganization" : "ISPsystem, cjsc",
            "isp" : "ISPsystem, cjsc",
            "organization" : "ISPsystem, cjsc",
            "userType" : "residential"
          },
          "isConfirmedPhishingWebsite" : "YES",
          "processingState" : "ANALYZED",
          "phishingURL" : "http://test.smart-z.ru/modules/mod_mainmenu/tmpl/lloydstsb/Memorable.htm",
          "reportedURLs" : [ "http://test.smart-z.ru/modules/mod_mainmenu/tmpl/lloydstsb/Memorable.htm" ],
          "actionURLs" : [ "http://test.smart-z.ru/modules/mod_mainmenu/tmpl/lloydstsb/memory.php" ]
        } ]
      }
    }

**POST /threat/updates**

**Description**: The ThreatHQ® API enables users to retrieve only the newest Threat IDs since last check. This should be
the primary endpoint used for an integration with a goal of maintaining near real-time synchronization with PhishMe. The
first query should include the timestamp field, the response will include a position value which can be used to retrieve
the next page of results. This search interface will return a UUID to be used in subsequent queries.

**Response Description**: A JSON object representing a list of newest PhishMe Intelligence and PhishMe Brand
Intelligence Threat IDs. Each page of results contains up to 1000 records.

**Parameters:**

========= ===== ========= =======
Parameter Type  Data Type Details
========= ===== ========= =======
timestamp query integer   Optional - The epoch in seconds from which data will be returned.
position  query string    Optional - A unique string used to identify the the last record read by this client.
========= ===== ========= =======

**Python Sample Code**::

    import requests
    host = 'https://www.threathq.com/apiv1/threat/updates'
    auth=('api_username', 'api_token')
    r = requests.post(host, auth=auth)
    print r.json()

    # Response
    {
        nextPosition: '2c916de4-fc3e-21e4-9c84-74e436e7eb39',
        changelog: [
          {threatId: 1, threatType: 'phish', timestamp: 1431720588000, deleted: false},
          {threatId: 12, threatType: 'phish', timestamp: 1431720588001, deleted: true},
          {threatId: 56, threatType: 'malware', timestamp: 1431720588001, deleted: true},
          {threatId: 560, threatType: 'malware', timestamp: 1431720588003, deleted: false},
        ]
    }