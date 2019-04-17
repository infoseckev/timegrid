from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

import json
import random
import datetime

def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    headers = [('content-type', 'application/json')]

    #faire dequoi ici pour sécuriser l'application et ne pas permettre CORS
    headers.extend([
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Credentials", "true"),
        ("Access-Control-Allow-Methods", "PUT, GET, OPTIONS, HEAD")
    ])

    numberOfFlights = 25
    flightInfo = getFlightInfo(numberOfFlights)

    test = json.dumps(flightInfo)
    test1 = bytes(test, 'utf-8')  # or test.encode('utf-8')
    start_response('200 OK', headers)
    return [test1]

def getFlightInfo(numberOfFlights) :
    destinations = ['Montréal', 'Vancouver', 'Ottawa', 'Halifax', 'Toronto','Edmonton', 'Québec', 'Calgary', 'Charlottetown', 'St-John\'s', 'Paris', 'Amsterdam']
    carriers = ['Air Canada', 'WestJet', 'Air Transat', 'Wow Air', 'Cyber Sécurit-Air',  'Porter Airlines']
    #on ajoute de l'importance sur les "On Time" par un multiple de 7
    statusList = ['On Time'] * 7 + ['Delayed'] * 2 + ['Cancelled'] * 1
    flightInfo = []
    minuteTillArrival = sorted(random.sample(range(3, 400), numberOfFlights))

    for x in range(numberOfFlights):
        flightNumber = random.randint(1000, 1999)
        gate = random.randint(1, 25)
        arrivalTime = str((datetime.datetime.now() + datetime.timedelta(minutes=minuteTillArrival[x])).strftime("%H:%M"))

        # il ne faudrait pas changer ceci a Cancelled...
        status = random.choice(statusList)

        flightInfo.append({'destination': random.choice(destinations),
                           'carrier': random.choice(carriers),
                           'flight': flightNumber,
                           'gate': gate,
                           'time': arrivalTime,
                           'status': status
                           })

    return flightInfo

httpd = make_server('', 8080, simple_app)
print("Serving on port 8080...")
httpd.serve_forever()
