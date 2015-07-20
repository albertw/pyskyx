''' pytest configuration to allow --host command line arg for tests.
'''
import pytest

def pytest_addoption(parser):
    ''' Add command line option
    '''
    parser.addoption("--host", action="store", default="localhost",
                     help="host: Host running TheSkyX")

@pytest.fixture
def skyxhost(request):
    ''' pytest fixture to allow the command line arg to be used.
    '''
    return request.config.getoption("--host")

