.. _schema_brand_intelligence_stix:

==========================================
PhishMe Brand Intelligence Structure: STIX
==========================================

PhishMe currently produces a STIX/CyBox package using STIX 1.1.1 and CyBox 2.1.0 which passes all best practices tests
performed by MITRE's `stix-validator <https://github.com/STIXProject/stix-validator>`_.

The layout is modeled after `Approach #2: Relationship via reference <http://stixproject.github.io/documentation/suggested-practices/#referencing-vs-embedding>`_.
Each of the major STIX constructs are placed at the top level of the STIX package and relationships are formed by
reference.

==================================  =======
Line Number                         PhishMe
==================================  =======
1547                                Threat ID
1536                                Brand
1413, 1432, 1451, 1470, 1489, 1508  First Seen Date
1552                                Screenshot (URL)
1551                                ThreatHQ (URL)
18                                  Phishing Domain
25                                  Phishing Host
32                                  Phishing IPv4
48                                  Phishing URL
37                                  ASN
38                                  ASN Organization
62                                  Reported URL
55                                  Action URL
86, 139, 220, etc                   Web Components URL
75, 128, 209, etc                   Web Components MD5
79, 132, 213, etc                   Web Components SHA-1
70, 123, 204, etc                   Web Components File Extension
69, 122, 203, etc                   Web Components File Name
71, 124, 205, etc                   Web Components File Size
1155, 1192, 1229, 1266, 1303        Drop Email Address
1179, 1216, 1253, 1290, 1327        Drop Email Obfuscation
1163, 1200, 1237, 1274, 1311        Drop Email File Name
1164, 1201, 1238, 1275, 1312        Drop Email File Extension
1168, 1205, 1242, 1279, 1316        Drop Email File MD5
==================================  =======

