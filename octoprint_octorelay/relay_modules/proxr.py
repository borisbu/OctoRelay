## relay_modules.proxr
##
## Relay Driver Base/Example Class - For testing
## Use this class as the prototype for your own relay driver class. It
## must have match all of the methods in this example class.



## ********************************************************************
## proxr_lib.py
## A Python3 I/O Library for the ProXR Relay Serial Command Protocol
## Library from: https://github.com/RichardEWillis/ProXRLib_Python3
##  (with permission)
##
## Version:       1.0
## Last Modified: Nov 2021 (REW)
##
## Requirements:
## [1] PySerial Library (Python3) 
##     https://pyserial.readthedocs.io/en/latest/pyserial.html
##
## ********************************************************************

import serial
from enum import Enum


# decodes Comms-Test return value
class STATUS(Enum):
    RUN    = 85     # normal mode
    CONFIG = 86     # config set on bank/board
    LOCKDN = 87     # board in lockdown mode


# Command Return Code
class CMDSTATE(Enum):
    FAIL = -1       # Cmd Nack : Failed
    OK   =  0       # Cmd ACK  : Success
    RCLR =  1       # [Relay] Clear/Open
    RSET =  2       # [Relay] Set/Closed


class ProXRLib(object):

    # Timeout: affects blocking vs non-blocking
    #           0 := non-blocking
    #           n := block read for n seconds (floating pt. OK)
    #        None := wait forever on a read
    def __init__(self, timeout=0, useHWRTS=False, useHWDSR=False, useXONXOFF=False):
        self.tmout = timeout
        self.use_HW_RTSCTS = useHWRTS
        self.use_HW_DSRDTR = useHWDSR
        self.use_SW_XON_XOFF = useXONXOFF
        self.ser = None
        pass
    
    # Parity Types: 'N'one, 'E'ven, 'O'dd, 'M'ark, 'S'pace
    def open(self, devname, baud=115200, bits=8, stops=1, parity='N'):
        # san-checks
        e_bitsz  = serial.EIGHTBITS
        e_parity = serial.PARITY_NONE
        e_stops  = serial.STOPBITS_ONE
        
        if bits == 5:
            e_bitsz = serial.FIVEBITS
        elif bits == 6:
            e_bitsz = serial.SIXBITS
        elif bits == 7:
            e_bitsz = serial.SEVENBITS
        elif bits == 8:
            e_bitsz = serial.EIGHTBITS
        else:
            raise Exception('Invalid bits, must be one of: {5,6,7,8}')

        if stops == 1:
            e_stops  = serial.STOPBITS_ONE
        elif stops == 2:
            e_stops  = serial.STOPBITS_TWO
        else:
            raise Exception('Invalid stops, must be one of: {1,2}')
            
        if parity == 'E':
            e_parity = serial.PARITY_EVEN
        elif parity == 'O':
            e_parity = serial.PARITY_ODD
        elif parity == 'N':
            e_parity = serial.PARITY_NONE
        elif parity == 'M':
            e_parity = serial.PARITY_MARK
        elif parity == 'S':
            e_parity = serial.PARITY_SPACE
        else:
            raise Exception('Invalid parity, must be one of: {E,O,N,M,S}')
            
        self.ser = serial.Serial(port=devname, baudrate=baud, bytesize=e_bitsz, 
            parity=e_parity, stopbits=e_stops, timeout=self.tmout, 
            xonxoff=self.use_SW_XON_XOFF, rtscts=self.use_HW_RTSCTS,
            dsrdtr=self.use_HW_DSRDTR, write_timeout=self.tmout,
            exclusive=True)
            
    def close(self):
        self.ser.close()
        self.ser = None

    def isOpen(self):
        return (self.ser != None)

    def _reader(self, count):
        if self.ser:
            return self.ser.read(count)
        return None
    
    def _readAck(self):
        inb = self._reader(1)
        return (inb.hex() == '55')
        
    # 'bout' must be of type 'bytearray'
    def _writer(self, bout):
        if self.ser:
            bout = bytearray(b'\xfe') + bout # add the preamble
            ret = self.ser.write(bout)
            return  ret - 1 # return no. 'bout' bytes sent, cmd preamble is not counted.
        return 0
    
    # Send a Comms Test.
    # Returns: one of {STATUS.RUN, STATUS.CONFIG, STATUS.LOCKDN} or None if closed.
    def Cmd_CommsTest(self):
        if self.ser:
            if self._writer(bytearray(b'\x21')) == 1:
                # returns: single element of type 'byte'
                #          convert to hex string then to base 10 int
                ack = int( self._reader(1).hex(), 16 )
                if ack == STATUS.RUN.value:
                    return STATUS.RUN
                elif ack == STATUS.CONFIG.value:
                    return STATUS.CONFIG
                elif ack == STATUS.LOCKDN.value:
                    return STATUS.LOCKDN
                else:
                    raise Exception('Unexpected return value from CommsTest')
        return None

    # Convert Comms Test state to a descriptive string.
    def StatusDesc(self, st):
        if st == STATUS.RUN:
            return "Normal running Mode"
        elif st == STATUS.CONFIG:
            return "Configuration Mode"
        elif st == STATUS.LOCKDN:
            return "Lockdown Mode"
        else:
            return "Unknown state ???"

    # Set/Clear a Relay
    # Bank: 1 .. 255 (Default = 1) (NOTE: Currently only Bank:1 is available)
    # Relay {0..7}. 0 := first relay in bank of 8
    # setOn {True, False} True := will close the relay contact (RSET).
    # Returns: (Enum)CMDSTATE: {OK,FAIL}
    def Cmd_Relay(self, relay=0, bank=1, setOn=False):
        if self.ser:
            if (relay > 7) or (relay < 0):
                raise Exception('Invalid Relay, range{0..7}')
            if bank != 1:
                raise Exception('Invalid Bank, At present, only 1 is supported')
            ba = bytearray()
            if setOn:
                ba.append(0x6c + relay)
            else:
                ba.append(0x64 + relay)
            ba.append(bank)
            if self._writer(ba) == 2 and self._readAck() == True:
                return CMDSTATE.OK
        return CMDSTATE.FAIL
        
    # Read a relay
    # Bank: 1 .. 255 (Default = 1) (NOTE: Currently only Bank:1 is available)
    # Relay {0..7}. 0 := first relay in bank of 8
    # Returns: (Enum)CMDSTATE: {FAIL,RCLR,RSET}
    def Cmd_RelayState(self, relay=0, bank=1):
        if self.ser:
            if (relay > 7) or (relay < 0):
                raise Exception('Invalid Relay, range{0..7}')
            if bank != 1:
                raise Exception('Invalid Bank, At present, only 1 is supported')
            ba = bytearray()
            ba.append(0x74 + relay)
            ba.append(bank)
            if self._writer(ba) == 2:
                res = self._reader(1)
                if res.hex() == '01':
                    return CMDSTATE.RSET
                else:
                    return CMDSTATE.RCLR
        return CMDSTATE.FAIL



