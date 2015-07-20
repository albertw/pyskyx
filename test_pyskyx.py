''' py.test tests for pyskyx
'''

import skyx
import pytest

@pytest.fixture
def skyxconn(skyxhost):
    ''' Fixture to set up a connection
    '''
    return skyx.SkyXConnection(skyxhost)

def test_module_init():
    ''' Test the module imported by creating a SkyXConnection object
    '''
    assert skyx.SkyXConnection()

def test_connection(skyxconn):
    ''' Test our connection. Find will work or throw an exception.'''
    assert skyxconn._send('sky6StarChart.Find("Saturn")') == "undefined"

def test_find(skyxconn):
    ''' Test our connection. Find will work or throw an exception.'''
    assert skyxconn.find('Saturn') == True

def test_Application(skyxconn):
    ''' Test the application class'''
    assert skyxconn._send('Application.initialized') == "true"

def test_sky6ObjectInformation(skyxconn):
    ''' Test Object information. Check we get some sort of sane response '''
    info = skyxconn.sky6ObjectInformation("Saturn")
    assert info['sk6ObjInfoProp_DEC_2000']

def test_TheSkyXAction(skyxconn):
    ''' Test TheSkyXAction
    '''
    assert skyxconn.TheSkyXAction("MOVE_UP") == True
    
def test_cameraConnect(skyxconn):
    ''' Test ccdsoftCameraConnect
    '''
    assert skyxconn.ccdsoftCameraConnect() == True

def test_cameraDisconnect(skyxconn):
    ''' Test ccdsoftCameraDisconnect
    '''
    assert skyxconn.ccdsoftCameraDisconnect() == True
    
def test_scopeConnect(skyxconn):
    ''' Test sky6RASCOMTeleConnect
    '''
    assert skyxconn.sky6RASCOMTeleConnect() == True
    
def test_scopeDisconnect(skyxconn):
    ''' Test sky6RASCOMTeleDisconnect
        This seems to be an expected fail as the telescope does not 
        disconnect. Need to look into this
    '''
    assert skyxconn.sky6RASCOMTeleDisconnect() == True
    
def test_closedloopslew(skyxconn):
    ''' Test a closed loop slew
        This needs the camera, telescope and image link set up correctly
            hence it will usually fail...
    '''
    skyxconn.ccdsoftCameraConnect()
    skyxconn.sky6RASCOMTeleConnect()
    assert skyxconn.closedloopslew("M81") == True
    