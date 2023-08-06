.. _schema_intelligence_stix:

====================================
PhishMe Intelligence Structure: STIX
====================================

PhishMe currently produces a STIX/CyBox package using STIX 1.1.1 and CyBox 2.1.0 which passes all best practices tests
performed by MITRE's `stix-validator <https://github.com/STIXProject/stix-validator>`_.

The layout is modeled after `Approach #2: Relationship via reference <http://stixproject.github.io/documentation/suggested-practices/#referencing-vs-embedding>`_.
Each of the major STIX constructs are placed at the top level of the STIX package and relationships are formed by
reference.

=========================== =======
Line Number                 PhishMe
=========================== =======
267                         Threat ID
268                         Brand
88, 110, 132, 154, 173, 192	First Publish Date
272                         T3 Report (URL)
271                         Threat HQ (URL)
213                         Malware Family Name
214                         Malware Family Description
40, 55, 70                  File Name
41, 56, 71                  File Extension
45, 60, 75                  File MD5
37, 52, 67                  File Type
17, 24, 31                  Watch List Type
25                          Watch List Domain
32                          Watch List IPv4
18                          Watch List URL
94, 116, 138, 160, 179, 198 Impact Rating
233, 253                    Infrastructure Type
234, 254                    Infrastructure Type Description
88, 110, 132, 154, 173, 192 Watch List Entry Last Updated
=========================== =======

