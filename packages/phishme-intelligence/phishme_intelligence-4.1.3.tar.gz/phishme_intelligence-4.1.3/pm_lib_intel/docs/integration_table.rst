.. _integrations:

======================
Supported Integrations
======================

.. note:: This is the current list of integrations that are supported for PhishMe Intelligence. If you have a product
          you'd like to use with PhishMe Intelligence, please contact us at support@phishme.com and our Solutions
          Engineers would be happy to discuss it with you.


.. list-table::
    :widths:  10, 30, 5, 10, 20, 25
    :header-rows: 1

    * - Vendor
      - Product
      - Version
      - Status
      - Deployment Type
      - Additional Information
    * - Anomali
      - :ref:`ThreatStream <anomali_threatstream>`
      -
      - Certified
      - Direct integration
      -
    * - Carbon Black
      - :ref:`CB Response <cb_response>`
      -
      - Supported
      - Standalone Python
      -
    * - Centripetal
      - :ref:`QuickThreat <centripetal_quickthreat>`
      -
      - Supported
      - Standalone Python
      -
    * - EclecticIQ
      - :ref:`EclecticIQ <eclecticiq>`
      -
      - Certified
      - Direct Integration
      -
    * - FireEye
      - :ref:`FireEye Security Orchestrator <fireeye_security_orchestrator>`
      - 4.2+
      - Certified
      - App
      -
    * - HPE
      - :ref:`Arcsight <arcsight>`
      - 6.0+
      - Certified
      - Standalone Python
      -
    * - IBM
      - :ref:`QRadar <qradar>`
      - 7.2.6+
      - Supported
      - Standalone Python
      - `Download from XForce <https://exchange.xforce.ibmcloud.com/hub/extension/4a57fd0a91c70d9be6a2705f40462477>`_
    * - LogRhythm
      - :ref:`LogRhythm <logrhythm>`
      -
      - Supported
      - Standalone Python
      -
    * - McAfee
      - :ref:`McAfee SIEM <mcafee_siem>`
      - 9.5+
      - Certified
      - Standalone Python
      - `Configuration of Event Receivers <https://kc.mcafee.com/resources/sites/MCAFEE/content/live/PRODUCT_DOCUMENTATION/26000/PD26993/en_US/esm_data_source_rg_rev_b_en-us.pdf>`_
    * - MITRE
      - :ref:`CRITs <crits>`
      - 4-master
      - Supported
      - Standalone Python
      -
    * - Palo Alto Networks
      - :ref:`MineMeld <paloalto_minemeld>`
      - 0.9.26+
      - Certified
      - Direct Integration
      - `MineMeld Community <https://live.paloaltonetworks.com/t5/MineMeld/ct-p/MineMeld>`_
    * - Phantom
      - :ref:`Phantom Platform <phantom>`
      - 2.0+
      - Certified
      - App
      - `Phantom Apps <https://www.phantom.us/apps/>`_
    * - Recorded Future
      - :ref:`Recorded Future <recorded_future>`
      -
      - Certified
      - Direct Integration
      -
    * - Splunk
      - :ref:`Splunk Enterprise <splunk_enterprise>`
      - 6.2+
      - Certified
      - App
      -
    * - Swimlane
      - Swimlane
      -
      - In Development
      -
      -
    * - ThreatConnect
      - :ref:`ThreatConnect <threatconnect>`
      - 4.3+
      - Certified
      - App
      - Available in TC Exchange
    * - ThreatQuotient
      - :ref:`ThreatQ <threatq>`
      - 3.1+
      - Certified
      - Direct Integration
      -
    * - Trend Micro
      - :ref:`TippingPoint IPS <tippingpoint_ips>`
      - 4.1+
      - Supported
      - Standalone python
      - Trend Micro does not have a formal certification program for this product.


**Status**

    * Certified: Vendor has independently verified that the PhishMe Intelligence integration has been built according
      to best practices set forth by that vendor.
    * Supported: PhishMe is still pursuing certification with that vendor (if applicable).
    * In Development: PhishMe Intelligence integration is currently under development

**Deployment Type**

    * Direct Integration: You'll only need to generate PhishMe Intelligence API credentials and add them to your
      existing product.
    * App: You'll simply add our integration through the vendor's App Store or as an available module, then configure
      the integration with a set of API credentials (plus whatever other configuration is specifically required by the
      integration).
    * Standalone python: You'll need to provide a space on a server meeting the
      :ref:`technical requirements <standalone_configuration>`




