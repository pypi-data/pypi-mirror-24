.. _schema_intelligence_json:

====================================
PhishMe Intelligence Structure: JSON
====================================

**JSON Schema**::

    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "definitions": {
            "url": {
                "title": "URL",
                "description": "Global definition for URL and components.",
                "type": "object",
                "required": [
                    "host",
                    "path",
                    "protocol",
                    "url"
                ],
                "properties": {
                    "domain": {
                        "title": "Domain Name",
                        "type": "string"
                    },
                    "host": {
                        "title": "Host Name",
                        "type": "string"
                    },
                    "path": {
                        "title": "The portion of the URL after the TLD and first '/'",
                        "type": "string"
                    },
                    "protocol": {
                        "title": "The prefix of the URL",
                        "type": "string"
                    },
                    "query": {
                        "title": "Any arguments",
                        "type": "string"
                    },
                    "url": {
                        "title": "Full URL",
                        "type": "string"
                    }
                }
            },
            "malwareFamily": {
                "title": "Malware Family",
                "description": "Names and describes malware families.",
                "type" : "object",
                "required": [
                    "description",
                    "familyName"
                ],
                "properties": {
                    "description": {
                        "title": "Brief description of the malware family, what it does, or how it works",
                        "type": "string"
                    },
                    "familyName": {
                        "title": "Family name of malware",
                        "type": "string"
                    }
                }
            },
            "infrastructureTypeSubclass": {
                "title": "Description of Infrastructure type",
                "type": "object",
                "required": [
                    "description"
                ],
                "properties": {
                    "description": {
                        "title": "Brief description of infrastructure type being used",
                        "type": "string"
                    }
                }
            },
            "ipDetail": {
                "title": "Specific information related to the domain name",
                "type": "object",
                "required": [
                    "asn",
                    "continentCode",
                    "ip",
                    "latitude",
                    "longitude",
                    "lookupOn"
                ],
                "properties": {
                    "asn": {
                        "title": "Autonomous system number (ASN) associated with domain name",
                        "type": "integer"
                    },
                    "asnOrganization": {
                        "title": "Administrative entity of ASN associated with domain name",
                        "type": "string"
                    },
                    "continentCode": {
                        "title": "Continent code associated with domain name",
                        "type": "string"
                    },
                    "continentName": {
                        "title": "Continent name associated with domain name",
                        "type": "string"
                    },
                    "countryIsoCode": {
                        "title": "Country ISO code associated with domain name",
                        "type": "string"
                    },
                    "countryName": {
                        "title": "Country name associated with domain name",
                        "type": "string"
                    },
                    "ip": {
                        "title": "IP address associated with domain name",
                        "type": "string"
                    },
                    "isp": {
                        "title": "Internet Service Provider (ISP) associated with domain name",
                        "type": "string"
                    },
                    "latitude": {
                        "title": "Approximate latitude location of domain name hosting",
                        "type": "number"
                    },
                    "longitude": {
                        "title": "Approximate longitude location of domain name hosting",
                        "type": "number"
                    },
                    "lookupOn": {
                        "title": "timestamp when lookup of this information was performed",
                        "type": "integer"
                    },
                    "organization": {
                        "title": "Organization associated with domain name",
                        "type": "string"
                    },
                    "postalCode": {
                        "title": "Postal code associated with domain name",
                        "type": "string"
                    },
                    "subdivisionIsoCode": {
                        "title": "subdivision ISO code associated with domain name",
                        "type": "string"
                    },
                    "subdivisionName": {
                        "title": "subdivision name associated with domain name",
                        "type": "string"
                    },
                    "timeZone": {
                        "title": "timezone associated with domain name",
                        "type": "string"
                    }
                }
            },
            "vendorDetections": {
                "title": "List of antivirus vendors and whether they detected the executable in VirusTotal",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "detected",
                        "threatVendorName"
                    ],
                    "properties": {
                        "detected": {
                            "title": "Was executable detected?",
                            "type": "boolean"
                        },
                        "threatVendorName": {
                            "title": "Name of antivirus vendor",
                            "type": "string"
                        }
                    }
                }
            }
        },
        "type": "object",
        "required": [
            "blockSet",
            "campaignBrandSet",
            "domainSet",
            "executableSet",
            "extractedStringSet",
            "feeds",
            "firstPublished",
            "hasReport",
            "id",
            "label",
            "executiveSummary",
            "lastPublished",
            "malwareFamilySet",
            "reportURL",
            "senderEmailSet",
            "senderIpSet",
            "senderNameSet",
            "spamUrlSet",
            "subjectSet",
            "threatType"
        ],
        "properties": {
            "blockSet": {
                "title": "BlockSet or WatchList",
                "description": "Each web location described in the set of watchlist indicators associated with a Threat ID has a series of description fields meant to provide detail about the nature of that indicator. Each of these corresponds to a finite set of possible entries at any given time. The categories used to describe this information are as follows.",
                "type": "array",
                "items": {
                  "type": "object",
                  "oneOf": [
                    {
                      "required": [
                        "blockType",
                        "data_1",
                        "impact"
                      ],
                      "properties": {
                        "blockType": {
                          "title": "Data type of the watchlist item",
                          "type": "string",
                          "enum": [
                            "Domain Name",
                            "IPv4 Address"
                          ]
                        },
                        "data": {
                          "title": "DEPRECATED",
                          "description": "Replaced by 'data_1'",
                          "type": "string"
                        },
                        "data_1": {
                          "title": "Either a domain name or an IP address",
                          "type": "string"
                        },
                        "impact": {
                          "title": "Values borrowed from stixVocabs:ImpactRatingVocab-1.0",
                          "type": "string",
                          "enum": [
                            "Major",
                            "Moderate",
                            "Minor",
                            "None"
                          ]
                        },
                        "infrastructureTypeSubclass": {
                          "$ref": "#/definitions/infrastructureTypeSubclass"
                        },
                        "ipDetail": {
                          "$ref": "#/definitions/ipDetail"
                        },
                        "malwareFamily": {
                          "$ref": "#/definitions/malwareFamily"
                        },
                        "role": {
                          "title": "Infrastructure Type",
                          "type": "string"
                        },
                        "roleDescription": {
                          "title": "Description of infrastructure type",
                          "type": "string"
                        }
                      },
                      "additionalProperties": false
                    },
                    {
                      "required": [
                        "blockType",
                        "data_1",
                        "impact"
                      ],
                      "properties": {
                        "blockType": {
                          "title": "Data type of the watchlist item",
                          "type": "string",
                          "enum": [
                            "URL"
                          ]
                        },
                        "data": {
                          "title": "DEPRECATED",
                          "type": "string"
                        },
                        "data_1": {
                          "$ref": "#/definitions/url"
                        },
                        "impact": {
                          "title": "Values borrowed from stixVocabs:ImpactRatingVocab-1.0",
                          "type": "string",
                          "enum": [
                            "Major",
                            "Moderate",
                            "Minor",
                            "None"
                          ]
                        },
                        "infrastructureTypeSubclass": {
                          "$ref": "#/definitions/infrastructureTypeSubclass"
                        },
                        "ipDetail": {
                          "$ref": "#/definitions/ipDetail"
                        },
                        "malwareFamily": {
                          "$ref": "#/definitions/malwareFamily"
                        },
                        "role": {
                          "title": "Infrastructure Type",
                          "type": "string"
                        },
                        "roleDescription": {
                          "title": "Description of infrastructure type",
                          "type": "string"
                        }
                      },
                      "additionalProperties": false
                    },
                    {
                      "required": [
                        "blockType",
                        "data_1",
                        "impact"
                      ],
                      "properties": {
                        "blockType": {
                          "title": "Data type of the watchlist item",
                          "type": "string",
                          "enum": [
                            "Email"
                          ]
                        },
                        "data": {
                          "title": "DEPRECATED",
                          "type": "string"
                        },
                        "data_1": {
                          "title": "Email address",
                          "type": "string"
                        },
                        "impact": {
                          "title": "Values borrowed from stixVocabs:ImpactRatingVocab-1.0",
                          "type": "string",
                          "enum": [
                            "Major",
                            "Moderate",
                            "Minor",
                            "None"
                          ]
                        },
                        "infrastructureTypeSubclass": {
                          "$ref": "#/definitions/infrastructureTypeSubclass"
                        },
                        "malwareFamily": {
                          "$ref": "#/definitions/malwareFamily"
                        },
                        "role": {
                          "title": "Infrastructure Type",
                          "type": "string"
                        },
                        "roleDescription": {
                          "title": "Description of infrastructure type",
                          "type": "string"
                        }
                      },
                      "additionalProperties": false
                    }]
                }
            },
            "campaignBrandSet": {
                "title": "Campaign brand set",
                "description": "All brands spoofed by this campaign.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "brand",
                        "totalCount"
                    ],
                    "properties": {
                        "brand": {
                            "title": "Brand being spoofed",
                            "type": "object",
                            "required": [
                                "id",
                                "text"
                            ],
                            "properties": {
                                "id": {
                                    "title": "Numeric identifier used by Malcovery to track this brand",
                                    "type": "integer"
                                },
                                "text": {
                                    "title": "String identifier used by Malcovery to track this brand",
                                    "type": "string"
                                }
                            }
                        },
                        "totalCount": {
                            "title": "Number of individual messages associated with this brand",
                            "type": "integer"
                        }
                    }
                }
            },
            "domainSet": {
                "title": "Domain set",
                "description": "This is the domain name of the sending address or the TO: field.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "domain",
                        "totalCount"
                    ],
                    "properties": {
                        "domain": {
                            "title": "Sender domain name",
                            "type": "string"
                        },
                        "totalCount": {
                            "title": "Count of the instances of each item named",
                            "type": "integer"
                        }
                    }
                }
            },
            "executableSet": {
                "title": "Executable set",
                "description": "These are all the files placed on an endpoint during the course of a malware infection.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "dateEntered",
                        "fileName",
                        "md5Hex"
                    ],
                    "properties": {
                        "dateEntered": {
                            "title": "Date when this file was analyzed by Malcovery",
                            "type": "integer"
                        },
                        "fileName": {
                            "title": "The file name of any file discovered during a malware infection.",
                            "type": "string"
                        },
                        "malwareFamily": {
                            "$ref": "#/definitions/malwareFamily"
                        },
                        "md5Hex": {
                            "title": "The md5 hash of the file",
                            "type": "string",
                            "minLength": 32,
                            "maxLength": 32
                        },
                        "sha1Hex": {
                            "title": "The SHA-1 hash of the file",
                            "type": "string",
                            "minLength": 40,
                            "maxLength": 40
                        },
                        "sha224Hex": {
                            "title": "The SHA-224 hash of the file",
                            "type": "string",
                            "minLength": 56,
                            "maxLength": 56
                        },
                        "sha256Hex": {
                            "title": "The SHA-256 hash of the file",
                            "type": "string",
                            "minLength": 64,
                            "maxLength": 64
                        },
                        "sha384Hex": {
                            "title": "The SHA-384 hash of the file",
                            "type": "string",
                            "minLength": 96,
                            "maxLength": 96
                        },
                        "sha512Hex": {
                            "title": "The SHA-512 hash of the file",
                            "type": "string",
                            "minLength": 128,
                            "maxLength": 128
                        },
                        "ssdeep": {
                            "title": "The ssdeep hash of the file",
                            "type": "string"
                        },
                        "type": {
                            "title": "Description of the purpose this file serves within the malware infection",
                            "type": "string"
                        },
                        "vendorDetections": {
                            "$ref": "#/definitions/vendorDetections"
                        }
                    }
                }
            },
            "extractedStringSet": {
                "title": "Extracted strings",
                "description": "These are configuration items for the malware to know what browser URLs to capture or inject with additional fields.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "data"
                    ],
                    "properties": {
                        "data": {
                            "title": "Configuration items",
                            "type": "string"
                        }
                    }
                }
            },
            "feeds": {
                "title": "Feeds",
                "description": "A list of feeds where Malcovery discovered this threat. If contractually allowed, the feed will be named. If not, the name shown will be Malcovery. If the threat was provided privately by your organization, you will see the name of your organization.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "displayName",
                        "id",
                        "permissions"
                    ],
                    "properties": {
                        "displayName": {
                            "title": "Human readable name for this feed",
                            "type": "string"
                        },
                        "id": {
                            "title": "Integer identifier for this feed",
                            "type": "integer"
                        },
                        "permissions": {
                            "title": "List of permissions that current customer has to this particular feed",
                            "type": "object",
                            "required": [
                                "OWNER",
                                "READ",
                                "WRITE"
                            ],
                            "properties": {
                                "OWNER": {
                                    "title": "True if you are the original provider of the source data for this feed",
                                    "type": "boolean",
                                    "enum": [
                                        false,
                                        true
                                    ]
                                },
                                "READ": {
                                    "title": "True if you are allowed to view data for this feed",
                                    "type": "boolean",
                                    "enum": [
                                        false,
                                        true
                                    ]
                                },
                                "WRITE": {
                                    "title": "True if you are allowed to submit data to this feed",
                                    "type": "boolean",
                                    "enum": [
                                        false,
                                        true
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "firstPublished": {
                "title": "Timestamp of when this campaign was initially published",
                "type": "integer"
            },
            "hasReport": {
                "title": "Flag to show whether this campaign has a written report associated with it.",
                "type": "boolean",
                "enum": [
                    false,
                    true
                ]
            },
            "id": {
                "title" : "Threat ID",
                "Description": "This is a unique identifier for this campaign.",
                "type": "integer"
            },
            "label": {
                "title": "Human readable name for this campaign",
                "type": "string"
            },
            "executiveSummary": {
                "title": "Analyst written summary of the campaign",
                "type": "string"
            },
            "lastPublished": {
                "title": "Timestamp of when this campaign was most recently updated",
                "type": "integer"
            },
            "malwareFamilySet": {
                "type": "array",
                "items": {
                    "$ref": "#/definitions/malwareFamily"
                }
            },
            "reportURL": {
                "title": "T3 Report URL",
                "description": "Direct URL to human readable report for this campaign.",
                "type": "string"
            },
            "senderEmailSet":{
                "title": "Sender Email Addresses",
                "description": "These are the email addresses being used to deliver the mail. Due to the nature of mail headers, some of these email addresses may be spoofed.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "senderEmail",
                        "totalCount"
                    ],
                    "properties": {
                        "senderEmail": {
                            "title": "The possibly spoofed email address used in the delivery of the email.",
                            "type": "string"
                        },
                        "totalCount": {
                            "title": "Count of the instances of each item named.",
                            "type": "integer"
                        }
                    }
                }
            },
            "senderIpSet": {
                "title": "Sender IP",
                "description": "These are the IP addresses being used to deliver the mail. Due to the nature of mail headers, some of these IPs may be spoofed.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "ip",
                        "totalCount"
                    ],
                    "properties": {
                        "ip": {
                            "title": "One of possibly many IPs used in the delivery of the email.",
                            "type": "string"
                        },
                        "totalCount": {
                            "title": "Count of the instances of each item named.",
                            "type": "integer"
                        }
                    }
                }
            },
             "senderNameSet": {
                "title": "Sender Name",
                "description": "This is the friendly name of the sender of the email.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "totalCount"
                    ],
                    "properties": {
                        "totalCount": {
                            "title": "Count of the instances of each item named.",
                            "type": "integer"
                        }
                    }
                }
            },
            "spamUrlSet": {
                "title": "Spam URL",
                "description": "Set of URLs identified in spam emails associated with a campaign.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "totalCount",
                        "url_1"
                    ],
                    "properties": {
                        "totalCount": {
                            "title": "Number of times a URL was seen in conjunction with a set of spam emails.",
                            "type": "integer"
                        },
                        "url": {
                            "title": "DEPRECATED",
                            "type": "string"
                        },
                        "url_1": {
                            "$ref": "#/definitions/url"
                        }
                    }
                }
            },
            "subjectSet": {
                "title": "Email Subjects",
                "description": "This is the subject line of all malicious emails determined to be part of this campaign.",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "subject",
                        "totalCount"
                    ],
                    "properties": {
                        "subject": {
                            "title": "Email subject line.",
                            "type": "string"
                        },
                        "totalCount": {
                            "title": "Count of the instances of each item named.",
                            "type": "integer"
                        }
                    }
                }
            },
            "threatType": {
                "title": "Threat Type",
                "description": "This will only have one value for malware.",
                "type": "string",
                "enum": [
                    "MALWARE"
                ]
            }
        }
    }