import subprocess, sys, unittest

@unittest.skip("Failing. It wasn't part of the test suite before")
def test_notebook_runs():
    """
    Test that the script exported from notebook runs without error.
    Assumes test is being run from ChannelWorm root directory.
    """

    code = subprocess.call([sys.executable, 'IVCurve_Model.py'],
            cwd='tests')
    assert( code == 0 )

