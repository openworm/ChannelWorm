ChannelWorm Test Suite
=====================

General Notes:
* Unlike with unittest, nose tests do not require a loader file (as we currently
  have with PyOpenWorm)
* Unsure if we can use nose tests with Django tests.  They will likely have to be
in a specific location under the webapps directory.   

Naming Conventions:
* Unit test files should have test in the name

Change Log:
7/18/2018: SciUnit tests have been removed because of the new openworm/tests repository
which will house most project-wide model-validation tests
