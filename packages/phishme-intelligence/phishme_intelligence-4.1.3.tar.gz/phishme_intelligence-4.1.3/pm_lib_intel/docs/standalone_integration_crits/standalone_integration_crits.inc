.. _crits:

=====
CRITs
=====

.. note:: This integration is part of the Python standalone integration. Please see :ref:`here <standalone_configuration>`
          and :ref:`here <general_configuration>` for additional information and email support@phishme.com to request
          the standalone integration.

.. image:: /standalone_integration_crits/crits_logo.png

.. rst-class:: html-toggle

Integration Setup Prerequisites
-------------------------------

    * Access to your CRITs instance over TCP port 443 or port 80 (depending on whether you have SSL set up)
    * CRITs API Key (An API Key role created under a user in CRITs)

.. rst-class:: html-toggle

Overview
--------

PhishMe Intelligence data is organized into Campaign TLOs, which correspond to a Threat ID in PhishMe Intelligence.
Each Campaign has one or more Sample TLOs (file-based indicators) and Indicator TLOs (network-based Indicators).

.. rst-class:: html-toggle

Getting Started
---------------

**Turn On API Access on CRITs Server**

If you have not already done so you will need to enable API Access to your CRITs server; this integration uses the CRITs
Authenticated API to populate data.  As a user with administrative privileges in CRITs select the **CRITs Control Panel**
from the Navigation Menu (the "gear" icon in the top left corner) and select SYSTEM and then General (this should
generally be selected by default). Click the **Enable api:** checkbox.

.. image:: /standalone_integration_crits/crits_screenshot_1.jpeg

.. note:: You will need to restart the web server for the change to take effect.

**Get API Key**

In CRITs API Keys are generated under a user account. Once you have determined which user account you want to use login
to that account and select **My CRITs** from the Navigation Menu (the "gear" icon in the top left corner). Select the
**My API Keys** tab. You can either choose to just use the default API key or create a new key and use that.

.. image:: /standalone_integration_crits/crits_screenshot_2.jpeg

**Create Source for PhishMe Intelligence**

You will either need to use an existing Source or (recommended) create a new Source for PhishMe Intelligence inside the
CRITs instance. Select **Add New Item > Source** from the Navigation Menu (the "gear" icon in the top left corner). Give
a name for the Source (e.g. "PhishMe" or "PhishMe Intelligence") and click the **New Source** button.

.. image:: /standalone_integration_crits/crits_screenshot_3.jpeg

You will need to add this Source to the account that you using for API access. Select **CRITs Control Panel > Users**
from the Navigation Menu (the "gear" icon in the top left corner). Click the username you want to add the Source to.

.. image:: /standalone_integration_crits/crits_screenshot_4.jpeg

This will open the **Add/Edit User** window. in the Sources section either click **Add all** to add all Sources or add
the specific Source by click the **+** next to that Source.

.. image:: /standalone_integration_crits/crits_screenshot_5.jpeg

.. note:: You will also have to add this Source to any other user accounts you want to be able to view PhishMe
          Intelligence TLOs.

.. rst-class:: html-toggle

Sample config.ini
-----------------

config.ini example::

    [integration_crits]
    use = False
    ssl_verify = False
    host_with_protocol = https://your.crits.url.com
    user =
    api_token =
    source =

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
    * - integration_crits
      - use
      - A Boolean value to control whether the integration outputs to CRITs
      - True
    * - integration_crits
      - ssl_verify
      - A Boolean value to control whether the SSL certificate used for a connection to CRITs should be
        verified
      - True
    * - integration_crits
      - host_with_protocol
      - The destination hostname or IPv4 address (with protocol) of the CRITs instance
      - True
    * - integration_crits
      - user
      - Username of account used to create API Key for REST API access to CRITs
      - True
    * - integration_crits
      - api_key
      - API key to use for REST API access to CRITs
      - True
    * - integration_crits
      - source
      - Source to write PhishMe Intelligence data to in CRITs
      - True

.. rst-class:: html-toggle

Features
--------

List of Campaigns (You can click **Refresh Stats** to see numbers Campaign attributed TLOs in this view):

.. image:: /standalone_integration_crits/crits_features_1.jpeg

Specific Campaign:

.. image:: /standalone_integration_crits/crits_features_2.jpeg

List of Samples in Campaign:

.. image:: /standalone_integration_crits/crits_features_3.jpeg

List of Indicators in Campaign:

.. image:: /standalone_integration_crits/crits_features_4.jpeg

Specific Sample:

.. image:: /standalone_integration_crits/crits_features_5.jpeg

Specific Indicator:

.. image:: /standalone_integration_crits/crits_features_6.jpeg
