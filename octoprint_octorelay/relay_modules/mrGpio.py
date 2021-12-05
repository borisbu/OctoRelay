## relay_modules.mrGpio
##
## Relay Driver for native Raspberry Pi GPIO pins. For compatible
## support of Octoprint plugin "OctoRelay" older version, the GPIO 
## identification mode used is "BCM".
##
## Usage:
## Create one instance for all GPIO pins. As pins are introduced to the
## driver, a cache entry will be created in order to track it's state.
##
## pincache [array of dicts]
##   dict format: { "pin"   : [int]<pin>, 
##                  "state" : [bool]<state> }
import RPi.GPIO as GPIO

_DEBUG_MRGPIO_ = False

class mrGpio(object):

    def __init__(self):
        self.pincache = None
        if _DEBUG_MRGPIO_:  print("{mrGpio.__init__()}")

    # Test if driver is open
    # -----------------------------------------------------------------
    def _isOpen(self):
        return ( type(self.pincache).__name__ == 'list' )
    
    # return index to the cached pin or -1 if no entry
    # -----------------------------------------------------------------
    def _findCacheIdx(self, pin):
        idx = -1
        if self.pincache != None and len(self.pincache) > 0:
            for I in range(len(self.pincache)):
                if self.pincache[I]['pin'] == pin:
                    idx = I
                    break
        return idx

        
    # add a new pin to the cache, if missing
    # 'pin'   [int]   BCM pin number
    # 'state' [bool]  True := on/energized, False := off
    # Returns:
    #   reference to the pin's dictionary
    # -----------------------------------------------------------------
    def _addToCache(self, pin, state):
        D = None
        I = self._findCacheIdx(pin)
        S = GPIO.LOW # state ==> GPIO.(state)
        if state:
            S = GPIO.HIGH
        if I < 0:
            D = { 'pin' : pin, 'state' : state }
            self.pincache.append(D)
            GPIO.setup(pin, GPIO.OUT, initial=S)
            if _DEBUG_MRGPIO_:  print("{mrGpio._addToCache()} - new pin[%s] state[%s]" % (pin,state))
        else:
            D = self.pincache[I]
            # update pin, if already in cache and in wrong state
            if D['state'] != state:
                GPIO.output(pin, S)
                if _DEBUG_MRGPIO_:  print("{mrGpio._addToCache()} - pin[%s] new state[%s]" % (pin,state))
            D['state'] = state
        return D

    
    # attrs not required... ignored.
    def open(self, attrs):
        if self._isOpen() == False:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            self.pincache = [] # cache filled as pins are first used.
            if _DEBUG_MRGPIO_:  print("{mrGpio.open()}")

        
    def close(self):
        if self._isOpen():
            GPIO.setwarnings(True)
            GPIO.cleanup()
            self.pincache = None 
            if _DEBUG_MRGPIO_:  print("{mrGpio.close()}")


    def relayOn(self, relay):
        if self._isOpen():
            if _DEBUG_MRGPIO_:  print("{mrGpio.relayOn()} - pin[%s]" % relay)
            D = self._addToCache(relay, True)


    def relayOff(self, relay):
        if self._isOpen():
            if _DEBUG_MRGPIO_:  print("{mrGpio.relayOff()} - pin[%s]" % relay)
            D = self._addToCache(relay, False)

        
    def relaySet(self, relay, on=True):
        if self._isOpen():
            if _DEBUG_MRGPIO_:  print("{mrGpio.relaySet()} - pin[%s] state[%s]" % (relay,on))
            D = self._addToCache(relay, on)

        
    def relayGet(self, relay):
        if self._isOpen():
            I = self._findCacheIdx(relay)
            if I >= 0:
                if _DEBUG_MRGPIO_:  print("{mrGpio.relayGet()} - pin[%s] state[%s]" % (relay, self.pincache[I]['state']))
                return self.pincache[I]['state']
            if _DEBUG_MRGPIO_:  print("{mrGpio.relayGet()} Error, pin[%s] not registered!" % relay)
        return False


# this method must be in each driver's sub-module file!
def get_top_class_instance():
    return mrGpio()

                                
