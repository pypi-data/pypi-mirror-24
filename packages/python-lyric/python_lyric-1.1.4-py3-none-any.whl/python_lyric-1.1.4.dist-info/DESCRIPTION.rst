=========================================================
Python API for the Honeywell Lyric™ Thermostat
=========================================================

Installation

Using pip

# Install package from PyPi
$ pip install python-lyric

Get a client_id and client_secret from
https://developer.honeywell.com

Use it in your script:
=========================================================

import lyric

lapi = lyric.Lyric(client_id=client_id, client_secret=client_secret,
                   token_cache_file=token_cache_file,
                   redirect_uri=redirect_uri, app_name=app_name)


for location in lapi.locations:
    print ('id: %s' % location.id)
    print ('name: %s' % location.name)
    print ('city: %s' % location.city)

    for user in location.users:
        print ('id: %s' % user.id)
        print ('name: %s' % user.name)
        print ('firstname: %s' % user.firstname)
        print ('lastname: %s' % user.lastname)

    for thermostat in location.thermostats:
        print ('id: %s' % thermostat.id)
        print ('name: %s' % thermostat.name)
        thermostat.temperatureSetpoint = 20

