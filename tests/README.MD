ChannelWorm Test Suite
=====================

General Notes:
* Unlike with unittest, nose tests do not require a loader file (as we currently
  have with PyOpenWorm)
* Unsure if we can use nose tests with Django tests.  They will likely have to be
in a specific location under the webapps directory.  
* Use the Scratch directory for work in progress, testing new ideas.  

Naming Conventions:
* Unit test files should have test in the name
* SciUnit files should have SCU in the name, for both models and capabilities
