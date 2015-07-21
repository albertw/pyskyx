''' py.test tests for pyskyx
'''

import skyx
import pytest

@pytest.fixture
def skyxconn(skyxhost):
    ''' Fixture to set up a connection
    
        Need to set the host explicitly here as py.test seems to call it
        earlier and as a singleton we get the default host not the one
        we want.
    '''
    conn = skyx.SkyXConnection(skyxhost)
    conn.host = skyxhost
    return conn

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
    info = skyx.sky6ObjectInformation().sky6ObjectInformation("Saturn")
    assert info['sk6ObjInfoProp_DEC_2000']

def test_TheSkyXAction(skyxconn):
    ''' Test TheSkyXAction
    '''
    assert skyx.TheSkyXAction().TheSkyXAction("MOVE_UP") == True
    
def test_cameraConnect(skyxconn):
    ''' Test ccdsoftCameraConnect
    '''
    camera = skyx.ccdsoftCamera()
    assert camera.Connect() == True

def test_cameraDisconnect(skyxconn):
    ''' Test ccdsoftCameraDisconnect
    '''
    camera = skyx.ccdsoftCamera()
    assert camera.Disconnect() == True

def test_setcameraExposureTime(skyxconn):
    ''' Test ccdsoftCameraDisconnect
    '''
    camera = skyx.ccdsoftCamera()
    assert camera.ExposureTime(23) == str(23)
    
def test_getcameraExposureTime(skyxconn):
    ''' Test ccdsoftCameraDisconnect
    '''
    camera = skyx.ccdsoftCamera()
    assert camera.ExposureTime() == str(23)

def test_setcameraBin(skyxconn):
    ''' Test ccdsoftCameraDisconnect
    '''
    camera = skyx.ccdsoftCamera()
    assert camera.ExposureTime(3) == str(3)
    
def test_getcameraBin(skyxconn):
    ''' Test ccdsoftCameraDisconnect
    '''
    camera = skyx.ccdsoftCamera()
    assert camera.ExposureTime() == str(3)

def test_setcameraFrame(skyxconn):
    ''' Test ccdsoftCameraDisconnect
    '''
    camera = skyx.ccdsoftCamera()
    assert camera.Frame("Light") == "Light"
    
def test_getcameraFrame(skyxconn):
    ''' Test ccdsoftCameraDisconnect
    '''
    camera = skyx.ccdsoftCamera()
    assert camera.Frame() == "Light"
                
def test_scopeConnect(skyxconn):
    ''' Test sky6RASCOMTeleConnect
    '''
    tele = skyx.sky6RASCOMTele()
    assert tele.Connect() == True
    
def test_scopeDisconnect(skyxconn):
    ''' Test sky6RASCOMTeleDisconnect
        This seems to be an expected fail as the telescope does not 
        disconnect. Need to look into this
    '''
    tele = skyx.sky6RASCOMTele()
    assert tele.Disconnect() == True
    
def test_takeImage(skyxconn):
    ''' Test taking an image.
    '''
    pass

def test_closedloopslew(skyxconn):
    ''' Test a closed loop slew
        This needs the camera, telescope and image link set up correctly
            hence it will usually fail...
    '''
    skyx.ccdsoftCamera().Connect()
    skyx.sky6RASCOMTele().Connect()
    assert skyxconn.closedloopslew("M81") == True
    