import pytest

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="localhost",
        help="host: Host running TheSkyX")

@pytest.fixture
def skyxhost(request):
    return request.config.getoption("--host")

