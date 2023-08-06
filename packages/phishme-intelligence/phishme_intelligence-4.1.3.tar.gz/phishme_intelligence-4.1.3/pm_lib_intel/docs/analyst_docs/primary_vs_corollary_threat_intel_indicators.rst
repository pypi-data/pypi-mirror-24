Primary vs Corollary Threat Intelligence Indicators
---------------------------------------------------

This page seeks to discern the difference between primary and what PhishMe Intelligence refers to as corollary
indicators of compromise. Within each threat intelligence product produced by PhishMe, some of the indicators are clear,
or primary, indicators a compromise has occurred. Other pieces of the threat intelligence product can be used to verify
such a compromise, but do not, by themselves, indicate a compromise has occurred. Caution should be exercised with this
distinction, otherwise many cycles can be expended tracking down potential compromises based strictly on corollary
indicators.

*Corollary* indicators are by definition, less reliable. These are indicators that should only be used for alerting; we
recommend against active mitigation solely based on them in any device. An example would be correlating email subject
lines with incoming emails and triggering an alert if there's a match. Because email subject lines are arbitrary, a
malware campaign could use the subject line: "Hello". While it might seem suspicious, it would be prudent to avoid
rejecting the message simply because of its subject line without any type of additional confirmation.

The best usage of *corollary* indicators is in tools like SIEMs that allow wide scale correlation across security data.
These indicators observed across multiple events on your network would be a fairly good indicator of a compromise.
Included with a primary indicator, these should be a clear scenario to take action on.

Sender IP addresses are a *corollary* indicator requiring special mention. While the true sender IP is likely hidden
within the headers of an email message, it is remarkably difficult to determine which is the true sender IP. For this
reason, PhishMe Intelligence provides a list of potential sender IP addresses that we have identified within a malware
campaign. This allows customers to use correlations as an additional scoring mechanism for their own mail or as
additional confirmation that an incident under investigation is related to a specific email message. But these
indicators are probably the least valuable and most likely to lead to false positives if used alone. The ease of
spoofing an email origination IP and the likelihood of the sender IP being a dynamically allocated IP make it
significantly less reliable than even other corollary indicators. Its value lies largely in confirming/investigating a
scenario if seen with multiple other indicators.

**PhishMe Intelligence**

.. list-table::
    :widths:  50, 50
    :header-rows: 1

    * - Primary
      - Corollary
    * - :ref:`Malware Artifacts <executable_set>`
      - :ref:`Sender Domain <domain_set>`
    * - :ref:`Watch List <block_set>`
      - :ref:`Sender Domain(s) <domain_set>`
    * -
      - :ref:`Sender IP(s) <sender_ip_set>`
    * -
      - :ref:`Subject Line(s) <sender_subject_set>`
