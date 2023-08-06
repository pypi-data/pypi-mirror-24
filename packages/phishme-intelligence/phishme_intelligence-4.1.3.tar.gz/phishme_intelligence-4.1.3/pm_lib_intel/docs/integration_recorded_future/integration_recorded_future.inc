.. _recorded_future:

===============
Recorded Future
===============

.. image:: /integration_recorded_future/recorded_future_logo.png

.. rst-class:: html-toggle

Overview
--------

PhishMe Intelligence and Recorded Future provide analysts with the ability to effortlessly cross reference
between each solution to research indicators. An analyst investigating phishing activity within Recorded Future
can instantly cross-examine using PhishMe’s API against IPs, domains, or hashes. Analysts can quickly validate
their research in tandem with PhishMe’s human-verified intelligence and access contextual reports that provide
organizations insight into the criminal infrastructure. Likewise, the analyst can connect back into Recorded
Future to continue following the trail of bits from the open, dark, and deep web. Security teams gain time and
insight from the ability to seamlessly move between their intelligence sources.

.. rst-class:: html-toggle

Setting up Integration
----------------------

In the upper-right corner of the Recorded Future interface select your username and then select **Extensions**:

.. image:: /integration_recorded_future/recorded_future_setup_1.png

Select **Enable** under the PhishMe entry.

.. image:: /integration_recorded_future/recorded_future_setup_2.png

Enter the API username and password you have generated (`go here <https://www.threathq.com/p42/settings/apitokens>`_)
and click **OK**. You now can use the PhishMe Intelligence integration in Recorded Future.

.. image:: /integration_recorded_future/recorded_future_setup_3.png


.. rst-class:: html-toggle

Using Integration
-----------------

When searching for a specific indicator type in Recorded Future supported by the PhishMe Intelligence integration
(URL, Domain, IP Address, or MD5 Hash) there will be the option to show PhishMe Intelligence information related to
the indicator:

.. image:: /integration_recorded_future/recorded_future_using_1.png

Open the drop down to show what PhishMe Intelligence Threat IDs (if any) match the indicator being researched. If there
is at least one Threat ID that matches the indicator you will see the following:

.. image:: /integration_recorded_future/recorded_future_using_2.png

And if there are no matches you will see something like the following:

.. image:: /integration_recorded_future/recorded_future_using_3.png

The links in the matches will take you to the Threat ID in the PhishMe Intelligence portal where you can find more
indicators and information to continue research.


