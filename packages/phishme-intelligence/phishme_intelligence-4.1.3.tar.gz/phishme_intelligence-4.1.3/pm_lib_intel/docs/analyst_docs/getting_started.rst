.. _getting_started:

===============
Getting Started
===============

Chapter 1: PhishMe Intelligence Portal at a Glance
--------------------------------------------------

PhishMe Intelligence Portal Overview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The PhishMe Intelligence portal is a web-based portal providing a complete archival history of the phishing attacks
against your brand and others and of PhishMe’s analysis of malware distributed by large spam campaigns.

Please contact support@phishme.com with your comments or questions.

What You Need
^^^^^^^^^^^^^

You can use any modern web browser, such as Internet Explorer, Chrome, Firefox, or Safari, to access the portal.
However, some types of web browsers could cause some functionality to be limited or even non-existent.  A partial list
of browsers supported follows:

    * Microsoft Internet Explorer 9.0+
    * Google Chrome 8.0+
    * Safari on Mac 5.0+
    * Mozilla Firefox 6.0+
    * Opera 10.0+

.. note:: When Internet Explorer 11 is configured using the "High" security setting, several web functionalities which
          are required for the proper operation of the portal are disabled by default. These features are enabled and
          the application should work normally on both the "Medium" and "Medium High" security settings.  If using the
          "Medium-High" security setting is not an option–e.g. due to corporate security policy, you can use the "High"
          security setting and manually adjust the security settings so that the following parameters are enabled:
          *Download -> File Download = Enabled*, *Download -> Font Download = Enabled*,
          *Scripting -> Active Scripting = Enabled*, * *Miscellaneous -> Allow META REFRESH = Enabled*
          and *Miscellaneous -> Userdata Persistence = Enabled*

The portal provides an optimal viewing experience – easy reading, editing, researching, and navigation with a minimum of
resizing, panning, and scrolling – across a wide range of devices, including desktop computer monitors, smart mobile
phones, and tablets. Please note that cookies must be enabled for the site to function properly.

Chapter 2: Getting Started
--------------------------

Logging in to PhishMe Intelligence Portal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The PhishMe Intelligence portal uses a permission-based access control approach, restricting access and actions to
certain Users and User groups. In both scenarios, you will be prompted to log in to the PhishMe Intelligence portal.

The Sign In panel is shown below.

.. image:: /analyst_docs/getting_started/chapter_2_1.jpeg

Provide your Email Address and Password and click the Sign In button.  If your credentials are correct, the dashboard
will be displayed.  Passwords must contain at least eight characters and include at least one uppercase letter, at least
one lowercase letter, and at least one punctuation symbol.

.. image:: /analyst_docs/getting_started/chapter_2_2.jpeg

Forgot your Password
^^^^^^^^^^^^^^^^^^^^

In case you cannot remember your password, click on the “Forgot password?” found on the Sign In page.

The Forgot Password panel is shown below.

.. image:: /analyst_docs/getting_started/chapter_2_3.jpeg

Provide your Email address and click the Submit button.  An email message providing detailed instructions will be
immediately sent to you.  Your new password must contain at least eight characters and include at least one uppercase
letter, at least one lowercase letter, and at least one punctuation symbol.

If you have forgotten the email address specified in your User profile, you will need to contact your Company
Administrator for help.  In the event that you cannot determine or recall your Company Administrator, please contact
support@phishme.com.

Exploring the Workspace
^^^^^^^^^^^^^^^^^^^^^^^

The Dashboard is the first page you see once you sign in to the PhishMe Intelligence portal.

The User Interface of the application consists of:

    * Navigation Bar: Use the Navigation Bar on the left side of your screen to navigate between the segments of the
      application.
    * Main Panel: This is the area where you can find all the related information you are looking for.  Use this area to
      search and discover threats, set up Groups for the Brands you care the most about, manage your profile, and create
      Users for your account.

The following is a typical User Interface as seen using a browser on a desktop computer.

.. image:: /analyst_docs/getting_started/chapter_2_4.jpeg

Using ThreatHQ on a Mobile or Tablet Device
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use your mobile device, such as an iPhone or an Android phone, or Tablet—such as an iPad or a Galaxy, and an
optimized version of the product will be displaced.  The PhishMe Intelligence portal chooses the mobile, tablet, or
desktop interface based on your device.  The PhishMe Intelligence portal is viewed on a mobile or tablet device via a
web interface (optimized for mobile or tablet devices), not an app.  Type the URL for the PhishMe Intelligence portal
using your mobile browser to bring up the mobile interface.

