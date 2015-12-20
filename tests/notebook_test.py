import subprocess, sys, unittest


def test_notebook_runs():
    """
    Test that the script exported from notebook runs without error.
    Assumes test is being run from ChannelWorm root directory.
    Converts the version controlled notebook to a python script, 
    and then runs that script.  
    """
    notebook_name = 'SCU_IVCurve_Model'
    code = subprocess.call('ipython nbconvert %s.ipynb --to python' % notebook_name, shell=True)
    assert(code == 0, "Could not create python script from testing notebook %s.ipynb" % notebook_name)
    code = subprocess.call([sys.executable, 'SCU_IVCurve_Model.py'],
                            cwd='tests')
    assert(code == 0, "The test script %s.py raised an error" % notebook_name)
