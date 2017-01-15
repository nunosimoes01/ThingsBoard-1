#!/usr/bin/env python
import sys
import time


'''
========================================================================================================
SYNOPSIS
    'config.py' holds all the information needed to run the 'monitor.py' script to publish telemetry
        and attributes to a Thingsboard IoT server.
    
DESCRIPTION
    This script contains all the necessary configuration settings to gather telemetry information and
        submit to a Thingsboard server.  This file is heavily commented to make sure that you understand
        the different options, and their purposes.

REQUIRES
    The following requirements must be met
        Thingsboard Server      As configured in config.py, it is the destination
                                to which information is sent.  You can get a demo
                                account at http://demo.thingsboard.io
        Thingsboard Device      The "authkey" as defined in config.py is a unique key
                                for each device in Thingsboard, and defines the target
                                to which telemetry and attribute information will be published.
        Required libraries      See top of script for the list of python libraries needed, and their use
        
AUTHOR
    Bob Perciaccante - Bob@perciaccante.net
    
VERSION
    1.4 - 1/15/2017 - Initial publication
========================================================================================================
'''

me = {
    'ver': '1.4',
    'name': 'config.py'
    }
'''
========================================================================================================
Connection Configuration:
---------------------
This section defines how your host will connect to the Thingsboard server.

*Note* you will need to have an account on the Thingsboard Demo server, located at http://demo.thingsboard.io
    or you will need to have a local installation of Thingsboard.

In order to support the publication of telemetry and attributes via HTTP through a proxy, if necessary you can
    define the proxy needed below.  The actual hosts will be ignored if 'proxy' is set to 0
========================================================================================================
    
'''
conn = {
    'server': '[YOUR SERVER HERE]',              # IP or hostname of manager    
    'port': 1883,                                 # MQTT server port number (MQTT transport not yet supported in this script)
    'method': "http",                             # Method used to send data to TB server
    'proxy': 0,                                   # (0,1) If you need to go through a proxy, set to 1
    'proxy_http': 'http://[YOURPROXY}{:PROXY PORT]',
    'proxy_https': 'https://[YOURPROXY}{:PROXY PORT]'
    }

# These values are used for HTTP POST operations, and supporting the use of proxies easily in functions in
#    'common.py'

http_headers = {'Content-Type': 'application/json'}
proxies = {
     'http': conn['proxy_http'],
     'https': conn['proxy_https']
    }
'''
========================================================================================================
Sensor Configuration:
---------------------

The sensor definitions are broken up into four sections: notes, settings, attributes, and telemtry (sources).

Notes:
    Since it can become confusing keeping track of different sensors based primarily on device auth token,
        this section is completely free-form, and is not used for any processing.  This should allow you to
        include many sensors and potentially a complex deployment, with relative ease.

Settings (settings):
    Settings are required - and define how the device is handled
    |-----------------------------------------------------------------------------------------|
    |      Key     |  Value |                        Notes                                    |
    |-----------------------------------------------------------------------------------------|
    | active       | 0 or 1 | If enabled, device will be processed - otherwise will be ignored|
    |--------------|--------|-----------------------------------------------------------------|
    | sys_info     | 0 or 1 | If enabled, local machine stats will be collected. CPU Temp not |
    |              |        |   available on Win32                                            |
    |--------------|--------|-----------------------------------------------------------------|
    | cache_on_err | 0 or 1 | If enabled, telemetry will be cached if connection errors occur |
    |--------------|--------|-----------------------------------------------------------------|
    |              |        | If enabled, script will try to push cache files to server for   |
    |  clearcache  | 0 or 1 |    this sensor, even if localonly is set.  This will cause the  |
    |              |        |    last record to be cached for a period of time before being   |
    |              |        |    published - useful for troubleshooting                       |
    |--------------|--------|-----------------------------------------------------------------|
    | localonly    | 0 or 1 | If enabled, script will not try to publish, but will cache      |
    |              |        |    locally only.  Does not override clearcache                  |
    |--------------|--------|-----------------------------------------------------------------|
    
Attributes (attr):
    Attributes are free-form.  The values in the attr dictionary block are passed as-is as device
        attributes.  Note - betware that these values do not contain characters that could be
        interpreted by the server as operators - for example, use '_' instead of '-'
    
Telemetry (tele):
    Telemetry keys are where the processing of sensor data takes place.  Currently supported
        options are below:
    |-----------------------------------------------------------------------------------------|
    |      Key     |                                 Notes                                    |
    |-----------------------------------------------------------------------------------------|
    |  type        | defines the function to be used to process the 'device' key.  Functions  |
    |              |     should be added to the common.py file to keep standardized           |
    |-----------------------------------------------------------------------------------------|
    |              | defines the device or target asset to gather the appropriate telemetry.  |
    |  device      |     ds18b20: /sys/bus/w1/devices/28*/w1_slave is an example              |
    |              |     weather: incude the ZIP code of the area you want to gather telemetry|
    |              |         information on                                                   |
    |-----------------------------------------------------------------------------------------|
    |              | defines the label used to reflect that specific sensor, a temperature    |
    |  label       |    sensor would be sent as telemetry value 'temp_[label]'.  This allows  |
    |              |    for more than one sensor to be installed on a single system.          |
    |-----------------------------------------------------------------------------------------|

========================================================================================================
   '''
