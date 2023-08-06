.. _tippingpoint_ips:

=================
Tipping Point IPS
=================

.. note:: This integration is part of the Python standalone integration. Please see :ref:`here <standalone_configuration>`
          and :ref:`here <general_configuration>` for additional information and email support@phishme.com to request
          the standalone integration.

.. rst-class:: html-toggle

Overview
--------

PhishMe places IOCs into the TippingPoint SMS's Reputation Database. Each IOC is fed with several user-defined tags that
can be used to build block or alert policies within the SMS.

.. rst-class:: html-toggle

Integration Setup Prerequisites
-------------------------------

    * Access to Tipping Point SMS on port 443.
    * Create a policy on the SMS for PhishMe Intelligence.

A user account will need to be created on the SMS and credentials will be placed into the config.ini provided by
PhishMe. In the TippingPoint SMS, upload the user-defined Tag Categories provided by
:download:`PhishMe Intelligence import tags.xml </standalone_integration_tippingpoint_ips/PhishMe Intelligence import tags.xml>`.

.. image:: /standalone_integration_tippingpoint_ips/screenshot_1.jpeg

.. rst-class:: html-toggle

Sample config.ini
-----------------

config.ini example::

    [integration_tipping_point_ips]
    use = False
    ssl_verify = False
    host_with_protocol =
    user =
    pass =
    impact_major = True
    impact_moderate = True
    impact_minor = False
    impact_none = False

.. rst-class:: html-toggle

config.ini Descriptions
-----------------------

.. list-table::
    :widths:  10, 10, 70, 10
    :header-rows: 1

    * - Section
      - Key
      - Description
      - Required
    * - integration_tipping_point_ips
      - use
      - A Boolean value to control whether the integration outputs to TippingPoint IPS
      - True
    * - integration_tipping_point_ips
      - ssl_verify
      - A Boolean value to control whether the SSL certificate used for a connection to TippingPoint IPS should be
        verified
      - True
    * - integration_tipping_point_ips
      - host_with_protocol
      - The destination hostname or IPv4 address (with protocol) of the TippingPoint IPS instance
      - True
    * - integration_tipping_point_ips
      - user
      - The username used to access the TippingPoint IPS instance
      - True
    * - integration_tipping_point_ips
      - pass
      - The password used to access the TippingPoint IPS instance
      - True
    * - integration_tipping_point_ips
      - impact_major
      - Boolean used to indicator whether impact Major indicators should be sent to TippingPoint IPS
      - True
    * - integration_tipping_point_ips
      - impact_moderate
      - Boolean used to indicator whether impact Moderate indicators should be sent to TippingPoint IPS
      - True
    * - integration_tipping_point_ips
      - impact_minor
      - Boolean used to indicator whether impact Minor indicators should be sent to TippingPoint IPS
      - True
    * - integration_tipping_point_ips
      - impact_none
      - Boolean used to indicator whether impact None indicators should be sent to TippingPoint IPS
      - True

.. rst-class:: html-toggle

Features
--------

Each IOC will have the following tags which can be used to create Policies. PhishMe recommends using the
*PhishMeIntel_Impact-Rating == Major* in a blocking policy and *PhishMeIntel_Impact-Rating == Moderate* in either a
blocking or an alerting policy. The other tags can be used to understand additional context about the IOC in question.

    * PhishMeIntel_Impact-Rating
    * PhishMeIntel_Last-Published
    * PhishMeIntel_Malware-Family
    * PhishMeIntel_Role
    * PhishMeIntel_Threat-ID

.. image:: /standalone_integration_tippingpoint_ips/screenshot_2.jpeg
