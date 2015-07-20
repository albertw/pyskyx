''' Method to handle connections to TheSkyX
'''
from __future__ import print_function

import logging
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR, error


logger = logging.getLogger(__name__)


class SkyxObjectNotFoundError(Exception):
    ''' Exception for objects not found in SkyX.
    '''
    def __init__(self, value):
        ''' init'''
        super(SkyxObjectNotFoundError, self).__init__(value)
        self.value = value

    def __str__(self):
        ''' returns the error string '''
        return repr(self.value)


class SkyxConnectionError(Exception):
    ''' Exception for Failures to Connect to SkyX
    '''
    def __init__(self, value):
        ''' init'''
        super(SkyxConnectionError, self).__init__(value)
        self.value = value

    def __str__(self):
        ''' returns the error string '''
        return repr(self.value)

class SkyxTypeError(Exception):
    ''' Exception for Failures to Connect to SkyX
    '''
    def __init__(self, value):
        ''' init'''
        super(SkyxTypeError, self).__init__(value)
        self.value = value

    def __str__(self):
        ''' returns the error string '''
        return repr(self.value)
    

class SkyXConnection(object):
    ''' Class to handle connections to TheSkyX
    '''
    def __init__(self, host="192.168.1.123", port=3040):
        ''' define host and port for TheSkyX.
        '''
        self.host = host
        self.port = port

    def _send(self, command):
        ''' sends a js script to TheSkyX and returns the output.
        '''
        try:
            logger.debug(command)
            sockobj = socket(AF_INET, SOCK_STREAM)
            sockobj.connect((self.host, self.port))
            sockobj.send(bytes('/* Java Script */\n' +
                               '/* Socket Start Packet */\n' + command +
                               '\n/* Socket End Packet */\n'))
            oput = sockobj.recv(2048)
            logger.debug(oput)
            sockobj.shutdown(SHUT_RDWR)
            sockobj.close()
            return oput.split("|")[0]
        except error as msg:
            raise SkyxConnectionError("Connection to " + self.host + ":" + \
                                      str(self.port) + " failed. :" + str(msg))

    def find(self, target):
        ''' Find a target
            target can be a defined object or a decimal ra,dec
        '''
        output = self._send('sky6StarChart.Find("' + target + '")')
        if output == "undefined":
            return True
        else:
            raise SkyxObjectNotFoundError(target)

    def sky6RASCOMTeleConnect(self):
        ''' Connect to the telescope
        '''
        command = """
                  var Out;
                  sky6RASCOMTele.Connect();
                  Out = sky6RASCOMTele.IsConnected"""
        output = self._send(command).splitlines()
        if int(output[0]) != 1:
            raise SkyxTypeError("Telescope not connected. "+\
                                "sky6RASCOMTele.IsConnected=" + output[0])
        return True
        
    def sky6RASCOMTeleDisconnect(self):
        ''' Disconnect the telescope
            Whatever this actually does...
        '''
        command = """
                  var Out;
                  sky6RASCOMTele.Disconnect();
                  Out = sky6RASCOMTele.IsConnected"""
        output = self._send(command).splitlines()
        if int(output[0]) != 0:
            raise SkyxTypeError("Telescope still connected. " +\
                                "sky6RASCOMTele.IsConnected=" + output[0])
        return True
                
    def ccdsoftCameraConnect(self, async=0):
        ''' Connect to the camera defined in the TheSkyX profile
      
            Returns True on success or throws a SkyxTypeError
        '''
        command = """
                    var Imager = ccdsoftCamera;
                    var Out = "";
                    Imager.Connect();
                    Imager.Asynchronous = """ + str(async) + """;
                    Out = Imager.Status;
                    """
        output = self._send(command).splitlines()
        if "Ready" not in output[0]:
            raise SkyxTypeError(output[0])
        return True

    def ccdsoftCameraDisconnect(self):
        ''' Disconnect the camera
        
            Returns True on success or throws a SkyxTypeError
        '''
        command = """
                    var Imager = ccdsoftCamera;
                    var Out = "";
                    Imager.Disconnect();
                    Out = Imager.Status;
                  """
        output = self._send(command).splitlines()
        if "Not Connected" not in output[0]:
            raise SkyxTypeError(output[0])
        return True
                                    
    def closedloopslew(self, target=None):
        ''' Perform a closed loop slew.
            UNTESTED
        '''
        if target != None:
            self.find(target)
        command = '''
            var nErr=0;
            ccdsoftCamera.Connect();
            ccdsoftCamera.AutoSaveOn = 1;
            ClosedLoopSlew.exec();
            nErr = ClosedLoopSlew.exec();
            '''
        oput = self._send(command)
        for line in oput.splitlines():
            print(line)
            if "Error" in line:
                raise SkyxTypeError(line)
        return True

    def takeimages(self, exposure, nimages):
        ''' Take a given number of images of a specified exposure.
        '''
        # TODO
        command = """
        var Imager = ccdsoftCamera;
        function TakeOnePhoto()
        {
            Imager.Connect();
            Imager.ExposureTime = """+str(exposure)+"""
            Imager.Asynchronous = 0;
            Imager.TakeImage();
        }

        function Main()
        {
            for (i=0; i<"""+str(nimages)+"""; ++i)
            {
                TakeOnePhoto();
            }
        }

        Main();
        """

    def TheSkyXAction(self, action):
        ''' The TheSkyXAction object allows a script to invoke a subset of
            commands listed under Preferences, Toolbars, Customize.
        '''
        command = "TheSkyXAction.execute(\"" + action + "\")"
        oput = self._send(command)
        if oput == "undefined":
            return True
        else:
            raise SkyxObjectNotFoundError(oput)

    def Sk6ObjectInformationProperty(self, prop):
        ''' Returns a value for the desired Sk6ObjectInformationProperty
            argument.
        '''
        command = """
                var Out = "";
                sky6ObjectInformation.Property(""" + str(prop) + """);
                Out = String(sky6ObjectInformation.ObjInfoPropOut);"""
        oput = self._send(command)
        return oput

    def Sk6ObjectInformationPropertyApplies(self, prop):
        pass

    def Sk6ObjectInformationPropertyName(self, prop):
        pass


    def sky6ObjectInformation(self, target):
        ''' Method to return basic SkyX position information on a target.
        '''
        # TODO: make target optional
        # TODO: return all data
        command = """
                var Target = \"""" + target + """\";
                var Target56 = 0;
                var Target57 = 0;
                var Target58 = 0;
                var Target59 = 0;
                var Target77 = 0;
                var Target78 = 0;
                var Out = "";
                var err;
                sky6StarChart.LASTCOMERROR = 0;
                sky6StarChart.Find(Target);
                err = sky6StarChart.LASTCOMERROR;
                if (err != 0) {
                            Out = Target + " not found."
                } else {
                            sky6ObjectInformation.Property(56);
                            Target56 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(57);
                            Target57 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(58);
                            Target58 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(59);
                            Target59 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(77);
                            Target77 = sky6ObjectInformation.ObjInfoPropOut;
                            sky6ObjectInformation.Property(78);
                            Target78 = sky6ObjectInformation.ObjInfoPropOut;
                            Out = "sk6ObjInfoProp_RA_2000:"+String(Target56)+
                            "\\nsk6ObjInfoProp_DEC_2000:"+String(Target57)+
                            "\\nsk6ObjInfoProp_AZM:"+String(Target58)+
                            "\\nsk6ObjInfoProp_ALT:"+String(Target59)+
                            "\\nsk6ObjInfoProp_RA_RATE_ASPERSEC:"+String(Target77)+
                            "\\nsk6ObjInfoProp_DEC_RATE_ASPERSEC:"+String(Target78)+"\\n";

                }
                """
        results = {}
        oput = self._send(command)
        for line in oput.splitlines():
            if "Object not found" in line:
                raise SkyxObjectNotFoundError("Object not found.")
            if ":" in line:
                info = line.split(":")[0]
                val = line.split(":")[1]
                results[info] = val
        return results
