## relay_loader.py
## [Relay Modules Support] - top level relay driver loader. 
##
## import this python and call instantiate_relay_object() with the 
## relay driver's name. An instantiated object of the top-level
## class for that driver is returned, or None if the relay name is
## unknown.
##
## Adding new relay types:
## [1] create a new python file, in relay_modules/, and add a new
##     class. The new class must exactly replicate all methods found in 
##     mrBase.py (!) It does not need to derive from mrBase!
## [2] The new driver can use sub-classes but the top level class 
##     is the only one returned. A top class instance is created locally
##     in the sub-module's function: get_top_class_instance() and returns 
##     an instance of the top level class.
##     (!) Each relay driver (submodule) must contain its own definition
##         of get_top_class_instance()
## [3] Register the new driver in the json file "relay_register.json". 
##     follow the format below.
## [4] Top level documentation must be updated to identify the new driver,
##     and specify the driver's name so that it can be configured in the
##     OctoPrint config section for OctoRelay by a user.
##
## Registration file [json] format:
## { "relays" : 
##     [   
##         { "name" : "GPIO",  "submod" : "gpio"   },
##         { "name" : "ProXr", "submod" : "proxr"  },
##         { "name" : "null",  "submod" : "mrBase" }
##     ]
## }
## name:   [string] formal name of the relay driver. specified in Octoprint Config
## submod: [string] python sub-module filename, eg. "gpio" --> relay_modules/gpio.py
##
## Note: sub-module "null" is a special default driver that can be loaded during 
##       self-tests and TDD. It generates explicit strings when it's methods are
##       called and also acts as the class method prototype for other drivers.
##
## Typical Usage:
## [1] the driver name is known (from configuration params or in testing)
##     eg. 'null' (load the test driver)
## [2] code:
##      import relay_loader # only call once for each run-cycle of OctoPrint.
##      ...
##      # open-close cycles can be repeated in an OctoPrint run-cycle.
##      driver = relay_loader.instantiate_relay_object('null')
##      if driver != None:
##          driver.open(attrs)
##          ...
##          driver.relaySet(0, True)  # turn on first relay, relay # is zeros's based!
##          ...
##          driver.close() # close out the driver
##          driver = None 

import json
import importlib

## Called by the top level python script, __init__.py, to find the 
## relevent relay class. Relays are registered in a json file along
## with the class name for the API.
## function returns a created instance for this relay, or None if the
## relay name was not matched.
def instantiate_relay_object( relayName ):
    jsonDBName = "relay_register.json"
    relayDBFile = None
    relay = None
    try:
        relayDBFile = open(jsonDBName, 'r')
        relayDB = json.load(relayDBFile)
        relayDBFile.close()
        for R in relayDB['relays']:
            if R['name'] == relayName:
                submodpath = 'relay_modules.%s' % R['submod']
                sm = importlib.import_module(submodpath)
                relay = sm.get_top_class_instance()
    except:
        if relayDBFile != None:
            relayDBFile.close()
        return None
    return relay
    
