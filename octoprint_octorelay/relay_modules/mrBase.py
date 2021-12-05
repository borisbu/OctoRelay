## relay_modules.mrBase
##
## Relay Driver Base/Example Class - For testing
## Use this class as the prototype for your own relay driver class. It
## must have match all of the methods in this example class.

class mrBase(object):

    # Base class has no need for an init method. remove it later on
    def __init__(self):
        print("{mrBase} - Loaded.")
        pass
        
    # Open underlying relay device or interface to it. 
    # Inputs
    #   'attrs' [string]        comma separated parameters, specific to 
    #                           the relay device or interface. 
    #                           Example: (USB serial) : "/dev/ttyUSB2,115200,8N1"
    #                                    dev = "/dev/ttyUSB2, 
    #                                    baud = "115200" 8-bit no-parity, 1 stopbit
    # Note: 'attrs' is a string parameter set during plugin configuration.
    # -----------------------------------------------------------------
    def open(self, attrs):
        print("{mrBase.open()} - (!) sub-class method missing (!) - attrs :: %s" % attrs)
        pass
        
    # Close underlying device or interface. Call on shutdown or when re-
    # loading parameters.
    # -----------------------------------------------------------------
    def close(self):
        print("{mrBase.close()} - (!) sub-class method missing (!)")
        pass

    # Turn a relay on.
    # Inputs
    #   'relay' [int]           zeros-based relay number. So first relay is 0.
    #                           some relay boards may also encode a bank number 
    #                           into this value, eg. modulo 256 (as needed).
    #                           First bank is assumed to be 0, second (1 * 256) etc.
    #                           Eg. 2nd relay in Bank 1 --> relay = 257 (0x101)
    # -----------------------------------------------------------------
    def relayOn(self, relay):
        print("{mrBase.relayOn()} - (!) sub-class method missing (!) - relay :: %s" % relay)
        pass

    # Turn a relay off.
    # Inputs
    #   'relay'                 (see method header for relayOn)
    # -----------------------------------------------------------------
    def relayOff(self, relay):
        print("{mrBase.relayOff()} - (!) sub-class method missing (!) - relay :: %s" % relay)
        pass
        
    # Turn a relay to state reflected in 'on' [bool].
    # Inputs
    #   'relay'                 (see method header for relayOn)
    #   'on' [bool]             True := on/energized, False := off
    # -----------------------------------------------------------------
    def relaySet(self, relay, on=True):
        print("{mrBase.relaySet()} - (!) sub-class method missing (!) - relay :: %s, val :: %s" % (relay,on))
        pass
        
    # Get a relay state,
    # Inputs
    #   'relay'                 (see method header for relayOn)
    # Returns [bool]
    #   True                    relay is on/energized
    #   False                   relay is off
    # -----------------------------------------------------------------
    def relayGet(self, relay):
        print("{mrBase.relayGet()} - (!) sub-class method missing (!) - relay :: %s, returns (off)" % relay)
        return False

# this method must be in each driver's sub-module file!
def get_top_class_instance():
    return mrBase()

                                
