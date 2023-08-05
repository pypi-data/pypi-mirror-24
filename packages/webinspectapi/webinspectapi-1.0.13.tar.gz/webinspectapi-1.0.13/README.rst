WebInspect API
**************

A Python module to assist with the `WebInspect <http://www8.hp.com/us/en/software-solutions/webinspect-dynamic-analysis-dast/>`__ RESTFul API to administer scans.

Quick Start
~~~~~~~~~~~

Several quick start options are available:

- Install with pip: ``pip install webinspectapi``
- Build locally: ``python setup.py build``
- `Download the latest release <https://github.com/target/webinspectapi/releases/latest/>`__.

Example
~~~~~~~

::


    # import the package
    from webinspectapi import webinspect

    # setup webinspect connection information
    host = 'http://localhost:8083/webinspect/'

    # instantiate the webinspect api wrapper
    wi = webinspect.WebInspectAPI(host)

    # List scans
    scans = wi.list_scans()

    for scan in scans.data:
            print(str(scan['Name']), str(scan['Status']), str(scan['ID']))

Supporting information for each method available can be found in the `documentation <https://target.github.io/webinspectapi/>`__.

Bugs and Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~

Found something that doesn't seem right or have a feature request? `Please open a new issue <https://github.com/target/webinspectapi/issues/new/>`__.

Copyright and License
~~~~~~~~~~~~~~~~~~~~~

- Copyright 2017 Target Brands, Inc.
- `Licensed under MIT <https://github.com/target/webinspectapi/blob/master/LICENSE.txt/>`__.

