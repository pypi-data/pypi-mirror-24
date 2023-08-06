.. _schema_brand_intelligence_json:

==========================================
PhishMe Brand Intelligence Structure: JSON
==========================================

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
            }
        },
        "type": "object",
        "required": [
            "brands",
            "confirmedDate",
            "feeds",
            "firstDate",
            "id",
            "lastDate",
            "processingState",
            "reportedURLs_1",
            "threatType"
        ],
        "properties": {
            "actionURLs": {
                "title": "DEPRECATED",
                "description": "Replaced by 'actionURLs_1'",
                "type": "array",
                "items": {
                    "title": "This is the next URL to be called when the victim submits their information to the phishing site. It might lead directly to a second page of the phishing site, it might be an intermediate PHP script that submits credentials to the criminal, it might lead to an exit URL, or it may be some combination of these things. Note: each page of a phishing attack will have an action URL, PhishMe is only capturing the Action URL for the first page.",
                    "type": "string"
                }
            },
            "actionURLs_1": {
                "title": "This is the next URL to be called when the victim submits their information to the phishing site. It might lead directly to a second page of the phishing site, it might be an intermediate PHP script that submits credentials to the criminal, it might lead to an exit URL, or it may be some combination of these things. Note: each page of a phishing attack will have an action URL, PhishMe is only capturing the Action URL for the first page.",
                "type": "array",
                "items": {
                    "$ref": "#/definitions/url"
                }
            },
            "brands": {
                "title": "The brand being imitated by this phishing attack. Typically an ESM (email service provider) or FI (financial institution).",
                "type": "array",
                "items": {
                    "title": "Imitated brand.",
                    "type": "object",
                    "required": [
                        "id",
                        "text"
                    ],
                    "properties": {
                        "id": {
                            "title": "A numerical identifier for PhishMe.",
                            "type": "integer"
                        },
                        "text": {
                            "title": "Name of imitated brand.",
                            "type": "string"
                        }
                    }
                }
            },
            "confirmedDate": {
                "title": "Timestamp when this phish was confirmed.",
                "type": "integer"
            },
            "feeds": {
                "title": "Feeds",
                "description": "A list of feeds where PhishMe discovered this threat. If contractually allowed, the feed will be named. If not, the name shown will be PhishMe. If the threat was provided privately by your organization, you will see the name of your organization.",
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
            "firstDate": {
                "title": "First date this phish was received by PhishMe.",
                "type": "integer"
            },
            "id": {
                "title": "Threat ID",
                "type": "integer"
            },
            "ipDetail": {
                "title": "Details about the IP address where this phish is hosted.",
                "type": "object",
                "properties": {
                    "asn": {
                        "title": "The number which refers to a network operator having control over this IP address.",
                        "type": "integer"
                    },
                    "asnOrganization": {
                        "title": "The long form name of the organization responsible for this ASN.",
                        "type": "string"
                    },
                    "continentCode": {
                        "title": "Two-letter continent code.",
                        "type": "string",
                        "minLength": 2,
                        "maxLength": 2
                    },
                    "continentName": {
                        "title": "Friendly name of continent.",
                        "type": "string"
                    },
                    "countryIsoCode": {
                        "title": "Two-letter code for country where this IP is located.",
                        "type": "string",
                        "minLength": 2,
                        "maxLength": 2
                    },
                    "countryName": {
                        "title": "The friendly name of the country where this IP is located.",
                        "type": "string"
                    },
                    "ip": {
                        "title": "IPv4 address.",
                        "type": "string",
                        "format": "ipv4"
                    },
                    "isp": {
                        "title": "The ISP having control over this IPv4 address.",
                        "type": "string"
                    },
                    "latitude": {
                        "title": "latitude",
                        "type": "number",
                        "not": {
                            "title": "This is a float, but JSON schemas don't support floats directly.",
                            "type": "integer"
                        }
                    },
                    "longitude": {
                        "title": "longitude",
                        "type": "number",
                        "not": {
                            "title": "This is a float, but JSON schemas don't support floats directly.",
                            "type": "integer"
                        }
                    },
                    "lookupOn": {
                        "title": "Timestamp when this IP address enrichment was performed.",
                        "type": "integer"
                    },
                    "organization": {
                        "title": "The organization having control over this IPv4 address.",
                        "type": "string"
                    },
                    "timeZone": {
                        "title": "Hosting provider for this IP address.",
                        "type": "string"
                    },
                    "userType": {
                        "title": "Primary usage of this IPv4 address, according to hosting provider.",
                        "type": "string"
                    }
                }
            },
            "isConfirmedPhishingWebsite": {
                "title": "Is it a phish?",
                "type": "string",
                "enum": [
                    "YES",
                    "NO"
                ]
            },
            "language": {
                "title": "Primary language of the phishing page.",
                "type": "object",
                "properties": {
                    "languageDefinition": {
                        "title": "Language.",
                        "type": "object",
                        "properties": {
                            "family": {
                                "title": "Family of detected language.",
                                "type": "string"
                            },
                            "isoCode": {
                                "title": "Two-letter language code or 'zh-cn' or 'zh-tw'.",
                                "type": "string",
                                "minLength": 2,
                                "maxLength": 5
                            },
                            "name": {
                                "title": "Friendly name of langage.",
                                "type": "string"
                            },
                            "nativeName": {
                                "title": "Native name of language.",
                                "type": "string"
                            }
                        }
                    },
                    "probability": {
                        "title": "Probability of the named language being correct, as assigned by the language detection algorithm.",
                        "type": "number",
                        "not": {
                            "title": "Numerical percentage.",
                            "type": "integer"
                        }
                    }
                }
            },
            "lastDate": {
                "title": "Timestamp for most recent time PhishMe detected this phishing attack.",
                "type": "integer"
            },
            "phishingURL": {
                "title": "DEPRECATED",
                "description": "Replaced by 'phishingURL_1'",
                "type": "string"
            },
            "phishingURL_1": {
                "title": "The URL of the phishing attack.",
                "type": "object",
                "$ref": "#/definitions/url"
            },
            "processingState": {
                "title": "Status of processing this phish.",
                "type": "string",
                "enum": [
                    "ANALYZED"
                ]
            },
            "reportedURLs": {
                "title": "DEPRECATED",
                "description": "Replaced by 'reportedURLs_1'",
                "type": "array"
            },
            "reportedURLs_1": {
                "title": "Original URL reported to PhishMe.",
                "type": "array",
                "items": {
                    "$ref": "#/definitions/url"
                }
            },
            "screenshot": {
                "title": "Direct URL to screenshot of phish.",
                "type": "object",
                "properties": {
                    "url": {
                        "title": "DEPRECATED",
                        "description": "Replaced by 'url_1'",
                        "type": "string"
                    },
                    "url_1": {
                        "title": "Direct URL to screenshot of phish.",
                        "type": "object",
                        "$ref": "#/definitions/url"
                    }
                }
            },
            "threatType": {
                "title": "Threat Type",
                "description": "This will only have one value for phish.",
                "type": "string",
                "enum": [
                    "PHISH"
                ]
            },
            "title": {
                "title": "The text from the raw HTML used to display the phishing URL, typically found within the <title> </title> tags. This is the text displayed by a browser at the top of the browser or tab.",
                "type": "string"
            }
        }
    }