sensors = [
    {'authkey': '[AUTHKEY #1]',
         'notes': {
             'notes': 'The label of this on the Device list is "Example 1"',
             },
         'settings': {                
            'active': 1,
            'sys_info': 1,
            'cache_on_err': 1,
            'clearcache': 0,
            'localonly': 1
             },
         'attr': {
            'platform': "Raspberry Pi 2",
            'name': '[DESCRIPTIVE NAME LIKE "My Office"]',
            'location': '[DESCRIPTIVE LOCATION LIKE "Hometown"]',
            'address': '[STREET ADDRESS - USED FOR MAPS]',
            'lattitude': '[GET FROM www.latlong.net - also can come from API source]',
            'longitude': '[GET FROM www.latlong.net - also can come from API source]',
            'contact': '[NAME OF PERSON RESPONSIBLE FOR AREA]',
            'contact_email': '[CONTACT EMAIL ADDRESS]',
            'contact_phone': '[CONTACT PHONE NUMBER]',
            'temp_low': '[LOWER TEMP THRESHOLD]',
            'temp_high': '[UPPER TEMP THRESHOLD]'
             },
         'tele': {
            'type': 'ds18b20',
            'device': '/sys/bus/w1/devices/[YOUR DEVICE ID HERE]/w1_slave',
            'label': 'office'
             }
     },
     {'authkey': '[AUTHKEY #2]',
          'notes': {
                 'notes': 'Another place to put notes that wont affect the program at all',
                 },
         'settings': {
            'active': 1,
            'sys_info': 1,
            'cache_on_err': 0,
            'clearcache': 0,
            'localonly': 1
             },
         'attr': {
            'platform': "API Call",
            'name': 'Local Weather - MyHomeTown',
            'location': '[DESCRIPTIVE LOCATION LIKE "Hometown"]',
            'address': '[STREET ADDRESS - USED FOR MAPS]',
            'lattitude': '[GET FROM www.latlong.net - also can come from API source]',
            'longitude': '[GET FROM www.latlong.net - also can come from API source]',
            'contact': '[NAME OF PERSON RESPONSIBLE FOR AREA]',
            'contact_email': '[CONTACT EMAIL ADDRESS]',
            'contact_phone': '[CONTACT PHONE NUMBER]',
            'temp_low': '[LOWER TEMP THRESHOLD]',
            'temp_high': '[UPPER TEMP THRESHOLD]'
             },
         'tele': {
            'type': 'owm', 
            'device': '10118',
            'label': 'ignored'
             }
     }
]

'''
========================================================================================================
Logging configurations go here and both define logging destinations, as well as assemble variables into
    more usable format in the functions called
========================================================================================================
'''
logs = {
        'cachedir': 'cache/',                                      # Location where cache files will be stored
        'logdir': 'logs/',                                         # where log file will be kept
        'logfile': time.strftime("%Y-%m-%d") + '_messages.log'     # log file name
    }
logfile = logs['logdir'] + logs['logfile']
cachefile = logs['cachedir']


'''
========================================================================================================
Custom configuration settings can be added below this point for different sensor types, add-on services,
    etc.
========================================================================================================
'''

# Settings spefically for OpenWeatherMaps integration.  To use OpenWeatherMaps, you will need an API key
#    specific to your installation.  You can get more information on API keys on their website at:
#    https://openweathermap.org/api

owm_settings = {
    'owm_api': '[YOUR API KEY HERE]',
    'owm_format': 'json',
    'owm_url': 'http://api.openweathermap.org/data/2.5/weather?us&APPID=',
    'temp_units': 'f',
    }
owm_url = owm_settings['owm_url']+owm_settings['owm_api']+'&mode='+owm_settings['owm_format']

# Settings spefically for WeatherUnderground integration.  To use WeatherUnderground, you will need an API key
#    specific to your installation.  You can get more information on API keys on their website at:
#    https://www.wunderground.com/weather/api/
wund_settings = {
    'wund_api': '[YOUR API KEY HERE]',
    'wund_format': 'json'
    }
wund_url = 'http://api.wunderground.com/api/'+wund_settings['wund_api']+'/geolookup/conditions/q/'