_DEBUG_PROXR_ = False

# ---------------------------------------------------------------------

class mrProXR(object):

    def __init__(self):
        self.pxrdriver = None  # class ProXRLib
        if _DEBUG_PROXR_:  print("{mrProXR.__init__()}")

    
    def _isOpen(self):
        return (type(self.pxrdriver).__name__ != 'NoneType')    


    def _decodeRB(self,relay):
        # (!) bump bank up by 1. 0 means all banks and is currently not 
        #     supported by the underlying library API.
        # (!) bnk,rly must both be of type 'int'
        bnk = relay / 256
        rly = relay % 256
        return( int(bnk+1), int(rly) )
        
    # Open underlying relay device or interface to it. 
    # Inputs
    #   'attrs' [string] format: <dev[,baud[,bits,par,stops]]>
    #     defaults:
    #       <baud>
    #       <bits,par,stops>
    #     internal:
    #       <timeout>       1 second (serial must block to receive response)
    # -----------------------------------------------------------------
    def open(self, attrs):
        if self._isOpen():
            return
        if _DEBUG_PROXR_:  print("{mrProXR.open()} - attrs[%s]" % attrs)
        atlist = attrs.split(',')
        self.dev = atlist[0]
        if _DEBUG_PROXR_:  print("{mrProXR.open()} - dev[%s]" % self.dev)
        self.baud = 115200
        self.bits = 8
        self.parity = 'N'
        self.stops = 1
        self.tmout = 1
        if len(atlist) > 1:
            self.baud = atlist[1]
            if _DEBUG_PROXR_:  print("{mrProXR.open()} - new baud[%s]" % self.baud)
        if len(atlist) > 2:
            self.bits = atlist[2]
            if _DEBUG_PROXR_:  print("{mrProXR.open()} - new bits[%s]" % self.bits)
        if len(atlist) > 3:
            self.parity = atlist[3]
            if _DEBUG_PROXR_:  print("{mrProXR.open()} - new parity[%s]" % self.parity)
        if len(atlist) > 4:
            self.stops = atlist[4]
            if _DEBUG_PROXR_:  print("{mrProXR.open()} - new stop bits (stops)[%s]" % self.stops)
        if _DEBUG_PROXR_:
            print("{mrProXR.open()} - dev[%s] baud[%s] bits/par/stops[%s%s%s] tmout[%s]" % (
                self.dev, self.baud, self.bits, self.parity, self.stops, self.tmout))
        self.pxrdriver = ProXRLib(timeout=self.tmout)
        self.pxrdriver.open(devname=self.dev, baud=self.baud, bits=self.bits, stops=self.stops, parity=self.parity)
        if _DEBUG_PROXR_:  print("{mrProXR.open()} - OK")


    # Close underlying device or interface. Call on shutdown or when re-
    # loading parameters.
    # -----------------------------------------------------------------
    def close(self):
        if self._isOpen():
            self.pxrdriver.close()
            self.pxrdriver = None
            if _DEBUG_PROXR_:  print("{mrProXR.close()} - OK")


    def relayOn(self, relay):
        if self._isOpen():
            (bnk,rly) = self._decodeRB(relay)
            rc = self.pxrdriver.Cmd_Relay(relay=rly, bank=bnk, setOn=True)
            if rc == CMDSTATE.OK:
                if _DEBUG_PROXR_:  print("{mrProXR.relayOn()} - B[%s] R[%s] - OK" % (bnk,rly))
                return
        if _DEBUG_PROXR_:  print("{mrProXR.relayOn()} - Error, R[%s] not open."% relay)


    def relayOff(self, relay):
        if self._isOpen():
            (bnk,rly) = self._decodeRB(relay)
            rc = self.pxrdriver.Cmd_Relay(relay=rly, bank=bnk, setOn=False)
            if rc == CMDSTATE.OK:
                if _DEBUG_PROXR_:  print("{mrProXR.relayOff()} - B[%s] R[%s] - OK" % (bnk,rly))
                return
        if _DEBUG_PROXR_:  print("{mrProXR.relayOff()} - Error, R[%s] not open."% relay)
        

    def relaySet(self, relay, on=True):
        if self._isOpen():
            (bnk,rly) = self._decodeRB(relay)
            rc = self.pxrdriver.Cmd_Relay(relay=rly, bank=bnk, setOn=on)
            if rc == CMDSTATE.OK:
                if _DEBUG_PROXR_:  print("{mrProXR.relaySet()} - B[%s] R[%s] - OK" % (bnk,rly))
                return
        if _DEBUG_PROXR_:  print("{mrProXR.relaySet()} - Error, R[%s] not open."% relay)
        

    def relayGet(self, relay):
        if self._isOpen():
            (bnk,rly) = self._decodeRB(relay)
            rc = self.pxrdriver.Cmd_RelayState(relay=rly, bank=bnk)
            if rc == CMDSTATE.RSET:
                if _DEBUG_PROXR_:  print("{mrProXR.relayGet()} - B[%s] R[%s] : (ON) - OK" % (bnk,rly))
                return True
            elif rc == CMDSTATE.RCLR:
                if _DEBUG_PROXR_:  print("{mrProXR.relayGet()} - B[%s] R[%s] : (OFF) - OK" % (bnk,rly))
                return False
        if _DEBUG_PROXR_:  print("{mrProXR.relayGet()} - Error, R[%s] not open."% relay)
        return False


# this method must be in each driver's sub-module file!
def get_top_class_instance():
    return mrProXR()

                                
