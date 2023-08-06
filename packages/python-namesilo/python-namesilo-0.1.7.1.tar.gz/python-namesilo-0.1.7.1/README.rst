python-namesilo
===============

|Build Status| |CodeCov| |PyPiVersion|

version: 0.1.7.1

This code is written in Python 3.6.x. If you want to contribute to this
project feel free to contact me at any time.

Goals for implementation
~~~~~~~~~~~~~~~~~~~~~~~~

-  [x] registerDomain:\* Register a new domain name
-  [ ] registerDomainDrop:\* Register a new domain name using drop-catching
-  [x] renewDomain:\* Renew a domain name
-  [ ] transferDomain:\* Transfer a domain name into your NameSilo account
-  [ ] checkTransferStatus: Check the status of a domain transfer
-  [x] checkRegisterAvailability: Determine if up to 200 domains can be registered at this time
-  [ ] checkTransferAvailability: Determine if up to 200 domains can be transferred into your account at this time
-  [x] listDomains: A list of all active domains within your account
-  [x] getDomainInfo: Get essential information on a domain within your account
-  [x] contactList: View all contact profiles in your account
-  [x] contactAdd: Add a contact profile to your account
-  [x] contactUpdate: Update a contact profile in account
-  [x] contactDelete: Delete a contact profile in account
-  [ ] contactDomainAssociate: Associate contact profiles with a domain
-  [ ] dnsListRecords: View all DNS records associated with your domain
-  [ ] dnsAddRecord: Add a new DNS resource record
-  [ ] dnsUpdateRecord: Update an existing DNS resource record
-  [ ] dnsDeleteRecord: Delete an existing DNS resource record
-  [x] changeNameServers: Change the NameServers for up to 200 domains
-  [ ] portfolioList: List the active portfolios within your account
-  [ ] portfolioAdd: Add a portfolio to your account
-  [ ] portfolioDelete: Delete a portfolio from your account
-  [ ] portfolioDomainAssociate: Add up to 200 domains to a portfolio
-  [ ] listRegisteredNameServers: List the Registered NameServers associated with one of your domains
-  [ ] addRegisteredNameServer: Add a Registered NameServer for one of your domains
-  [ ] modifyRegisteredNameServer: Modify a Registered NameServer
-  [ ] deleteRegisteredNameServer: Delete a Registered NameServer
-  [ ] addPrivacy: Add WHOIS Privacy to a domain
-  [ ] removePrivacy: Remove WHOIS Privacy from a domain
-  [ ] addAutoRenewal: Set your domain to be auto-renewed
-  [ ] removeAutoRenewal: Remove the auto-renewal setting from your domain
-  [ ] retrieveAuthCode: Have the EPP authorization code for the domain emailed to the administrative contact
-  [ ] domainForward: Forward your domain
-  [ ] domainForwardSubDomain: Forward a sub-domain
-  [ ] domainForwardSubDomainDelete: Delete a sub-domain forward
-  [x] domainLock: Lock your domain
-  [x] domainUnlock: Unlock your domain
-  [ ] listEmailForwards: List all email forwards for your domain
-  [ ] configureEmailForward: Add or modify an email forward for your domain
-  [ ] deleteEmailForward: Delete an email forward for your domain
-  [ ] emailVerification Verify a Registrant email address

.. |Build Status| image:: https://travis-ci.org/goranvrbaski/python-namesilo.svg?branch=master
   :target: https://travis-ci.org/goranvrbaski/python-namesilo

.. |CodeCov| image:: https://codecov.io/gh/goranvrbaski/python-namesilo/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/goranvrbaski/python-namesilo

.. |PyPiVersion| image:: https://badge.fury.io/py/python-namesilo.svg
   :target: https://badge.fury.io/py/python-namesilo