The following is a typical User Interface as seen using a mobile phone.

.. image:: /analyst_docs/getting_started/chapter_2_5.jpeg

Click on the

.. image:: /analyst_docs/getting_started/chapter_2_6.png

icon on top left area of your screen to display the Navigation Bar.

Navigation Bar Items
^^^^^^^^^^^^^^^^^^^^

.. image:: /analyst_docs/getting_started/chapter_2_7.jpeg

User Roles
^^^^^^^^^^

ThreatHQ® supports two types of User roles; the “Users” and “Company Administrators”.  Each user is given specific user
access rights. Both “Users” and “Company Administrators” can:

    * View and personalize dashboard data
    * Perform searches and save search criteria for future use
    * Create and use Groups of Brands
    * View library documents
    * Update own settings

Furthermore, “Company Administrators” can create/invite new “Users” within their organization.

Chapter 3: Dashboard
--------------------

.. image:: /analyst_docs/getting_started/chapter_3_1.jpeg

Dashboard Overview
^^^^^^^^^^^^^^^^^^

Use your dashboard to get quick information about recent PhishMe Intelligence threats.

Latest Threats
^^^^^^^^^^^^^^

The top of the Dashboard shows two tables–Top Malware Families (Last 10 Days) and Latest Reports.

.. image:: /analyst_docs/getting_started/chapter_3_2.jpeg

The Top Malware Families table presents a quick-reference list of the ten most-frequently-analyzed types of malware,
including droppers and payloads, over the past ten days.  Clicking a malware variety performs a filter and Search (see
:ref:`Chapter 4 <getting_started_ch4>`) for all threats related to that variety.

The Latest Reports table presents an easy-access list of the ten most-recently-published Active Threat Reports, with
links to the corresponding Malware Threat Detail Pages and Active Threat Reports in HTML and PDF formats for download.

Find Threats
^^^^^^^^^^^^

The bottom of the Dashboard allows PhishMe Intelligence customers to search for indicators of compromise.  Just enter a
search term in the appropriate field to quickly navigate to the threat details and Active Threat Reports for related
malware.  The fields include Domain, IP Address, URL, MD5, Filename, Phishing Subject, Malware Description, and
Language.

By default, recent malware threats will be listed in your Dashboard.  First-time users will see the columns Threat ID,
Type, Malware Description, and First Seen. Use the Search boxes to filter those results, and use the Customize button to
configure the columns presented in your results table.  Following is a screenshot of a results table showing recent
malware campaigns, the spoofed Brands, the Malware Subject lines, the Malware Description (family) and the First Seen
date:

.. image:: /analyst_docs/getting_started/chapter_3_3.jpeg

.. _getting_started_ch4:

Chapter 4: Search
-----------------

.. image:: /analyst_docs/getting_started/chapter_4_1.jpeg

Search Overview
^^^^^^^^^^^^^^^

The PhishMe Intelligence portal provides powerful search capabilities.  You can search for Brands, specific threats,
URLs, Domains, and a wide range of other fields.  Search criteria can be saved and can be used again in the future.
The PhishMe Intelligence portal search allows you to:

    * Save and reuse search filters
    * Export search results
    * Sort search results
    * Review detailed threat information
    * Discover information about related threats

From the Navigation bar, click on the magnifying glass symbol to reach the Search page, where there are tabs for
Advanced Search and Saved (searches), as seen below:

.. image:: /analyst_docs/getting_started/chapter_4_2.jpeg

Advanced Search
^^^^^^^^^^^^^^^

Use Advanced Search to discover precise threat results. You can use one or more of the available fields.  Multiple terms
within one category are joined using OR operators.  Entering terms into multiple categories will cause them to be joined
using AND operators.

After viewing your results, you may display the search fields again by clicking the two-directional arrow seen at the
bottom of the screenshot below.

.. image:: /analyst_docs/getting_started/chapter_4_3.jpeg

The table below identifies the capabilities of each Advanced Search Field.  Each Field on the Advanced Search page
allows you to search for threats based on different data types. Searching without quotation marks will yield the
broadest range of results. **Exact Search** means that you only want to see results where the values in that data type
exactly match your search term.