**STIX Schema**::

    <stix:STIX_Package id="PhishMe:Package-01bb9ef0-1c8d-4362-aad9-6b601ae7c8cf" timestamp="2015-06-26T13:53:38.192-05:00" version="1.1.1">
        <stix:STIX_Header>
            <stix:Title>PhishMe Malware ThreatID 3664</stix:Title>
            <stix:Package_Intent xsi:type="stixVocabs:PackageIntentVocab-1.0">Malware Characterization</stix:Package_Intent>
            <stix:Information_Source>
                <stixCommon:Identity>
                    <stixCommon:Name>PhishMe, Inc - Machine Readable Threat Intelligence Feed</stixCommon:Name>
                </stixCommon:Identity>
                <stixCommon:Time>
                    <cyboxCommon:Produced_Time>2015-06-26T13:53:38.218-05:00</cyboxCommon:Produced_Time>
                </stixCommon:Time>
            </stix:Information_Source>
        </stix:STIX_Header>
        <stix:Observables cybox_major_version="2" cybox_minor_version="1" cybox_update_version="0">
            <cybox:Observable id="PhishMe:Observable-6f1937d2-f1e9-4f7e-9fb1-a1462994923d">
                <cybox:Object id="PhishMe:URI-6f1937d2-f1e9-4f7e-9fb1-a1462994923d">
                    <cybox:Properties type="URL" xsi:type="URIObj:URIObjectType">
                        <URIObj:Value condition="Equals">http://subdomain.domain.com/pcss/gate.php</URIObj:Value>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-0609268f-2d98-4a87-a647-f22a668e8abc">
                <cybox:Object id="PhishMe:DomainName-0609268f-2d98-4a87-a647-f22a668e8abc">
                    <cybox:Properties xsi:type="DomainNameObj:DomainNameObjectType">
                        <DomainNameObj:Value condition="Equals">subdomain.domain.com</DomainNameObj:Value>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-cf54844f-b452-4743-9c1b-4673e8961a90">
                <cybox:Object id="PhishMe:Address-cf54844f-b452-4743-9c1b-4673e8961a90">
                    <cybox:Properties category="ipv4-addr" xsi:type="AddressObj:AddressObjectType">
                        <AddressObj:Address_Value condition="Equals">255.255.255.256</AddressObj:Address_Value>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-73296479-7ba5-4ae1-a4b0-3cfea2d0fdbc">
                <cybox:Description>Drop</cybox:Description>
                <cybox:Object id="PhishMe:File-73296479-7ba5-4ae1-a4b0-3cfea2d0fdbc">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name condition="Equals">new order.exe</FileObj:File_Name>
                        <FileObj:File_Extension condition="Equals">exe</FileObj:File_Extension>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type condition="Equals" xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value condition="Equals">a401feb2c159bb273aa1e5a78b3333e0</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-41f36c4f-6460-4be5-a9f9-eb8b0d1ca1fd">
                <cybox:Description>Drop</cybox:Description>
                <cybox:Object id="PhishMe:File-41f36c4f-6460-4be5-a9f9-eb8b0d1ca1fd">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name condition="Equals">new order.zip</FileObj:File_Name>
                        <FileObj:File_Extension condition="Equals">zip</FileObj:File_Extension>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type condition="Equals" xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value condition="Equals">8829913c2ddcbd8df21e37f8aee09b1b</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-7e2d75fc-0540-4f70-9d6e-b87dce84fd2d">
                <cybox:Description>Drop</cybox:Description>
                <cybox:Object id="PhishMe:File-7e2d75fc-0540-4f70-9d6e-b87dce84fd2d">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name condition="Equals">P order.exe</FileObj:File_Name>
                        <FileObj:File_Extension condition="Equals">exe</FileObj:File_Extension>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type condition="Equals" xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value condition="Equals">8b07e7126cfbb53401add74c3aa0ef5e</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
        </stix:Observables>
        <stix:Indicators>
            <stix:Indicator id="PhishMe:indicator-6f1937d2-f1e9-4f7e-9fb1-a1462994923d" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>Watchlist URL</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">URL Watchlist</indicator:Type>
                <indicator:Description>Watchlist URL</indicator:Description>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-26T09:33:35.020-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-12106bf8-d184-470d-a4d9-5f5d431a8529" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Likely_Impact>
                    <stixCommon:Value xsi:type="stixVocabs:ImpactRatingVocab-1.0">Major</stixCommon:Value>
                </indicator:Likely_Impact>
                <indicator:Confidence timestamp="2015-06-26T09:33:35.020-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-01bb9ef0-1c8d-4362-aad9-6b601ae7c8cf" timestamp="2015-06-26T09:33:35.020-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-0609268f-2d98-4a87-a647-f22a668e8abc" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>Watchlist Domain</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">Domain Watchlist</indicator:Type>
                <indicator:Description>Watchlist Domain</indicator:Description>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-26T09:33:35.020-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-12106bf8-d184-470d-a4d9-5f5d431a8529" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Likely_Impact>
                    <stixCommon:Value xsi:type="stixVocabs:ImpactRatingVocab-1.0">Minor</stixCommon:Value>
                </indicator:Likely_Impact>
                <indicator:Confidence timestamp="2015-06-26T09:33:35.020-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-01bb9ef0-1c8d-4362-aad9-6b601ae7c8cf" timestamp="2015-06-26T09:33:35.020-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-cf54844f-b452-4743-9c1b-4673e8961a90" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>Watchlist IPv4</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">IP Watchlist</indicator:Type>
                <indicator:Description>Watchlist IPv4</indicator:Description>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-26T09:33:35.020-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-12106bf8-d184-470d-a4d9-5f5d431a8529" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Likely_Impact>
                    <stixCommon:Value xsi:type="stixVocabs:ImpactRatingVocab-1.0">Moderate</stixCommon:Value>
                </indicator:Likely_Impact>
                <indicator:Confidence timestamp="2015-06-26T09:33:35.020-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-01bb9ef0-1c8d-4362-aad9-6b601ae7c8cf" timestamp="2015-06-26T09:33:35.020-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-73296479-7ba5-4ae1-a4b0-3cfea2d0fdbc" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>File associated with malware infection</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">File Hash Watchlist</indicator:Type>
                <indicator:Description>File associated with malware infection</indicator:Description>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-26T09:33:35.020-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-12106bf8-d184-470d-a4d9-5f5d431a8529" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Confidence timestamp="2015-06-26T09:33:35.020-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-01bb9ef0-1c8d-4362-aad9-6b601ae7c8cf" timestamp="2015-06-26T09:33:35.020-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-41f36c4f-6460-4be5-a9f9-eb8b0d1ca1fd" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>File associated with malware infection</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">File Hash Watchlist</indicator:Type>
                <indicator:Description>File associated with malware infection</indicator:Description>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-26T09:33:35.020-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-12106bf8-d184-470d-a4d9-5f5d431a8529" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Confidence timestamp="2015-06-26T09:33:35.020-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-01bb9ef0-1c8d-4362-aad9-6b601ae7c8cf" timestamp="2015-06-26T09:33:35.020-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-7e2d75fc-0540-4f70-9d6e-b87dce84fd2d" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>File associated with malware infection</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">File Hash Watchlist</indicator:Type>
                <indicator:Description>File associated with malware infection</indicator:Description>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-26T09:33:35.020-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-12106bf8-d184-470d-a4d9-5f5d431a8529" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Confidence timestamp="2015-06-26T09:33:35.020-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-01bb9ef0-1c8d-4362-aad9-6b601ae7c8cf" timestamp="2015-06-26T09:33:35.020-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
        </stix:Indicators>
        <stix:TTPs>
            <stix:TTP id="PhishMe:ttp-12106bf8-d184-470d-a4d9-5f5d431a8529" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType">
                <ttp:Title>Pony</ttp:Title>
                <ttp:Behavior>
                    <ttp:Malware>
                        <ttp:Malware_Instance>
                            <ttp:Name>Pony</ttp:Name>
                            <ttp:Description>Information stealer and malware downloader</ttp:Description>
                        </ttp:Malware_Instance>
                    </ttp:Malware>
                </ttp:Behavior>
                <ttp:Related_TTPs>
                    <ttp:Related_TTP>
                        <stixCommon:Relationship>Uses infrastructure</stixCommon:Relationship>
                        <stixCommon:TTP idref="PhishMe:ttp-ff57eac5-fa54-4fc1-b68e-76b6b5a8016f" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                    </ttp:Related_TTP>
                    <ttp:Related_TTP>
                        <stixCommon:Relationship>Uses infrastructure</stixCommon:Relationship>
                        <stixCommon:TTP idref="PhishMe:ttp-b98102f8-8a6d-46dc-be78-4ede8fbba7c3" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                    </ttp:Related_TTP>
                </ttp:Related_TTPs>
            </stix:TTP>
            <stix:TTP id="PhishMe:ttp-b98102f8-8a6d-46dc-be78-4ede8fbba7c3" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType">
                <ttp:Title>Infrastructure Type</ttp:Title>
                <ttp:Resources>
                    <ttp:Infrastructure>
                        <ttp:Type>C2</ttp:Type>
                        <ttp:Description>Command and control location used by malware</ttp:Description>
                        <ttp:Observable_Characterization cybox_major_version="2" cybox_minor_version="1" cybox_update_version="0">
                            <cybox:Observable idref="PhishMe:Observable-6f1937d2-f1e9-4f7e-9fb1-a1462994923d"/>
                            <cybox:Observable idref="PhishMe:Observable-0609268f-2d98-4a87-a647-f22a668e8abc"/>
                            <cybox:Observable idref="PhishMe:Observable-cf54844f-b452-4743-9c1b-4673e8961a90"/>
                        </ttp:Observable_Characterization>
                    </ttp:Infrastructure>
                </ttp:Resources>
                <ttp:Related_TTPs>
                    <ttp:Related_TTP>
                        <stixCommon:Relationship>Infrastructure for</stixCommon:Relationship>
                        <stixCommon:TTP idref="PhishMe:ttp-12106bf8-d184-470d-a4d9-5f5d431a8529" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                    </ttp:Related_TTP>
                </ttp:Related_TTPs>
            </stix:TTP>
            <stix:TTP id="PhishMe:ttp-ff57eac5-fa54-4fc1-b68e-76b6b5a8016f" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType">
                <ttp:Title>Infrastructure Type</ttp:Title>
                <ttp:Resources>
                    <ttp:Infrastructure>
                        <ttp:Type>Payload</ttp:Type>
                        <ttp:Description>Location from which a payload is obtained</ttp:Description>
                    </ttp:Infrastructure>
                </ttp:Resources>
                <ttp:Related_TTPs>
                    <ttp:Related_TTP>
                        <stixCommon:Relationship>Infrastructure for</stixCommon:Relationship>
                        <stixCommon:TTP idref="PhishMe:ttp-12106bf8-d184-470d-a4d9-5f5d431a8529" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="ttp:TTPType"/>
                    </ttp:Related_TTP>
                </ttp:Related_TTPs>
            </stix:TTP>
        </stix:TTPs>
        <stix:Campaigns>
            <stix:Campaign id="PhishMe:Campaign-01bb9ef0-1c8d-4362-aad9-6b601ae7c8cf" timestamp="2015-06-26T09:33:35.020-05:00" xsi:type="campaign:CampaignType">
                <campaign:Title>3664</campaign:Title>
                <campaign:Description>Generic Malware Threat</campaign:Description>
                <campaign:Information_Source>
                    <stixCommon:References>
                        <stixCommon:Reference>https://www.threathq.com/p42/search/default?m=3664</stixCommon:Reference>
                        <stixCommon:Reference>https://www.threathq.com/apiv1/t3/3664/html</stixCommon:Reference>
                    </stixCommon:References>
                </campaign:Information_Source>
            </stix:Campaign>
        </stix:Campaigns>
    </stix:STIX_Package>