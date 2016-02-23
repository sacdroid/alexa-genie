import cec

class CECDevice:
    cecconfig = cec.libcec_configuration()
    lib = {}
    log_level = cec.CEC_LOG_DEBUG

    def __int__config(self):
        self.cecconfig.strDeviceName = "pyLibCec"
        self.cecconfig.bActivateSource = 0
        self.cecconfig.deviceTypes.Add(cec.CEC_DEVICE_TYPE_RECORDING_DEVICE)
        self.cecconfig.clientVersion = cec.LIBCEC_VERSION_CURRENT

    def __init__(self):
        self.__int__config()
        self.lib = cec.ICECAdapter.Create(self.cecconfig)    
        adapter = self.lib.DetectAdapters()[0]
        self.lib.Open(adapter.strComName)
        
    def ProcessCommandActiveSource(self):
        self.lib.SetActiveSource()
      
    def Pause(self):
        self.lib.SendKeypress(cec.CECDEVICE_TV, cec.CEC_USER_CONTROL_CODE_PAUSE)
      
    def TurnOn(self):
        self.lib.PowerOnDevices()
    
    def AudioStatus(self):
        return self.lib.AudioStatus()

    def Mute(self):
        self.lib.AudioToggleMute()
    
    def VolumeUp(self):
        self.lib.VolumeUp()
    
    def VolumeDown(self):
        self.lib.VolumeDown()
    
    def TurnOff(self):
        self.lib.StandbyDevices(cec.CECDEVICE_BROADCAST)
        
    def hdmi(self, number):
        command = "4f:86:1{}:00".format(number)
        self.Tx(command)
        return "OK"
    
    def Tx(self, data):
        cmd = self.lib.CommandFromString(data)
        return self.lib.Transmit(cmd)
   
    def Scan(self):
        return self.lib.GetActiveDevices()
  
      