**Search Example 1**

If you want to view all threats involving the exact Domain name baddomain.com, then search for that term in quotation
marks, like this:

    "baddomain.com"

However, if you would also like to view threats involving any Domain name that includes that term, such as threats on
*notsobaddomain.com*, *prettybaddomain.com*, and *verybaddomain.com*, then you should enter that term without quotation
marks, like this:

    baddomain.com

If you would like to view all threats on the host name *maybe.notsobaddomain.com* but not **every** thing on
*notsobaddomain.com*, then you would need to enter that term into the **URL** Search Field, as it is not simply a Domain
but a host name that includes a subdomain name.  Since it's not a complete URL (with protocol, for example), then you
should not use quotation marks when you enter it into the URL Search Field.

**Search Example 2**

The Extracted String Search Field does not contain data of only a certain type; rather, it contains phrases pulled from
the configurations of machines infected with malware.  Therefore, you cannot know the range of exact phrases that may be
included there.  So, when searching among Extracted Strings, it is best not to use quotation marks.

**Search Example 3**

Everything that you enter will be treated as part of what you are looking for, as long as it is within the Property
characteristic of the data type that the Field represents.  This means that you can search among Action URLs for
*loginexpress.phpp* and possibly get no results because there is an extra character on the end of your term.  But it
also means that you can search among URLs for */mybank/mybank/mybank/* and view only the threats where that exact path
was exhibited in the URL.

As with all the Fields that offer Sub string Search, if you enter phrases with special characters, the special
characters will be treated as literals.  Searching with regular expressions (or, wildcards) is not supported.

.. list-table::
    :widths:  10, 10, 24, 24, 22, 10
    :header-rows: 1

    * - Field
      - Property
      - Exact Search (case sensitive)
      - Exact Search (case insensitive)
      - Sub string Search (case insensitive)
      - Range search
    * - Threat ID
      - Numeric
      - Yes
      - No
      - No
      - No
    * - Drop Mail
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - Extracted String
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - ASN
      - Numeric
      - Yes
      - No
      - No
      - No
    * - ASN Organization
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - ASN Country Code
      - String - Valid country code in the form XX
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - Malware Subject
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - Malware Sender Name
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - Malware Description
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - Phishing Page Title Attribute
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - IP Address
      - IP Address
      - Yes
      - No
      - No
      - Yes (CIDR)**
    * - Threat Language
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - URL
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - Domain
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - MD5
      - Hexadecimal
      - No
      - Yes
      - No
      - No
    * - Filename
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No
    * - Malware System Changes
      - String
      - Yes (requires quotes)
      - No
      - Yes
      - No

Advanced Search allows you to search for sub strings that may contain special characters.  For example, you can search
for certain URL patterns, including slashes, and retrieve only the URLs that exhibit that exact sub string.

The fields First Seen, Last Date, and Has Kit fields provide a drop-down menu of static choices.  The Reset button
clears all Search fields.

\*\*: The IP Address filter box supports searches on net blocks entered in **CIDR format**.  For example, you can enter
the net block for some of the IP addresses recorded in malware analysis recently:  188.165.0.0/16.  This block belongs
to OVH France, and the portal links the IP addresses in that net block to over two thousand threats, including IP
addresses that the Dyre malware communicates with to receive configuration updates (new instructions of what to do to
the infected machine and with stolen data) and to check in with its command and control.

**Autocomplete Feature**

As you type the name of the Brand or Group you want to search for, The PhishMe Intelligence portal will recognize the
context and offer a list of suggestions.

    1. Click in the Brands field
    2. Start typing the name of a Brand or Group (if you have previously created one)
    3. The portal recognizes the context and offers a list of suggestions
    4. Select the one that you want
    5. Repeat steps 2-4 as many times as you like

**Customized Fields**

Certain fields of Advanced Search can be customized. You can add multiple instances of specific fields by clicking their
“+” (plus) icon as shown below.

.. image:: /analyst_docs/getting_started/chapter_4_4.jpeg

Click the “Remove Field” link to remove unneeded extra fields.

Each instance can be further customized by selecting the **type** of information you want to use. Simply click the field
to toggle it on or off.

In the Filename field, Kit Filename and File refer to Phish threats, and Malware Filename refers to Malware threats.

The URL Types Threat, Reported, and Action refer to Phish threats, and Malware Watch List refers to Malware threats.

In the IP Address field, you can select Threat for the IP address of a phishing page, or you can select Malware Sender
or Malware Watch List when investigating Malware threats.

The MD5 field allows you to focus on the hash values for phishing Kits, phishing page Files (web components), and/or
Malware Artifacts.

The Domain field can be customized to show the domains of phishing pages by selecting “Threat”.  The Domain Types
“Reported” and “Action” also refer to credential phishing threats.  Choose “Malware” to limit your Domain search to
include only Watch List domains and spam sender email address domains identified in PhishMe’s analysis of malicious spam
campaigns.  Choose Watch list to limit your results to domain names enumerated in Watch Lists for malicious spam
campaigns.  Choose Sender to limit your results to spam sender email address domains.  If you select none of these
options, the default behavior is to return All Types.

.. image:: /analyst_docs/getting_started/chapter_4_5.jpeg

Search Results
^^^^^^^^^^^^^^

The results of your search are presented as a table.  The PhishMe Intelligence portal initially displays up to the first
ten threats in the results panel.

If the information you're looking for is not on the current page of search results, you can use the paging navigation at
the bottom of the page to see more results.  You can also view ten more results in the same page by clicking the [+10]
at the bottom-right of the table.

Click on the header of each column to sort results based on your preferences (view “Multiple Field Sorting” section
below for more information).

.. image:: /analyst_docs/getting_started/chapter_4_6.jpeg

**Back Button**

You can use your browser's back button to return to previous search results after pivoting and performing subsequent
searches.

**Search Results View Customization**

You can customize the way you view the listing of your searches by adding or removing columns from the table of results.

    1. Click on the Customize link.
    2. Click in the field that just appeared.
    3. Start typing the name of the column you would like to add to the table, or simply scroll up and down the
       available list.
    4. Select the name of the column.
    5. Column immediately appears in your table of results.

Just click on the “x” button next to each selected column to remove it from your table of results.

Once you have arranged your search results summary table into a configuration that you prefer, you can save that
configuration by clicking on Manage Columns to name and save the view you have configured.  Then you can click on Manage
Columns again later to restore a saved view. You may want to save one view for Phishing threats and another view for
Malware threats. Your Phishing view may contain, for example, threats ordered by Last Date with the Reported URL,
Phishing URL, and Action URL displayed. For viewing recent Malware threats, you may want to set up your summary results
table to display the Malware Subject and Malware Description, ordered by First Seen date.

Note that the Id column name is short for Threat ID and cannot be removed from the table. The Type column will show one
of two values, either Phish or Malware. Brands refers to brand names or themes noted in both types of threats.

First Seen and Last Date are also relevant to both Phish and Malware threats.  With respect to credential phishing URLs,
PhishMe records a new Threat ID for each distinct URL reported to us; the First Seen date/time and the initial Last Date
represent when a suspicious credential phishing URL was reported to PhishMe.  If the same URL is reported to PhishMe
again, the Last Date is updated.  Malware threats are given a First Seen date and time according to the publication of
the analysis data related to the corresponding malicious spam campaign.  If additional information is added to the
analysis file, the Last Date may be updated.

The columns Action URL, ASN, ASN Country Code, ASN Organization, File Count, Has Kit, Kit MD5, Phishing Domain, Phishing
Host, Phishing IP, Phishing URL, and Reported URL all correspond to data points related to credential phishing web
sites.

.. image:: /analyst_docs/getting_started/chapter_4_7.jpeg

**Multiple Field Sorting**

You can use more than just one field to sort your search results.

    1. Click on the Customize link
    2. Drag and drop the field(s) from the list of fields you have selected for display that you would like to use in
       the “Sort by” area
    3. Use the arrows next to the column names (“Sort by” area) to sort the search results

For example, you can use Advanced Search to view all threats related to the IRS within the past year. If you then want
to view the Phish results at the top of the results table, toggle the arrow next to the Type column. To further sort
the Phish according to Last Date, make sure Last Date is one of your columns, then drag the column name tile from the
Customize area to the Sort by area. You can then toggle the arrow next to that tile in the Sort by area to sort on Last
Date.

.. image:: /analyst_docs/getting_started/chapter_4_8.jpeg

As another example of Multiple Field Sorting, you may want to view the malicious spam campaigns that spoofed Amazon,
sorted by First Seen date. Use Advanced Search to select the Amazon brand and click Search. Once your results table is
displayed, add the Type and First Seen columns. Then sort by Type by clicking the arrow next to the column header. To
further sort by First Seen, drag the First Seen column name tile from the Customize area to the Sort by area. Then
toggle the arrow next to that tile to display the Amazon Malware threats by First Seen date descending.

.. image:: /analyst_docs/getting_started/chapter_4_9.jpeg

**Save Search Criteria**

Search criteria can be saved and can be used again in the future.

In the results panel:

    1. Click the Save link found in upper right corner.
    2. Type the title of your search.
    3. Click the Save button.

In the example shown below, Advanced Search was used to filter All Data for threats hosted on the ASN 16276 (OVH) within
the past month.  That search can be saved with an intuitive name for later use.

.. image:: /analyst_docs/getting_started/chapter_4_10.jpeg

**Export a Search**

You can export search results in CSV format.

In the results panel:

    1. Click the Export link found in upper right corner
    2. Select to view the document online or download it to your device

.. image:: /analyst_docs/getting_started/chapter_4_11.jpeg

Load Saved Search
^^^^^^^^^^^^^^^^^

To run a saved search:

    1. Choose Saved tab.
    2. Locate the search you want to run.
    3. Click the Title to run the search.

.. image:: /analyst_docs/getting_started/chapter_4_12.jpeg

The PhishMe Intelligence portal will automatically run the search for you and present you with a list of updated
results. The search will be run against the criteria you specified when you saved it.

**Edit a Saved Search**

The PhishMe Intelligence portal allows you to edit the title of your saved search.

    1. Locate the search you want to edit
    2. Click the “Pencil” (edit) icon
    3. Modify the Title
    4. Click the Save button

**Remove a Saved Search**

    1. Locate the search you want to delete
    2. Click the “X” (delete) icon

Threat Detail View
^^^^^^^^^^^^^^^^^^

While in your search results panel, click the Threat ID of the threat you are interested to discover more information
about.  The Threat Detail panel opens.

You may also navigate to a Threat Detail panel using a URL pattern. For Phishing threats, use the following URL pattern
in your browser:

https://threathq.com/p42/search/default?phish=[Threat_ID]

For Malware threats, use the following URL pattern in your browser:

https://threathq.com/p42/search/default?malware=[Threat_ID]

Below is a partial screenshot of a PhishMe Brand Intelligence threat detail page:

.. image:: /analyst_docs/getting_started/chapter_4_13.jpeg

Click the magnifying glass in the gray area to expand your view of the screenshot of a phishing page; clicking on the
image again collapses it.

Just under the First Seen time stamp, you will notice one or more Feeds listed.  When the Reported URL for a phish is
sourced from you, your company will be listed.  Otherwise, a public feed such as “APWG” will be shown, or the word
“ThreatHQ” will be shown.

Under the Feeds is the HTML Title attribute of the phishing page, if any, labeled as Page Title.  The title attribute of
a phishing page can be a quick indicator of the language of the page and can, if fairly specific, be used with the
Google Search intitle operator to identify additional, live phish of the same style.

You can expand your investigation further by clicking the available links in the page to find correlations on those data
points among other threats.

You may also download Phishing Kits or the files fetched for the phishing page ("Web Components") to your device.
**Remember that these collections of files may contain malicious content.**  All of the downloadable files are in Zip
folders with the password THREATHQ in all caps.

When .ZIP folders are identified on phishing servers, PhishMe stores those files and extracts any email addresses
observed in those files.  The email addresses are listed at the bottom of Threat Detail pages in the Fetched Kits
section, as seen in the example below, alongside the path within the phishing kit from which the addresses were
extracted.  If an email address was obfuscated and yet still identified, the method of obfuscation is noted.  PhishMe
threat intelligence analysts may also manually review kits and apply a function to the various observed email addresses
such as Drop, From, Inactive Drop, or Other.

.. image:: /analyst_docs/getting_started/chapter_4_14.jpeg

Below is a partial screenshot of a PhishMe Intelligence threat detail page:

.. image:: /analyst_docs/getting_started/chapter_4_15.jpeg

PhishMe Intelligence threat detail pages show the title of the associated Active Threat Report, the names of any spoofed
brands—or if no specific brand was spoofed, then “Generic Malware Threat”, time stamps of when the threat analysis was
published and updated by PhishMe, the Subject lines of the related messages, the Sender Domain(s) of the sending
addresses of the messages, the full Sender Email addresses, the apparent Sender IP addresses, the Sender Name(s), a
Description of the associated malware, Malware Artifacts and their hash values, Watch List items (IP addresses, domains,
or URLs), Spammed URLs, and Extracted Strings.  Just under the Threat ID, you can click to download an HTML or PDF
version of the related Active Threat Report.

The malware Description imparts a general depiction of the spam campaign and typically includes a family name related to
the malware encountered.  As an example, the Description for malware Threat ID 2994 is "Upatre, Dyre".   You can search
the malware Description and see the results in a column in your search results summary table.  This allows you to, for
example, search on the term Cryptowall to discover all the detail pages for malicious spam campaigns that delivered this
malware family as early as 2014-07-15.

For malware samples that have no generally-accepted name in the security community, PhishMe provides specific numeric
labels with the prefix "QC Group", to reflect that the malware exhibits specific characteristics that will enable future
qualitative clustering analysis.  When a meaningful label for malware belonging to a qualitative cluster is identified,
that name will be applied to all malware of that variety. This allows for the tracking of malware varieties and their
associated indicators using the "QC Group" alias, thereby simplifying the investigation of esoteric malware varieties.

The Sender Email addresses are extracted from spam message headers and can sometimes be used toward attribution;
however, sometimes they represent compromised accounts.

Malware Sender Name refers to the display name of the spam message sender.  You can search among these Sender Names to
find the name that the spammer intended to be prominently displayed to the recipient.  Being able to reference the
display name of malicious spam messages is becoming more important as mobile users are increasingly targeted; many
mobile mail clients show the display name only, by default.  Also, as more companies enable DMARC and reduce the number
of phishing messages that are delivered when their legitimate domain is spoofed, spammers will likely be more prone to
configure the display name of the sending email account so that it reflects the spoofed brand.

Watch List items are assigned an Impact level by PhishMe Threat Intelligence Analysts, and that level can be None,
Minor, Moderate, or Major.  Watch List IP addresses are listed with an ASN, autonomous system Organization, and Country
Code, as seen below, making it very clear who controls the assets involved in malicious activity.

.. image:: /analyst_docs/getting_started/chapter_4_16.jpeg

Extracted Strings represents the text strings extracted from the memory of the malware analysis machine.

Some of the detail lists can grow large and are shown in paginated sets of ten.  For easier viewing and data
manipulation, you can click [All] at the bottom right of a list section if you would prefer to view all list items at
once.  This feature also allows investigators and analysts to copy/paste items into other media.

You can return to the search results by clicking the Return link in the upper left corner of the Threat Detail panel.

Chapter 5: Group of Brands
--------------------------

.. image:: /analyst_docs/getting_started/chapter_5_1.jpeg

Groups of Brands Overview
^^^^^^^^^^^^^^^^^^^^^^^^^

A Group of Brands is a convenient way to manage a collection of Brands of specific interest to you. You can use one or
more Groups in your searches throughout the PhishMe Intelligence portal and your Dashboard.

You can build as many Groups as you like, and one Brand can belong to many Groups.

Groups of Brands are personal and cannot be shared among Users of the same Company.

To reach the page for creating and managing Groups of Brands, click on the star symbol in the Navigation Bar.

Manage Groups
^^^^^^^^^^^^^

The PhishMe Intelligence portal comes with no Groups defined; you have the option to create your own Groups.

.. image:: /analyst_docs/getting_started/chapter_5_2.jpeg

**Add a Group**

Click on the “Add New Group” link found at the bottom of the page, and the Brand Group panel opens.

    1. Click the Group Name field
    2. Type its name (example: Banks)
    3. Click the Select Brands field
    4. Start typing the name of a Brand
    5. ThreatHQ® predicts the Brand or Group you want to type and presents you with options
    6. Select the one you are looking for
    7. Repeat steps 4-6 as many times as you like
    8. Click the Save button to create the Group

.. image:: /analyst_docs/getting_started/chapter_5_3.jpeg

The Group you just added is listed in the Brands panel, and it’s ready to be used in your searches and your dashboard.

Your Group will show first when you type the name of a Brand within that Group into search fields.

**Delete a Group**

You can delete a Group anytime, even if that Group is used in existing searches or your dashboard.

    1. Locate the Group in your listing
    2. Click the “X” icon (delete) under the last column of your listing

Your deleted Group will be removed from your dashboard and from your saved searches.

Once you delete a Group, you can re-create it using the same name and individual Brands, but it will not re-populate in
the previously-related saved search.

.. image:: /analyst_docs/getting_started/chapter_5_4.jpeg

**Edit a Group**

You can edit a Group anytime, even if that Group is used in existing searches or your dashboard.

    1. Locate the Group in your listing
    2. Click the “Pencil” icon (edit) under the last column of your listing, and the Brand Group panel opens
    3. You can modify the Name of your Group
    4. You can modify the Brands of your Group
    5. Click the Save button to update the Group

Group updates are propagated across ThreatHQ® where that Group is being used (dashboard and saved searches).

Chapter 6: Library
------------------

.. image:: /analyst_docs/getting_started/chapter_6_1.jpeg

Library Overview
^^^^^^^^^^^^^^^^

To reach the Library, click on the folder symbol in the Navigation Bar.

From time to time, PhishMe may share information with you in the form of files that you can download from the Library.
Those files may be public—available to all accounts and Users of the PhishMe Intelligence portal , or private—available
only to the Users of selected organizations.  Public Documents are available in the PUBLIC DOCUMENTS tab on the Library
page.  Documents available only to your organization are available in the tab labeled as YOUR_ORGANIZATION_NAME
DOCUMENTS.  Organizations that subscribe to PhishMe Intelligence have the ability to see all malicious spam campaign
reports under a tab labeled ACTIVE THREAT REPORTS.  All of the columns on all of the tabs can be sorted in ascending or
descending order by clicking the column heading to toggle the sort direction.

View Library Files
^^^^^^^^^^^^^^^^^^

The list of all available PUBLIC DOCUMENTS is shown upon visiting the Library.

.. image:: /analyst_docs/getting_started/chapter_6_2.jpeg

To view a document,

    1. Locate the file you are interested in viewing
    2. Click on the Document Title
    3. Select to view the document with applicable software or to download it to your device

Documents that are private to your organization are available in the next tab.  Their visibility to certain
organizations is controlled by PhishMe portal administrators.

The ACTIVE THREAT REPORTS tab provides a list of links to HTML documents with analyses of malicious spam campaigns.  The
page also includes links to the associated PhishMe Intelligence detail pages, under View Threat Details.

.. image:: /analyst_docs/getting_started/chapter_6_3.jpeg

Clicking on the THREATHQ DOCUMENTATION tab takes you directly to the URL

https://www.threathq.com/documentation

Chapter 7: Provide Feedback
---------------------------

.. image:: /analyst_docs/getting_started/chapter_7_1.jpeg

Submit Phish
^^^^^^^^^^^^

Click the bullhorn icon in the Navigation Bar to bring up a window in which you can submit suspicious URLs to PhishMe
for processing as part of the PhishMe Brand Intelligence product.  Just type or paste in line-separated URLs in the
noted format and click Submit.  You will receive a confirmation message on the screen when your URLs have been
delivered.

.. image:: /analyst_docs/getting_started/chapter_7_2.jpeg

Contact Us
^^^^^^^^^^

Another tab in the Provide Feedback section is labeled Contact Us.  Click there to submit comments or suggestions about
the PhishMe Intelligence portal.

.. image:: /analyst_docs/getting_started/chapter_7_3.jpeg

Chapter 8: Settings
-------------------

.. image:: /analyst_docs/getting_started/chapter_8_1.png

Settings Overview
^^^^^^^^^^^^^^^^^

Use your Settings to specify your PhishMe Intelligence portal basic settings. If you are the Company Administrator for
your organization, you are able to manage the Users in your organization.

To reach the Settings page, click on the gear symbol in the Navigation bar.

Manage Your Profile
^^^^^^^^^^^^^^^^^^^

The Profile tab is selected by default when you visit the Settings page.

You can modify your first and last name and update your phone number and time zone if you wish.

Currently, you cannot update your Organization’s name or your email address. Please contact your Company Administrator
if you need help regarding those two fields.

Manage Your Security
^^^^^^^^^^^^^^^^^^^^

Click the Security tab, and the form to update your password will open.

    1. Type your old password in the Old Password field
    2. Type your new password in the New Password and Retype New Password fields
    3. Click the Save button

Your new password must be at least 8 characters or more and must include at least one upper case letter, one lower case,
and one number or special character.

Manage Your Preferences
^^^^^^^^^^^^^^^^^^^^^^^

Click the Preferences tab, and the form to modify specific preferences opens.  The toggle buttons provide the capability
for you to manage when you receive certain email messages from PhishMe.  As of May 8, 2017, such messages are mailed
from "The PhishMe Team <support@phishme.com>".

Click on the red or green portion of the button to toggle the selection.  For example, click on the red portion of the
toggle icon next to “Reports uploaded to the Library” to move the button to green and receive an email message whenever
a document is available for download from the PhishMe Intelligence portal library.  Such documents may be "Public" and
available to all PhishMe Intelligence portal users, or they may be specific to your company or organization.

To select **not to** receive an email message whenever there is a Report uploaded to the Library, click on the green
portion of the button to make it switch to red.

.. image:: /analyst_docs/getting_started/chapter_8_2.jpeg

All PhishMe Intelligence portal users may also set whether they would like to receive email messages containing
notifications regarding updates to the PhishMe System, such as our bi-weekly release notes.

Those users who subscribe to PhishMe Intelligence may also use the Preferences page to select whether they would like to
receive email messages containing each Active Threat Report as a PDF or HTML attachment, a daily digest containing links
to Active Threat Reports on the PhishMe Intelligence portal , and/or email messages with PhishMe's weekly Strategic
Analysis Report attached as a PDF or an HTML file.

Manage Your Users
^^^^^^^^^^^^^^^^^

The Users tab is available to Company Administrators, who have additional permissions versus Standard Users.

.. image:: /analyst_docs/getting_started/chapter_8_3.jpeg

**Add a New User**

Click the “Add New User” link found at the bottom of page, and the “Add User” panel opens.

    1. Enter the First Name, Last Name and Email Address of the new User – note that the email address cannot be
       modified by the User you are about to add.
    2. Click the Add button

.. image:: /analyst_docs/getting_started/chapter_8_4.jpeg

An email message will be sent to the email address of the new User with an invitation to join ThreatHQ® .

Each invitation can only be used to create a User under the email address that it was sent to, and it can only be used
once.  By default, all new Users are given the role of Standard User.

**Cancel a User Invitation**

No invitation expires unless you cancel it before the User registers with the PhishMe Intelligence portal. A User hasn’t
signed up as long as the “X” button is seen in the Operations column.

Click the “X” button to cancel the invitation.  The User will not be able to sign up.  Later on, you can send another
invitation to the same User using the same email address.

**Deactivate an Existing User**

As an Administrator, you can deactivate existing Users and disable Users’ access to the PhishMe Intelligence portal.

    1. Locate the User in your listing
    2. Click the “Pause” button under the Operations column to make the button change from black to gray, as seen in the
       before and after examples below:

Active Users

.. image:: /analyst_docs/getting_started/chapter_8_5.jpeg

Deactivated Users

.. image:: /analyst_docs/getting_started/chapter_8_6.jpeg

A deactivated User will:

    * Continue to appear in your Users listing
    * Not receive any email messages – regardless of saved preferences
    * Be able to be activated again in the future and still have access to all saved data

**Assign Administrative Access Rights to a User**

By default, the PhishMe Intelligence portal assigns “Standard User” access rights to the new user. As an Administrator,
you can assign Administrative rights to a User on your account. You can also remove Administrative rights from an
existing Administrator.

    1. Locate the User in your listing
    2. Click the Toggle On or Off button (depending on previous state of the User) under the Administrator column

.. image:: /analyst_docs/getting_started/chapter_8_7.jpeg

Manage Your API Tokens
^^^^^^^^^^^^^^^^^^^^^^

Click the API TOKENS tab to reach the page where you can request an authentication key for PhishMe’s RESTful interface
for accessing machine-readable threat intelligence data.  Access to the ThreatHQ® API is controlled by API tokens.  More
details on using the API can be found in :ref`this <developers_and_users>` section of this documentation set.

You may also click the “View API documentation” to review the functionality without generating a token.  The
documentation features example code leveraging python to make requests against the API, but you can use your preferred
scripting language to access PhishMe’s data.

.. image:: /analyst_docs/getting_started/chapter_8_8.jpeg
