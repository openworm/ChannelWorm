import subprocess, sys, unittest


def test_notebook_runs():
    """
    Test that the script exported from notebook runs without error.
    Assumes test is being run from ChannelWorm root directory.
    Converts the version controlled notebook to a python script, 
    and then runs that script.  
    """
    notebooks = ['EGL-19_IV','SLO-2_IV']
    for notebook_name in notebooks:
        code = subprocess.call('ipython nbconvert sciunit/%s.ipynb --to python' % notebook_name, shell=True)
        assert(code == 0, "Could not create python script from testing notebook %s.ipynb" % notebook_name)
        code = subprocess.call([sys.executable, '%s.py' % notebook_name],
                                cwd='tests')
        assert(code == 0, "The test script %s.py raised an error" % notebook_name)
