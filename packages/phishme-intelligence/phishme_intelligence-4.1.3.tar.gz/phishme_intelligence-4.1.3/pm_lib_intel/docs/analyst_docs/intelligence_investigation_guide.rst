.. _intelligence_investigation_guide:

========================================
PhishMe Intelligence Investigation Guide
========================================

Starting Points
---------------

When beginning an investigation in the PhishMe Intelligence portal it is often helpful to consider the indicators you
are most likely to see. Three categories of common indicators are:

    * Email metadata
    * Filesystem artifacts
    * Network indicators

These three categories represent the most comprehensive methods by which malicious binaries evidence their presence.
However these categories present themselves at different times in the infection lifecycle and each can be used to
identify malware at different points within that lifecycle.

For example, the bulk of filesystem artifacts present themselves as evidence of the malware's presence after a machine
or environment has been affected. However, malware binaries attached to hostile spam emails are also represented in the
PhishMe Intelligence portal where allowing for speculative searching for matches to unknown email attachments is also
possible.

However, searching for spam email metadata within the PhishMe Intelligence portal also provides a strong resource for
both proactive and retroactive investigation. Characteristics of the email messages used to deliver malicious software
are collected in the PhishMe Intelligence portal and presented in a searchable manner allowing for users to match
malware behavior to email subject lines, sender domains, message origin IP addresses, and even the purported sender's
name.

Regarding network indicators, implementing and integrating the data available through the PhishMe API into your network
defense infrastructure is the best way to proactively take advantage of PhishMe Intelligence. However, in cases of
retroactive or speculative investigation, the PhishMe Intelligence portal provides insight into the infrastructure used
to support and propagate malware and its negative effects. Data collected by PhishMe's analysts from investigations
performed on live malware samples provides insight into locations from which malware is spread as well as the command
and control resources required by the malware to carry out its hostile activities.

The scenarios listed above provide examples of ways you might leverage these three overarching data categories to
perform investigations into the resources and behaviors associated with both the newest and most prominent malware
threats you and your organization face.

Tying it together
-----------------

When the time comes to collect the results of a malware investigation, one of the most valuable resources available
through the PhishMe Intelligence portal and the PhishMe API is the library of detailed reports--each associated with a
distinct threat ID. This library provides you with a description of the spam email used to deliver a malware sample as
well as a piece-by-piece description of each element in that malware's infection trajectory. This serves as a breakdown
of the most crucial data points needed to address a malware threat and is presented in a format meant to be accessible
and portable within your organization.

-------------------------

Scenario 1: A suspicious email
------------------------------

One of the richest portions of the data provided by the PhishMe Intelligence portal is the email metadata linking an
unwanted email message with a particular malware threat. If a suspicious email is delivered to a recipient within your
organization, you can select any almost any element among its metadata as a search key in the PhishMe Intelligence
portal. This includes not only the subject line and origin domain but also the "friendly" name of the sender and sender
IP address. If the message contains a URL, portions of this URL or the link in its entirety can be used as a search key.
The same is true for the names and hashes of attached files as these are included in the analysis of any hostile email
attachments.

For example, if an email with the subject line "Huntsman Way Water Line" is delivered to a user within your
organization. This email strikes you as suspicious for a number of reasons but mostly due to the .zip archive attachment
with a 12-character alphanumeric file name. You can search for the subject line substring "Huntsman Way" to find a
handful of results in the PhishMe Intelligence portal.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_1_1.jpeg

The first shows a subject line matching yours exactly while the rest show close matches that are not exact. The search
results reveal that this suspicious email belongs to a much larger set of spam emails delivering the Upatre malware as
an infection vector for the Dyre trojan.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_1_2.jpeg

Clicking on the Threat ID number will display the threat detail page. From here, it is possible to pivot in such a way
as to identify the malware binary and any other indicators of compromise that might be associated with this campaign.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_1_3.jpeg

Any of the indicator values displayed within this detail page can be clicked to find other related results. For example
the list of watchlist indicators associated with this campaign shows locations on the Web that can be considered hostile
due to their use by the Dyre trojan.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_1_4.jpeg

For example, clicking through on one these IP addresses reveals that IP address is connected to 31 other analyses of the
Dyre trojan revealing that the "Huntsman Way" email is not an isolated event but is instead connected to a much larger
web of malware behavior.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_1_5.jpeg

Scenario 2: An unknown binary
-----------------------------

When in the process of examining a machine known to be affected by malware, it is possible to search the PhishMe
Intelligence portal for data associated with that malware and its behavior based on the hash of an unknown binary. The
same is true for spam email attachments in many cases. For example, if a machine is identified as compromised and a file
named "erwtwgw.exe" is found on disk, the MD5 checksum of that file can be used to search for a related analysis within
the PhishMe Intelligence portal. Start by identifying the file's MD5.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_2_1.jpeg

Then search for this MD5 in the PhishMe Intelligence portal, selecting the "Malware Artifact" category for the most
precise search.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_2_2.jpeg

Results from this search show that the unknown binary "erwtwgw.exe" as identified by its MD5 is associated with a single
Threat ID. As is the case for every threat detail page in the PhishMe Intelligence portal, the detail page associated
with Threat ID 3362 contains the full set of indicators by which this campaign can be identified.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_2_3.jpeg

However, for more information on the behavior of this malware and a summation of the hazard it poses you may refer to
the human-readable component of PhishMe's reporting associated with this Threat ID. This document can be found within
the PhishMe Intelligence portal document library.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_2_4.jpeg

Scenario 3: Unexplained HTTP traffic
------------------------------------

Another way the PhishMe Intelligence portal can help in malware investigations is in helping to classify an unexplained
HTTP request found in request logs or any other means of tracking network communication. Telltale HTTP requests are
common in malware investigations and can be used to correlate suspicious network communication to a particular type of
malicious software.

Consider the situation in which an HTTP request is identified as having been made to the URL
hxxp://brushes[.]su/green[.]php. You can begin your investigation in the PhishMe Intelligence portal by simply searching
for this HTTP request URL.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_3_1.jpeg

The results from this search show that URL is strongly associated with the Andromeda botnet trojan. This trojan is known
to make callbacks to PHP applications running on command and control servers from which they might receive instructions
for downloading additional malware such as is shown in Threat ID 3033. In many cases, however, this malware is simply
meant to colonize machines for its botnet and will distribute instructions to those machines at a later date.

.. image:: /analyst_docs/intelligence_investigation_guide/scenario_3_2.jpeg


