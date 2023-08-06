.. _brand_intelligence_investigation_guide:

==============================================
Brand PhishMe Intelligence Investigation Guide
==============================================

Scenario 1: Cross-Brand Intelligence
------------------------------------

You have a message that contains a link to a suspicious site:

*hxxp://www.subalipack.com/media/tpc.php*

Using the PhishMe Intelligence portal , enter the exact domain name in double quotation marks into the Search > Domain
filter box as seen below:

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_1_1.jpeg

Your results will look something like the following:  (You can configure your columns using the Customize button.)

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_1_2.jpeg

Immediately you can see that, not only does the PhishMe Intelligence portal contain details of your suspicious URL, it
also contains details of threats targeting consumers of several brands.  These other threats were phishing websites
hosted on the same domain, on the same day.

You can change the columns of the Search summary results table to show other details instead, such as where the
**Reported URL** may have redirected to.  This would be shown as the **Phishing URL** in the PhishMe Intelligence
portal; sometimes the Phishing URL is slightly different from what was reported to PhishMe.  Below you can see some
Reported URLs and Phishing URLs side-by-side:

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_1_3.jpeg

n this case, most of the Reported URLs did not re-direct; however, the URL that was reported to PhishMe with respect to
the Regions Bank phishing attack was just a component of the attack, a PHP script that loaded what was likely the second
step of the attack, a page to collect the victim’s Secret Authentication Questions and Answers.  So, you can see above
that the path of the Phishing URL was slightly different from the Reported URL.

You may also want to view the **Action URLs** associated with these attacks.  The Action URL, sometimes called the
“post location,” is typically a PHP script on the same server that contains code directing the phishing server what to
do when the victim completes the form on the page.  For the Regions Bank phish, the Action URL was extracted from the
following snippet of phishing page source code::

    </head>
        <body>
            <form name="formMP" method="post" action="http://subalipack.com/regions.php" language="javascript"
            onsubmit="return VAM_ValOnSubmit();" id="formMP" autocomplete="off" onreset="if (window.setTimeout)
            window.setTimeout('VAM_OnReset(false);', 100);">
            <input name="VAM_Group" value="" type="hidden">

Navigation directly to the Action URL will often reveal a subsequent page to the phishing attack.  Other times it may
reveal what is known as the Exit URL.  Most phishing attacks will redirect the victim to the real login page for the
spoofed brand as a last step of the attack.  Below you can see the Phishing URLs side-by-side with the corresponding
Action URLs:

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_1_4.jpeg

When you click on the Threat ID hyperlink for one of the phish on this domain, you can see the screenshot of the page
that was deemed to be a phishing web page.  Click on the magnifying glass to expand and view the full screenshot.

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_1_5.jpeg

The next step in investigating this attack may involve looking up the Whois information on the domain that is hosting
all these attacks.  Just click on the small question mark next to the domain name to reveal the Whois details fetched by
PhishMe:

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_1_6.jpeg

From that information, you can see that the domain was registered in the year 2000; so, it’s not a new domain registered
for the purpose of phishing.  Rather, it is a domain that has been compromised.  When you scroll down through the Whois
information, you will see that the domain was registered with Tucows through a reseller called Exabytes.   You can reach
out to the registrant via email at *tsnsdnbhd@yahoo.com* to notify them that the domain has been compromised and request
that they work with you to provide log files showing the IP addresses that first created the phishing subdirectories and
placed the phishing content files on the server.  Furthermore, you will want to ask the webmaster whether there is a
phishing kit that may have been left behind on the server.  Phishing kits often contain the email addresses of the
phisher.

If you are able to recover a phishing kit and email addresses, you can seek to have those addresses de-activated with
that evidence.  This will cause temporary disruption in the phisher’s business plans.  Alternatively, you can check in
the PhishMe Intelligence portal to see whether an email address is associated with other phishing attacks.  You may want
to work with law enforcement to get a search warrant issued to reveal the contents of the email account.

Scenario 2: Identify New Phisher Email Addresses
------------------------------------------------

If your company has a current policy not to investigate drop email addresses but rather to seek to get them de-activated
as quickly as possible, then you will want to use the PhishMe Intelligence portal to filter the threats for
recently-identified drop email addresses.  You can use the Search page to filter among the most recent phishing attacks
spoofing your brand where a kit was retrieved from the phishing server:

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_2_1.jpeg

Once you have your results set, Customize your view by removing columns from your previous searches and adding columns
that are relevant to this set of results, such as the First Seen date and the Drop Mail addresses:

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_2_2.jpeg

Let’s look at the kit associated with the second threat in the list, a phish recorded on *cyberkoncepts.com*.  Start by
clicking on the Threat ID number to bring up the threat detail page.  There you will find details of the phishing kit at
the bottom of the page.  Click on the Download icon to download a copy of the kit so that you can verify the location of
the addresses within the kit.

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_2_3.jpeg

All Fetched Kits and sets of Web Component files available on the PhishMe Intelligence portal are password-protected so
that your enterprise network settings will allow you to download a zip folder; however, you will want to handle these
zips carefully, preferably in a virtual machine environment, because the kits will sometimes contain executable scripts.

Once you have downloaded and up-zipped the archive, navigate to one of the locations in the image above for the email
address C0o5@yahoo.com, such as the file *login.php*:

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_2_4.jpeg

By viewing the source code of that file, you can see that the address C0o5@yahoo.com is listed in the comments only and
that the address mr.mugger90@gmail.com is receiving the stolen credentials.  You can also see that the message built by
this code also gets stored in a file on the phishing server named *logins.txt*.  You will want to go quickly to that
location on the phishing server to recover stolen credentials and notify your affected customers.

Going back to the PhishMe Intelligence portal, click on the drop address to reveal other phishing attacks associated
with that email address.  Configure your results summary table to show the Kit MD5 hash value so that you can see that
there are two other kits that the address mr.mugger90@gmail.com was extracted from:

.. image:: /analyst_docs/brand_intelligence_investigation_guide/scenario_2_5.jpeg

Add the Brands column to reveal that the other phishing servers from which these kits were archived were locations for
PayPal phish. You can use a free online mail server query tool to see that the address is still valid::

    MX record about gmail.com exists.
    Connection succeeded to alt3.gmail-smtp-in.l.google.com SMTP.
    220 mx.google.com ESMTP xb4si11105307wjc.178 - gsmtp

    > HELO verify-email.org
    250 mx.google.com at your service

    > MAIL FROM: <check@verify-email.org>
    =250 2.1.0 OK xb4si11105307wjc.178 - gsmtp

    > RCPT TO: <mr.mugger90@gmail.com>
    =250 2.1.5 OK xb4si11105307wjc.178 - gsmtp

Use Gmail Search to learn that the address is affiliated with the Google Plus profile for “mohamed amer” at the URL
hxxps://plus.google.com/103851713747879687315

The profile links to his YouTube channel at hxxps://www.youtube.com/channel/UCo7TUy2qDWrKd300GPJfF4Q where he has posted
videos and subscribed to channels about hacking over the past eight months.  The About tab on the YouTube profile
indicates that he has “Joined February 1, 2014”.