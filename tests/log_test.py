"""This tests logging"""

import os
from os import path


def test_logs_file(client):
    """This gets path to logs"""
    p = "../app/locs/info.log"
    # assert os.getcwd() == "hi"
    path.isfile(p)
    # assert path.exists('chill_brz2l8x/') # Documents/IS218/myclass/flask_auth/tests')
    # assert path.isdir('../app')