**STIX Schema**::

    <stix:STIX_Package id="PhishMe:Package-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-25T11:50:00.370-05:00" version="1.1.1">
        <stix:STIX_Header>
            <stix:Title>PhishMe Phish ThreatID 19979634</stix:Title>
            <stix:Package_Intent xsi:type="stixVocabs:PackageIntentVocab-1.0">Indicators - Phishing</stix:Package_Intent>
            <stix:Information_Source>
                <stixCommon:Identity>
                    <stixCommon:Name>PhishMe, Inc - Machine Readable Threat Intelligence Feed</stixCommon:Name>
                </stixCommon:Identity>
                <stixCommon:Time>
                    <cyboxCommon:Produced_Time>2015-06-25T11:50:00.686-05:00</cyboxCommon:Produced_Time>
                </stixCommon:Time>
            </stix:Information_Source>
        </stix:STIX_Header>
        <stix:Observables cybox_major_version="2" cybox_minor_version="1" cybox_update_version="0">
            <cybox:Observable id="PhishMe:Observable-737d1b24-70cc-4781-b306-c2535da5306b">
                <cybox:Object id="PhishMe:DomainName-0bd282c2-d2ff-4e32-b74d-54eff62ae1ae">
                    <cybox:Properties xsi:type="DomainNameObj:DomainNameObjectType">
                        <DomainNameObj:Value condition="Equals">dental-aesthetic-tourism-belgrade.com</DomainNameObj:Value>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-fed2cee1-b27d-41bf-b832-c9f0cccf7fc5">
                <cybox:Object id="PhishMe:Hostname-7da00a8e-c654-4ee0-ae2e-90ad7f5ed01e">
                    <cybox:Properties xsi:type="HostnameObj:HostnameObjectType">
                        <HostnameObj:Hostname_Value condition="Equals">dental-aesthetic-tourism-belgrade.com</HostnameObj:Hostname_Value>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-c923c2c7-d7a0-476d-8536-09dc1709164a">
                <cybox:Object id="PhishMe:Address-7b315615-d1e4-4162-bfb3-993667429cfe">
                    <cybox:Properties xsi:type="AddressObj:AddressObjectType">
                        <AddressObj:Address_Value condition="Equals">130.255.185.23</AddressObj:Address_Value>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:AutonomousSystem-80d23549-2fc8-4ff9-a2f7-37ff703b215b">
                            <cybox:Properties xsi:type="ASObj:ASObjectType">
                                <ASObj:Number condition="Equals">29141</ASObj:Number>
                                <ASObj:Name condition="Equals">Bradler & Krantz GmbH & Co. KG</ASObj:Name>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Related_To</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-21b99334-9c8f-4458-a913-f42b69f1c6aa">
                <cybox:Object id="PhishMe:URI-ca33faa7-22f2-45b9-b1ff-c5e5a599d4e4">
                    <cybox:Properties type="URL" xsi:type="URIObj:URIObjectType">
                        <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate</URIObj:Value>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-23e5527e-a578-41cb-837f-d0faa5947229">
                <cybox:Object id="PhishMe:URI-74304689-5a91-4682-86a6-36fc36b6193a">
                    <cybox:Properties type="URL" xsi:type="URIObj:URIObjectType">
                        <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/ubs.php</URIObj:Value>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-8005cd6e-6e4f-4703-bf72-fe27b28bedde">
                <cybox:Object id="PhishMe:URI-70fa0d50-84db-475c-9ee7-8ef5deaeea99">
                    <cybox:Properties type="URL" xsi:type="URIObj:URIObjectType">
                        <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/</URIObj:Value>
                    </cybox:Properties>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-987590dc-05c8-4fb3-9b08-cc58e309b2ea">
                <cybox:Object id="PhishMe:Observable-021bc40d-e9e4-49e5-94f6-dabff314c9e1">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>nav_bottom_center2.gif</FileObj:File_Name>
                        <FileObj:File_Extension>.gif</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>81</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>c6f70ce0f1589d5a10df0a0af3d27184</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>ad656b68e193728c8db3b1911d117edda427d8df</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-8b6d7001-cab8-49d8-a966-fe57461c8b5b">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/nav_bottom_center2.gif</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-fe471465-934d-41ae-8e49-e462e1ddf3c6">
                <cybox:Object id="PhishMe:Observable-43d6e257-6eed-4aca-b9d3-473e715663c8">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name/>
                        <FileObj:Size_In_Bytes>10636</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>48b0f845c887460a645fda4ea00e05f1</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>deac7391a013158ed98b58d19da0942b7898e9bd</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-58926fc1-ab50-41d6-9af7-986f7d0f2bab">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-700dea4b-b789-499a-8272-3f4b97c62216">
                <cybox:Object id="PhishMe:Observable-c99180b4-63bd-4dc5-be91-37c016e591ef">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>title_login.gif</FileObj:File_Name>
                        <FileObj:File_Extension>.gif</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>442</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>920f9986196d2665391c11842283ea1f</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>d12f174f59e3d94c8d32c1305c83358309388035</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-1d43f513-eb40-4c7b-9a16-059e9a307fca">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/title_login.gif</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-e4259f34-25de-444f-9255-4253526ce3aa">
                <cybox:Object id="PhishMe:Observable-d084ab1e-8bef-4fa1-8114-06332b4a305b">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>questionmark.gif</FileObj:File_Name>
                        <FileObj:File_Extension>.gif</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>632</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>63000e25a9688a60460d5c52fa867a2d</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>0682fe722f6d3f27266bb26678e6a63668c0cd99</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-49a962d9-b557-4d03-8b2d-c01d3fc037ca">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/questionmark.gif</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-75be1a49-e390-4849-926d-705bca1cb9f3">
                <cybox:Object id="PhishMe:Observable-6d7a42ea-92e8-4180-9b47-bbab935de6ed">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>e_pic3_classic.jpg</FileObj:File_Name>
                        <FileObj:File_Extension>.jpg</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>8419</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>448b4eec5089674b3c0e46f556037566</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>b9531bc1a6cca9200139e0a1e89bbc36a3ded652</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-d7ca86dd-9683-4f87-8e93-40e00f3f493c">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/e_pic3_classic.jpg</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-703e8338-4cf7-4023-ade4-f1a1c8835cda">
                <cybox:Object id="PhishMe:Observable-d775ca6d-f930-4b3d-8291-61f67735ddcb">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>msiefix.js</FileObj:File_Name>
                        <FileObj:File_Extension>.js</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>27</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>23256d0571a87a6daf906c2999d7ad41</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>0015fdc81f4353877f8e9503fc7e0115159d654e</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-51f1aa93-fc70-46a7-bc4a-81b6f7bb6e90">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/msiefix.js</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-302f8fe5-3d1d-4db7-88bb-b275db2ee386">
                <cybox:Object id="PhishMe:Observable-34c120ae-04f8-4fa9-8b39-f2d2eaf5f142">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>default.js</FileObj:File_Name>
                        <FileObj:File_Extension>.js</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>29411</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>5921b0286496f675eca4c4faa7400262</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>1e4ddfb9aaea82321b770531e16db41b04a4660c</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-28c0970b-e7c5-452d-9689-cc6968c81e7a">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/default.js</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-810c98d7-3318-4871-a468-328fa0538ac0">
                <cybox:Object id="PhishMe:Observable-525b2b61-9775-4d97-a2b9-157bf900c082">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>compass_top.gif</FileObj:File_Name>
                        <FileObj:File_Extension>.gif</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>4870</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>4248a5d428854cccee954133bceeb2a4</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>38b726edbe4ababd995ada19bed9b07dbeffc6fd</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-22ee116c-e954-481d-b1f1-f8d3e874d7de">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/compass_top.gif</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-94d54b3c-5cb8-4440-b909-501ef2d4d5da">
                <cybox:Object id="PhishMe:Observable-1cf6fa34-0180-413b-8592-53d41ae7c3cf">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>default.css</FileObj:File_Name>
                        <FileObj:File_Extension>.css</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>149429</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>9712c35ff94f4ce43abc3220f26af72f</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>0646f936205df44b29e921f3583fd03c5c1732e9</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-7dbe57a9-e032-4a68-8f01-88999d57da65">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/default.css</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-2a1137d7-b72c-4086-b07d-8e5c04e776ef">
                <cybox:Object id="PhishMe:Observable-3ad469d4-db08-4a2f-9037-53707968da3c">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>logo_ubs_17.gif</FileObj:File_Name>
                        <FileObj:File_Extension>.gif</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>545</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>fe0dfce731c3c3affd9be00ecb305bc9</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>f46f268bf2ea733d07997aa69421f31a07f0371f</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-e85cf0a6-c144-4111-9756-4b278d27d3b7">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/logo_ubs_17.gif</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-8e25f148-1841-4a14-b11d-22ebf94eed39">
                <cybox:Object id="PhishMe:Observable-60b12518-aca5-4698-971b-9282d6087a19">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>ubsupdate</FileObj:File_Name>
                        <FileObj:Size_In_Bytes>10636</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>48b0f845c887460a645fda4ea00e05f1</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>deac7391a013158ed98b58d19da0942b7898e9bd</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-ee8758c5-fcff-4dd1-b600-1ca31d40ac8a">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-4b162f7a-f4a4-478f-8956-46e6577328d9">
                <cybox:Object id="PhishMe:Observable-26bcb70e-78b9-48ad-97c9-3c2810dbb92f">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>nav_top_center.gif</FileObj:File_Name>
                        <FileObj:File_Extension>.gif</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>60</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>4ec04eafadf4a6d837e0dab52a709b13</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>c44df1fe967caa376fc6c5d109d0251fd78818c0</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-18f40d89-f391-4bdc-a7d8-f790360e1e56">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/nav_top_center.gif</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-5fbf2a60-266f-44a6-b22b-048539afac25">
                <cybox:Object id="PhishMe:Observable-3b18bf9f-7281-47ca-8c91-6c996e7deaa6">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>compass_bottom.gif</FileObj:File_Name>
                        <FileObj:File_Extension>.gif</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>4795</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>091ae3c4578974302161de4c55bcb160</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>61e12faa8c935c1fbea7e80285737db681532b43</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-fa973147-89c7-403b-9380-24f96e7e44e2">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/compass_bottom.gif</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-00c39488-0a65-4313-82a3-408da782befe">
                <cybox:Object id="PhishMe:Observable-8a75f856-d8dd-4940-81d0-4db311bd1cb7">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>e_pic2_classic.jpg</FileObj:File_Name>
                        <FileObj:File_Extension>.jpg</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>16928</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>e71cb071dfc401ff2403ed8586fee86b</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>797b485cb61e2e1e53d6c89d9747f4c451698287</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-f5a6527e-4108-49d0-9c2f-1f8cd72ef272">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/e_pic2_classic.jpg</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-8abdf863-9238-4403-9347-39baa7651ef3">
                <cybox:Object id="PhishMe:Observable-c1a8a3c1-0d2f-420c-ac70-de53d1af97a8">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:File_Name>login4.jpg</FileObj:File_Name>
                        <FileObj:File_Extension>.jpg</FileObj:File_Extension>
                        <FileObj:Size_In_Bytes>39339</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>670ad40bc372293bedca2b6e6f50d475</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>4f6db6c4e159ea21f80de8c7ef7867e89652e194</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:URI-bd49e4d3-f1b4-4d1d-9985-8e12c70305ea">
                            <cybox:Properties xsi:type="URIObj:URIObjectType">
                                <URIObj:Value condition="Equals">http://dental-aesthetic-tourism-belgrade.com/ubsupdate/index_files/login4.jpg</URIObj:Value>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Downloaded_From</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-c60c8683-b428-45d9-836d-08598b478593">
                <cybox:Description>Phishing kit was recovered from this phishing site</cybox:Description>
                <cybox:Object id="PhishMe:File-58fe101b-5e23-475d-98a4-a2867f7dd641">
                    <cybox:Properties xsi:type="FileObj:FileObjectType">
                        <FileObj:Size_In_Bytes condition="Equals">409954</FileObj:Size_In_Bytes>
                        <FileObj:Hashes>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>2a91c8eb5196bfdc2c6e1157c7b707bb</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                            <cyboxCommon:Hash>
                                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">SHA1</cyboxCommon:Type>
                                <cyboxCommon:Simple_Hash_Value>792051018311cb5cfbb013235c51e8ef30247a46</cyboxCommon:Simple_Hash_Value>
                            </cyboxCommon:Hash>
                        </FileObj:Hashes>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:File-0f94bc40-55ef-4228-b237-ffe587827958">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">questionmark.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>632</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>63000e25a9688a60460d5c52fa867a2d</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-8261fc74-9a04-43d0-8389-43cc34165850">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">nav_top_center.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>60</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>4ec04eafadf4a6d837e0dab52a709b13</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-8e4f50d8-2894-4fe8-8fab-977a03bf11b3">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">compass_bottom.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>4795</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>091ae3c4578974302161de4c55bcb160</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-112c8554-3594-4061-ae93-1df8b8d3f047">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">f_pic3_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>8419</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>448b4eec5089674b3c0e46f556037566</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-92b86880-7a29-4ff0-8152-ecc27e1461e5">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">login4.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>39339</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>670ad40bc372293bedca2b6e6f50d475</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-33f36296-208e-490a-9425-10c96aa0d3df">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">questionmark.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>632</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>63000e25a9688a60460d5c52fa867a2d</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-50e877cf-fe6f-4628-bbfd-5d7255b35921">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">compass_top.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>4870</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>4248a5d428854cccee954133bceeb2a4</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-720393b9-04b8-4678-a093-b0cc41f07d7d">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">g_pic3_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>8419</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>448b4eec5089674b3c0e46f556037566</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-3231b28c-67f1-4abc-b401-b7f10348f33d">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">nav_bottom_center2.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>81</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>c6f70ce0f1589d5a10df0a0af3d27184</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-fe67ef50-3d98-4c76-b90e-e4133fb7d3d5">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">logo_ubs_17.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>545</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>fe0dfce731c3c3affd9be00ecb305bc9</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-f200f865-02f7-4453-b1c1-3ede4b8ceabd">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">nav_bottom_center2.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>81</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>c6f70ce0f1589d5a10df0a0af3d27184</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-b0534794-640a-4e6f-9008-af5e846d4e9b">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">e_pic3_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>8419</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>448b4eec5089674b3c0e46f556037566</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-136a3d12-7345-47ef-93f2-a3cd7f13026a">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">compass_top.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>4870</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>4248a5d428854cccee954133bceeb2a4</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-5dddaeaa-a0b2-4762-bfb0-de850ee18265">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">Thumbs.db</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.db</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>54784</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>3ce8a7b07a9289c06dd75c6b223192c4</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-cbc83957-14f0-452a-9eaf-b95088a5023a">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">ita.html</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.html</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>10906</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>0d7100d6529f22576b5cc44c7839b902</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-99bdeaa6-19b0-49e0-b6a8-e37ef4b28dcd">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">deu.html</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.html</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>10792</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>005208b87625177e43984c953f87f76c</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-141f95fa-2314-4a92-b336-376704e73af0">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">i_pic2_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>17172</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>e6c6fb4d890665a05c0d69ca055f903f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-c9864262-6bc0-46f5-8a58-58ade03f1ace">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">ubs.php</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.php</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>796</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>4949f6f2c75dfbfc01a9fab14cdb644f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-4da21156-1b66-44aa-91bc-1f894ebe5dc5">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">default.css</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.css</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>149429</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>9712c35ff94f4ce43abc3220f26af72f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-7711d1dd-9a87-4e14-bd1f-d46f2d508cfe">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">i_pic2_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>17172</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>e6c6fb4d890665a05c0d69ca055f903f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-84768575-4a7d-4fae-a68f-4dd851e9bd62">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">e_pic2_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>16928</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>e71cb071dfc401ff2403ed8586fee86b</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-3b5ba66c-a5e5-442b-9bc9-50766c9c1fa4">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">logo_ubs_17.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>545</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>fe0dfce731c3c3affd9be00ecb305bc9</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-d792dd9e-cdb0-4c77-9447-5b5311da5c4a">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">msiefix.js</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.js</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>27</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>23256d0571a87a6daf906c2999d7ad41</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-a7370d69-8ffd-40c5-9641-35f7a460f63f">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">g_pic3_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>8419</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>448b4eec5089674b3c0e46f556037566</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-caf1af29-0fa6-4154-be55-b2d4b75b1b3d">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">Thumbs.db</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.db</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>54784</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>01362be01070aff21867f32bafe9d669</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-5de9ae42-6ff6-42af-ad81-0784a5596dab">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">fra.html</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.html</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>11062</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>1d3d6e1d0089d5df4c86f7693f8dac04</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-3313181d-83f1-4988-ba49-0bf424503a3e">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">i_pic3_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>8419</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>448b4eec5089674b3c0e46f556037566</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-cc7d8fa2-ae66-4a2c-84f6-7642d5f1db75">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">i_pic3_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>8419</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>448b4eec5089674b3c0e46f556037566</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-b0fc4d0b-f83f-49f2-9ecf-0d143073426b">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">e_pic2_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>16928</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>e71cb071dfc401ff2403ed8586fee86b</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-3e4d4b38-344e-41cb-aeae-a67398df5b4f">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">login4.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>39339</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>670ad40bc372293bedca2b6e6f50d475</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-23d10a9d-9cfd-4838-9167-c550b85e163b">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">g_pic2_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>17375</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>d798b20455c627d7b551f4e3eb55a757</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-9ac890dc-82bb-43fb-a674-017382388a35">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">index.html</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.html</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>10636</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>48b0f845c887460a645fda4ea00e05f1</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-6744bee9-3875-40fe-b953-11685ae72b59">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">nav_top_center.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>60</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>4ec04eafadf4a6d837e0dab52a709b13</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-68b72427-1d86-4b43-afa3-17860f7f3bcb">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">g_pic2_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>17375</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>d798b20455c627d7b551f4e3eb55a757</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-c8e5c05a-bdc2-4392-a81f-7854013d06ce">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">title_login.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>442</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>920f9986196d2665391c11842283ea1f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-5ea17a71-b6b9-42be-8cf9-448c1c6cc45c">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">default.js</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.js</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>29411</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>5921b0286496f675eca4c4faa7400262</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-c8219703-2b3b-494b-b93e-034e5033d686">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">compass_bottom.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>4795</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>091ae3c4578974302161de4c55bcb160</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-01ead1d2-2c95-4df2-82da-228ce844cb09">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">title_login.gif</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.gif</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>442</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>920f9986196d2665391c11842283ea1f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-92cdff63-f5fb-4647-afdf-5d0a137022a0">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">e_pic3_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>8419</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>448b4eec5089674b3c0e46f556037566</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-b0ce61f7-acfd-4b05-9130-88cb13873650">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">f_pic3_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>8419</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>448b4eec5089674b3c0e46f556037566</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-7f98d8b5-0935-4aef-84e8-75465df667a0">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">f_pic2_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>17353</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>2b78b5e8be01667ca8b56cd2def5a6d3</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-23ca0bc7-a3fa-4ec0-bde3-33d367c1910f">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">default.css</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.css</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>149429</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>9712c35ff94f4ce43abc3220f26af72f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-4d74c45d-2e91-4ea5-8cbb-4514b6ae7952">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">f_pic2_classic.jpg</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.jpg</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>17353</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>2b78b5e8be01667ca8b56cd2def5a6d3</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-f8ee4e93-2bf3-4a13-9aee-9e54c8562ae0">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">default.js</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.js</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>29411</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>5921b0286496f675eca4c4faa7400262</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-25c5073f-a4d8-4126-ac8b-02a2e02a08c4">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">favicon.ico</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.ico</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>3238</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>7b7b354daed8f6947b527dba0c8aff2e</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-4f59b05f-9ad6-4fb2-bb9c-47c315254d40">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">msiefix.js</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.js</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>27</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>23256d0571a87a6daf906c2999d7ad41</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                        <cybox:Related_Object id="PhishMe:File-afe889b4-4aa7-4235-b8c2-949bf331bfda">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">favicon.ico</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.ico</FileObj:File_Extension>
                                <FileObj:Size_In_Bytes>3238</FileObj:Size_In_Bytes>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>7b7b354daed8f6947b527dba0c8aff2e</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contains</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-649ab2e6-e0a0-4eb5-b55b-917097dd8f63">
                <cybox:Title>Possible drop email address</cybox:Title>
                <cybox:Description>This email address was found within a phishing kit and may be the recipient of credentials stolen by phish created from this kit.</cybox:Description>
                <cybox:Object id="PhishMe:EmailMessage-c7212865-b557-42cc-b8b9-f5f4cf9a5c0a">
                    <cybox:Properties xsi:type="EmailMessageObj:EmailMessageObjectType">
                        <EmailMessageObj:Header>
                            <EmailMessageObj:To>
                                <EmailMessageObj:Recipient category="e-mail" xsi:type="AddressObj:AddressObjectType">
                                    <AddressObj:Address_Value>ubs@razorhack.com</AddressObj:Address_Value>
                                </EmailMessageObj:Recipient>
                            </EmailMessageObj:To>
                        </EmailMessageObj:Header>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:File-a0bf05cf-2fd0-4519-9b2b-8e234908bd23">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">ubs.php</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.php</FileObj:File_Extension>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>4949f6f2c75dfbfc01a9fab14cdb644f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contained_Within</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
                <cybox:Pattern_Fidelity>
                    <cybox:Evasion_Techniques>
                        <cybox:Obfuscation_Technique>
                            <cybox:Description>plaintext</cybox:Description>
                        </cybox:Obfuscation_Technique>
                    </cybox:Evasion_Techniques>
                </cybox:Pattern_Fidelity>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-615b1925-026f-442f-9130-a6dd1a780158">
                <cybox:Title>Possible drop email address</cybox:Title>
                <cybox:Description>This email address was found within a phishing kit and may be the recipient of credentials stolen by phish created from this kit.</cybox:Description>
                <cybox:Object id="PhishMe:EmailMessage-617d582a-f7ef-4d8e-aba8-8e48be72f17d">
                    <cybox:Properties xsi:type="EmailMessageObj:EmailMessageObjectType">
                        <EmailMessageObj:Header>
                            <EmailMessageObj:To>
                                <EmailMessageObj:Recipient category="e-mail" xsi:type="AddressObj:AddressObjectType">
                                    <AddressObj:Address_Value>uzzilogs@outlook.com</AddressObj:Address_Value>
                                </EmailMessageObj:Recipient>
                            </EmailMessageObj:To>
                        </EmailMessageObj:Header>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:File-ed409b46-3581-42a3-8179-32506ef3ba9a">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">ubs.php</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.php</FileObj:File_Extension>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>4949f6f2c75dfbfc01a9fab14cdb644f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contained_Within</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
                <cybox:Pattern_Fidelity>
                    <cybox:Evasion_Techniques>
                        <cybox:Obfuscation_Technique>
                            <cybox:Description>plaintext</cybox:Description>
                        </cybox:Obfuscation_Technique>
                    </cybox:Evasion_Techniques>
                </cybox:Pattern_Fidelity>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-cf8e137c-92a6-4c88-abae-16f105cb5c2c">
                <cybox:Title>Possible drop email address</cybox:Title>
                <cybox:Description>This email address was found within a phishing kit and may be the recipient of credentials stolen by phish created from this kit.</cybox:Description>
                <cybox:Object id="PhishMe:EmailMessage-b12937b8-bd71-4621-82e6-b6fdba1211e2">
                    <cybox:Properties xsi:type="EmailMessageObj:EmailMessageObjectType">
                        <EmailMessageObj:Header>
                            <EmailMessageObj:To>
                                <EmailMessageObj:Recipient category="e-mail" xsi:type="AddressObj:AddressObjectType">
                                    <AddressObj:Address_Value>c.2iit@yahoo.com</AddressObj:Address_Value>
                                </EmailMessageObj:Recipient>
                            </EmailMessageObj:To>
                        </EmailMessageObj:Header>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:File-ec72d013-b70c-4c46-b526-1739a4170ca7">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">ita.html</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.html</FileObj:File_Extension>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>0d7100d6529f22576b5cc44c7839b902</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contained_Within</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
                <cybox:Pattern_Fidelity>
                    <cybox:Evasion_Techniques>
                        <cybox:Obfuscation_Technique>
                            <cybox:Description>plaintext</cybox:Description>
                        </cybox:Obfuscation_Technique>
                    </cybox:Evasion_Techniques>
                </cybox:Pattern_Fidelity>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-f209383a-a133-4e53-96a9-1e52872c9a62">
                <cybox:Title>Possible drop email address</cybox:Title>
                <cybox:Description>This email address was found within a phishing kit and may be the recipient of credentials stolen by phish created from this kit.</cybox:Description>
                <cybox:Object id="PhishMe:EmailMessage-e0b07660-4f94-46d9-9ae0-107cbbe0ba29">
                    <cybox:Properties xsi:type="EmailMessageObj:EmailMessageObjectType">
                        <EmailMessageObj:Header>
                            <EmailMessageObj:To>
                                <EmailMessageObj:Recipient category="e-mail" xsi:type="AddressObj:AddressObjectType">
                                    <AddressObj:Address_Value>garangchol147@gmail.com</AddressObj:Address_Value>
                                </EmailMessageObj:Recipient>
                            </EmailMessageObj:To>
                        </EmailMessageObj:Header>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:File-fb7fcc28-b9b9-4494-b6a8-4ca904e0e488">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">ubs.php</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.php</FileObj:File_Extension>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>4949f6f2c75dfbfc01a9fab14cdb644f</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contained_Within</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
                <cybox:Pattern_Fidelity>
                    <cybox:Evasion_Techniques>
                        <cybox:Obfuscation_Technique>
                            <cybox:Description>plaintext</cybox:Description>
                        </cybox:Obfuscation_Technique>
                    </cybox:Evasion_Techniques>
                </cybox:Pattern_Fidelity>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-d3d02c2c-a4dc-44f4-a75b-e468bc5259e7">
                <cybox:Title>Possible drop email address</cybox:Title>
                <cybox:Description>This email address was found within a phishing kit and may be the recipient of credentials stolen by phish created from this kit.</cybox:Description>
                <cybox:Object id="PhishMe:EmailMessage-f465ac89-9b87-4c28-9b4d-09a4b8029786">
                    <cybox:Properties xsi:type="EmailMessageObj:EmailMessageObjectType">
                        <EmailMessageObj:Header>
                            <EmailMessageObj:To>
                                <EmailMessageObj:Recipient category="e-mail" xsi:type="AddressObj:AddressObjectType">
                                    <AddressObj:Address_Value>c.2iit@yahoo.com</AddressObj:Address_Value>
                                </EmailMessageObj:Recipient>
                            </EmailMessageObj:To>
                        </EmailMessageObj:Header>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:File-3545662b-a2e5-4148-8b66-8a40b9fe83db">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">index.html</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.html</FileObj:File_Extension>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>48b0f845c887460a645fda4ea00e05f1</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contained_Within</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
                <cybox:Pattern_Fidelity>
                    <cybox:Evasion_Techniques>
                        <cybox:Obfuscation_Technique>
                            <cybox:Description>plaintext</cybox:Description>
                        </cybox:Obfuscation_Technique>
                    </cybox:Evasion_Techniques>
                </cybox:Pattern_Fidelity>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-24290d8f-da5a-451f-8bf9-65d5c5349d30">
                <cybox:Title>Possible drop email address</cybox:Title>
                <cybox:Description>This email address was found within a phishing kit and may be the recipient of credentials stolen by phish created from this kit.</cybox:Description>
                <cybox:Object id="PhishMe:EmailMessage-2b8aee41-e7eb-4129-a380-7742ea3fd3dc">
                    <cybox:Properties xsi:type="EmailMessageObj:EmailMessageObjectType">
                        <EmailMessageObj:Header>
                            <EmailMessageObj:To>
                                <EmailMessageObj:Recipient category="e-mail" xsi:type="AddressObj:AddressObjectType">
                                    <AddressObj:Address_Value>c.2iit@yahoo.com</AddressObj:Address_Value>
                                </EmailMessageObj:Recipient>
                            </EmailMessageObj:To>
                        </EmailMessageObj:Header>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:File-e4b8d859-8113-4b86-9554-f43cf1c02e29">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">deu.html</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.html</FileObj:File_Extension>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>005208b87625177e43984c953f87f76c</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contained_Within</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
                <cybox:Pattern_Fidelity>
                    <cybox:Evasion_Techniques>
                        <cybox:Obfuscation_Technique>
                            <cybox:Description>plaintext</cybox:Description>
                        </cybox:Obfuscation_Technique>
                    </cybox:Evasion_Techniques>
                </cybox:Pattern_Fidelity>
            </cybox:Observable>
            <cybox:Observable id="PhishMe:Observable-d8358680-1233-4e0e-b574-0100fd62e590">
                <cybox:Title>Possible drop email address</cybox:Title>
                <cybox:Description>This email address was found within a phishing kit and may be the recipient of credentials stolen by phish created from this kit.</cybox:Description>
                <cybox:Object id="PhishMe:EmailMessage-d56fd075-c684-4202-9c2e-1e76d4149a49">
                    <cybox:Properties xsi:type="EmailMessageObj:EmailMessageObjectType">
                        <EmailMessageObj:Header>
                            <EmailMessageObj:To>
                                <EmailMessageObj:Recipient category="e-mail" xsi:type="AddressObj:AddressObjectType">
                                    <AddressObj:Address_Value>c.2iit@yahoo.com</AddressObj:Address_Value>
                                </EmailMessageObj:Recipient>
                            </EmailMessageObj:To>
                        </EmailMessageObj:Header>
                    </cybox:Properties>
                    <cybox:Related_Objects>
                        <cybox:Related_Object id="PhishMe:File-733c4aa1-f9d1-4e0e-8eb2-98268a7b1b80">
                            <cybox:Properties xsi:type="FileObj:FileObjectType">
                                <FileObj:File_Name condition="Equals">fra.html</FileObj:File_Name>
                                <FileObj:File_Extension condition="Equals">.html</FileObj:File_Extension>
                                <FileObj:Hashes>
                                    <cyboxCommon:Hash>
                                        <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0">MD5</cyboxCommon:Type>
                                        <cyboxCommon:Simple_Hash_Value>1d3d6e1d0089d5df4c86f7693f8dac04</cyboxCommon:Simple_Hash_Value>
                                    </cyboxCommon:Hash>
                                </FileObj:Hashes>
                            </cybox:Properties>
                            <cybox:Relationship xsi:type="cyboxVocabs:ObjectRelationshipVocab-1.1">Contained_Within</cybox:Relationship>
                        </cybox:Related_Object>
                    </cybox:Related_Objects>
                </cybox:Object>
                <cybox:Pattern_Fidelity>
                    <cybox:Evasion_Techniques>
                        <cybox:Obfuscation_Technique>
                            <cybox:Description>plaintext</cybox:Description>
                        </cybox:Obfuscation_Technique>
                    </cybox:Evasion_Techniques>
                </cybox:Pattern_Fidelity>
            </cybox:Observable>
        </stix:Observables>
        <stix:Indicators>
            <stix:Indicator id="PhishMe:indicator-bbc3e3ec-999d-4fc1-bbc8-d49dbdef7c8b" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>Phish Domain</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">Domain Watchlist</indicator:Type>
                <indicator:Description/>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-18T13:00:00.000-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Confidence timestamp="2015-06-18T13:00:00.000-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-e63c3bda-c630-41e1-a001-2b620ccb8a08" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>Phish Domain</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">Domain Watchlist</indicator:Type>
                <indicator:Description/>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-18T13:00:00.000-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Confidence timestamp="2015-06-18T13:00:00.000-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-e1726507-0b5d-4661-892d-84eb4e9d055e" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>Phish IP</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">IP Watchlist</indicator:Type>
                <indicator:Description/>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-18T13:00:00.000-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Confidence timestamp="2015-06-18T13:00:00.000-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-ebd86b0a-8e21-49fe-9619-e20a6503e3dd" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>Reported URL</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">URL Watchlist</indicator:Type>
                <indicator:Description>Original URL reported to PhishMe.</indicator:Description>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-18T13:00:00.000-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Confidence timestamp="2015-06-18T13:00:00.000-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-bebc2331-d5db-49f2-9cae-0aed9c019e47" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>Action URL</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">URL Watchlist</indicator:Type>
                <indicator:Description>The next URL to be called when the victim submits their information to the phishing site.</indicator:Description>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-18T13:00:00.000-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Confidence timestamp="2015-06-18T13:00:00.000-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
            <stix:Indicator id="PhishMe:indicator-5994adbf-d4d8-4945-81c5-00aca8a20bb4" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="indicator:IndicatorType">
                <indicator:Title>Phish URL</indicator:Title>
                <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">URL Watchlist</indicator:Type>
                <indicator:Description/>
                <indicator:Valid_Time_Position>
                    <indicator:Start_Time precision="second">2015-06-18T13:00:00.000-05:00</indicator:Start_Time>
                </indicator:Valid_Time_Position>
                <indicator:Indicated_TTP>
                    <stixCommon:TTP idref="PhishMe:ttp-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="ttp:TTPType"/>
                </indicator:Indicated_TTP>
                <indicator:Confidence timestamp="2015-06-18T13:00:00.000-05:00">
                    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
                </indicator:Confidence>
                <indicator:Related_Campaigns>
                    <indicator:Related_Campaign>
                        <stixCommon:Campaign idref="PhishMe:Campaign-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00"/>
                    </indicator:Related_Campaign>
                </indicator:Related_Campaigns>
            </stix:Indicator>
        </stix:Indicators>
        <stix:TTPs>
            <stix:TTP id="PhishMe:ttp-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="ttp:TTPType">
                <ttp:Title>Phishing</ttp:Title>
                <ttp:Behavior>
                    <ttp:Attack_Patterns>
                        <ttp:Attack_Pattern capec_id="CAPEC-98">
                            <ttp:Description>Phishing</ttp:Description>
                        </ttp:Attack_Pattern>
                    </ttp:Attack_Patterns>
                </ttp:Behavior>
                <ttp:Resources>
                    <ttp:Personas>
                        <ttp:Persona>
                            <stixCommon:Name>UBS</stixCommon:Name>
                        </ttp:Persona>
                    </ttp:Personas>
                </ttp:Resources>
                <ttp:Victim_Targeting>
                    <ttp:Targeted_Information xsi:type="stixVocabs:InformationTypeVocab-1.0">Information Assets - User Credentials</ttp:Targeted_Information>
                </ttp:Victim_Targeting>
            </stix:TTP>
        </stix:TTPs>
        <stix:Campaigns>
            <stix:Campaign id="PhishMe:Campaign-d02eb4cc-92f8-4f1e-b628-5e138f1b7f37" timestamp="2015-06-18T13:00:00.000-05:00" xsi:type="campaign:CampaignType">
                <campaign:Title>19979634</campaign:Title>
                <campaign:Description>UBS</campaign:Description>
                <campaign:Information_Source>
                    <stixCommon:References>
                        <stixCommon:Reference>https://www.threathq.com/p42/search/default?p=19979634</stixCommon:Reference>
                        <stixCommon:Reference>https://www.threathq.com/apiv1/screenshot/19979634</stixCommon:Reference>
                    </stixCommon:References>
                </campaign:Information_Source>
            </stix:Campaign>
        </stix:Campaigns>
    </stix:STIX_Package>