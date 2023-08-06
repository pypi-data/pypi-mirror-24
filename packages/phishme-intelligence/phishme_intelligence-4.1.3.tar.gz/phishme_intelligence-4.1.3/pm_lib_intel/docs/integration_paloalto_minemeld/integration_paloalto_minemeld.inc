.. _paloalto_minemeld:

=============================
Palo Alto Networks / MineMeld
=============================

.. image:: /integration_paloalto_minemeld/minemeld_logo.png
   :scale: 40%

.. rst-class:: html-toggle

Overview
--------

PhishMe® and Palo Alto Networks® have partnered to provide security teams with the ability to ingest human-verified
`phishing intelligence <http://phishme.com/product-services/phishing-intelligence/>`_ in a standard format that can then
be applied to custom PAN-OS security policies containing IPs, domains, and URLs. This integration is performed through a
VM appliance developed by Palo Alto Networks called MineMeld.

`MineMeld <https://live.paloaltonetworks.com/t5/MineMeld/ct-p/MineMeld>`_, by Palo Alto Networks, is an extensible
Threat Intelligence processing framework and the 'multi-tool' of threat indicator feeds. Based on an extremely flexible
engine, MineMeld can be used to collect, aggregate and filter indicators from a variety of sources and make them
available for consumption to peers or to the Palo Alto Networks security platforms.

.. rst-class:: html-toggle

Getting Started
---------------

Go to the Config menu and click the icon at the bottom right of the screen.

.. image:: /integration_paloalto_minemeld/minemeld_screenshot_1.jpeg

Search for 'phishme' and click the Miner in the results.

.. image:: /integration_paloalto_minemeld/minemeld_screenshot_2.jpeg

Click 'CLONE' to accept the default configuration or 'NEW' to modify the default configuration.

.. image:: /integration_paloalto_minemeld/minemeld_screenshot_3.jpeg

Replace the default name with a more friendly name (don't use spaces) and click OK.

.. image:: /integration_paloalto_minemeld/minemeld_screenshot_4.jpeg

Repeat this process of cloning new Miners to add Aggregator Nodes (search for 'Processor') and Output Nodes (search for
'output red value'). Each time you clone a new Miner, simply choose the upstream Miner in the Inputs field, as in the
example below. The Aggregator Nodes should have the PhishMe_Intelligence node selected as their input and the Output
Nodes should have their respective Aggregator Nodes selected according to the data type they process (domain, ipv4, url).

.. image:: /integration_paloalto_minemeld/minemeld_screenshot_5.jpeg

Once all necessary Nodes are added, return to the CONFIG page and click 'COMMIT' in the top left corner of the page.
Then, navigate to the Nodes page.

.. image:: /integration_paloalto_minemeld/minemeld_screenshot_6.jpeg

Click the newly created PhishMe_Intelligence Node. Notice the maroon exclamation point after the name indicated
additional configuration is needed.

.. image:: /integration_paloalto_minemeld/minemeld_screenshot_7.jpeg

Add your own API credentials generated from https://www.threathq.com/p42/settings/apitokens into the following fields.
The Miner will restart and activate, pulling new PhishMe Intelligence directly from the PhishMe API.

.. image:: /integration_paloalto_minemeld/minemeld_screenshot_8.jpeg

When completed, the Miners will look similar to the following example.

.. image:: /integration_paloalto_minemeld/minemeld_screenshot_9.jpeg

Each feed will be available by concatenating the protocol and hostname of your MineMeld instance, plus '/feeds/' plus
the name of your Output Node. In the above example, the first feed could be found at https://hostname/feeds/url_hc.
