.. _library_reference:

========================
Python Library Reference
========================

PhishMe Intelligence
--------------------

.. autoclass:: pm_lib_intel.core.intelligence.Malware
   :members:
   :noindex:

PhishMe Brand Intelligence
--------------------------

.. automodule:: pm_lib_intel.core.brand_intelligence
   :members:
   :noindex:

PhishMe Intelligence Library Entry Points
-----------------------------------------

.. automodule:: pm_lib_intel.core.phishme
   :members:
   :noindex:

PhishMe Intelligence Library Helpers
------------------------------------

.. automodule:: pm_lib_intel.core.config_check
   :members:

.. automodule:: pm_lib_intel.core.rest_api
   :members:

.. automodule:: pm_lib_intel.core.sqlite
   :members:

.. automodule:: pm_lib_intel.core.supported_integrations
   :members:

.. automodule:: pm_lib_intel.core.syslog
   :members:

PhishMe Intelligence Library Base Classes
-----------------------------------------

.. autoclass:: pm_lib_intel.output.base_integration.BaseIntegration
   :members:

.. autoclass:: pm_lib_intel.output.generic.generic_integration.GenericIntegration
   :members:

PhishMe Intelligence integration Classes
----------------------------------------

.. autoclass:: pm_lib_intel.output.generic.pm_cef.PmCef
   :members:

.. autoclass:: pm_lib_intel.output.generic.pm_json.PmJson
   :members:

.. autoclass:: pm_lib_intel.output.generic.pm_stix.PmStix
   :members:

.. autoclass:: pm_lib_intel.output.product.arcsight.arcsight.ArcSight
   :members:

.. autoclass:: pm_lib_intel.output.product.carbon_black.carbon_black.CarbonBlack
   :members:

.. autoclass:: pm_lib_intel.output.product.crits.crits.Crits
   :members:

.. autoclass:: pm_lib_intel.output.product.logrhythm.logrhythm.LogRhythm
   :members:

.. autoclass:: pm_lib_intel.output.product.mcafee_siem.mcafee_siem.McAfeeSiem
   :members:

.. autoclass:: pm_lib_intel.output.product.qradar_siem.qradar_siem.QRadarSiem
   :members:

.. autoclass:: pm_lib_intel.output.product.threatconnect.pm_threatconnect.PmThreatConnect
   :members:

.. autoclass:: pm_lib_intel.output.product.threatconnect.pm_intel_processor.PhishMeIntelligenceProcessor
   :members:

.. autoclass:: pm_lib_intel.output.product.tipping_point_ips.tipping_point_ips.TippingPointIps
   :members:

.. _library_usage:

====================
Python Library Usage
====================

This library is intended as an incorporation of best practices for interacting with the PhishMe Intelligence product.

Synchronized Integrations
-------------------------

To execute an integration, fill out your config.ini file properly (instructions here) and do the following::

   from pm_lib_intel.core import phishme

   ARGS = phishme.read_args(SCRIPT_DESCRIPTION='This is a sample integration.')

   CONFIG = phishme.read_config(ARGS.config_file)

   pm = phishme.PhishMeIntelligence(config=CONFIG, config_file_location=ARGS.config_file)

   pm.sync()

This will contact the PhishMe Intelligence API, retrieve any new or modified threat intelligence since the last successful check-in, process it into the output(s) designated by *config.ini*, and return.

Search Integrations
-------------------
.. note:: Because of the load volume against the PhishMe Intelligence API, these should not be used for automated lookups. Instead, use `Synchronized Integrations` to archive this intelligence and perform correlations against your local repository.

These type of integrations should only be used in cases where an analyst is actively researching individual IOCs. These will typically be for research tools or Automation/Orchestration platforms. To execute, fill out your config.ini file properly and do the following::

   from pm_lib_intel.core import phishme

   ARGS = phishme.read_args(SCRIPT_DESCRIPTION='This is a sample integration.')

   CONFIG = phishme.read_config(ARGS.config_file)

   pm = phishme.PhishMeIntelligence(config=CONFIG, config_file_location=ARGS.config_file)

   results = pm.search(ioc=)

   for result in results:
      print result.threat_id

This will contact the PhishMe Intelligence API, pass any IOC or specified parameters to PhishMe, and print the ThreatId of any search results found.

