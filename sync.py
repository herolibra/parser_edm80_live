import requests
import json

import collections
import sys
import errno
import multiprocessing
import pandas as pd
import hashlib
import entities
import datetime
from datetime import date, timedelta
import copy



def computeHashFromId(iot_id, offset, length):
    hash_object = hashlib.sha1(iot_id[offset:].encode('utf-8'))
    hex_dig = str(hash_object.hexdigest())
    hashed_id = ""
    if length > 0:
        hashed_id = iot_id[:offset] + hex_dig[:length]
    else:
        hashed_id = iot_id[:offset] + hex_dig
    return hashed_id


def rest_request(url, *args):
    """ Wrapper for REST requests. If only url is passed, GET request is executed, if additionally JSON (or any other payload) is passed, POST request is executed with payload from first optional argument. Other arguments are not evaluated. Kills script if connection fails for whatever reason or HTTP error response, returns valid response otherwise. """
    try:
        if not (args):
            response = requests.get(url)
        else:
            response = requests.post(url, args[0])

        if (response.status_code != 201):
            print(response.text)

    except requests.exceptions.Timeout:
        print("Error: connection timed out. You may want to try again.")
        sys.exit(errno.ETIMEDOUT)
    except requests.exceptions.TooManyRedirects:
        print("Error: connection: too many redirects. Bad URL?")
        sys.exit(errno.EINVAL)
    except requests.exceptions.RequestException as err:
        print("Error: connection error.")
        print(err)
        sys.exit(errno.ENODATA)

    #   if not (response):
    # print("\nError: HTTP error:", response, "\n")
    # print(response.text)
    # sys.exit(errno.EINVAL)

    return response


def PATCHRequest(url, data):
    """TODO: add docstring"""

    p = requests.patch(url, json=data)
    body = b""
    for chunk in p.iter_content(chunk_size=128):
        body += chunk
    body = body.decode("utf8")
    body = body.replace("\n", " ").replace("\r", "")
    print(body)
    print(p.status_code)


def patch_request(url, data):
    """TODO: add docstring"""

    p = requests.patch(url, json=data)
    body = b""
    for chunk in p.iter_content(chunk_size=128):
        body += chunk
    body = body.decode("utf8")
    body = body.replace("\n", " ").replace("\r", "")
    print(body)
    print(p.status_code)


def thing(url, thing_data):
    response = ""
    url_thing = url + "Things('" + thing_data['@iot.id'] + "')"
    response = rest_request(url_thing)
    if (response.status_code == 404):
        response = rest_request(url + "Things", json.dumps(thing_data))
        if (response.status_code == 201):
            print("Created Thing: ", url_thing)
    else:
        print("Thing already exists: ", url_thing)
    return response


def thing(url, thing_id, thing_type, lon, lat, hei):
    response = ""
    url_thing = url + "Things('" + thing_id + "')"
    response = rest_request(url_thing)
    if (response.status_code == 404):
        thing_data = copy.deepcopy(entities.default_entities[thing_type])
        thing_data['@iot.id'] = thing_id
        thing_data['name'] = "Crowdsensor:" + thing_type
        thing_data['Locations'] = [{
            'name': "",
            'description': 'A street with little traffic',
            'encodingType': 'application/vnd.geo+json',
            'location': {
                'type': 'Point',
                'coordinates': [float(lon), float(lat),float(hei)]# height also?
            },
            '@iot.id': 'geo:' + lat + ',' + lon + ',' + hei
        }]
        print(thing_data)

        response = rest_request(url + "Things", json.dumps(thing_data))
        print(response.text)
        if (response.status_code == 201):
            print("Created Thing: ", url_thing)
    else:
        if response.status_code == 200:
            print("Thing already exist: ", url_thing)
        else:
            print('error:', response.status_code)
    return response


def postObservation(url, result, rtime, ptime, ds_id, cali_time):
    ds_id_hash = computeHashFromId(ds_id, 8, 7)
    obs = copy.deepcopy(entities.default_entities["observation"])
    print("creating observations")
    obs['Datastream'] = {'@iot.id': ds_id_hash}
    obs['result'] = result
    obs['phenomenonTime'] = ptime
    obs['resultTime'] = rtime
    obs['@iot.id'] = computeHashFromId('saqn:ds:' + ds_id[8:] + ":" + rtime, 8, 0)
    obs['parameters'] = {}
    obs['parameters']['last calibration'] = cali_time # need this?
    response = rest_request(url + 'Observations', json.dumps(obs))
    print(response.text)
    print(obs['@iot.id'])


def merge_properties(prop1, prop2):
    prop_m = prop1.copy()
    prop_m.update(prop2)
    prop_m_o = collections.OrderedDict(sorted(prop_m.items(), key=lambda t: t[0]))

    seen = set()

    for key in prop_m_o.keys():
        value = tuple(prop_m_o[key])
        if value in seen:
            del prop_m_o[key]
        else:
            seen.add(value)

    prop = {}
    for key in prop_m_o.keys():
        prop[key] = prop_m_o[key]

    return prop

def datastream(url, ds_data):
    response = ""
    url_ds = url + "Datastreams('" + ds_data['@iot.id'] + "')"
    response = rest_request(url_ds)
    print(response.status_code)
    if (response.status_code == 404):
        response2 = rest_request(url + "Datastreams", json.dumps(ds_data))
        if (response2.status_code == 201):
            print("Created Datastream: ", url_ds)
        else:
            print("Error created ds", response2.status_code)


    else:
        print("Datastream already exists: ", url_ds)
        if (response.status_code == 200):
            data = json.loads(response.text)
            prop = data['properties']
            prop_v = prop['software_version']
            if (type(prop_v) == str):
                prop_v = {'software_version': prop_v}
            prop_m_v = merge_properties(prop_v, ds_data['properties']['software_version'])
            if (prop_m_v is not prop):
                prop_m = {}
                prop_m['properties'] = prop
                prop_m['properties']['software_version'] = prop_m_v
                patch_request(url_ds, prop_m)
                print(prop_m_v)
                print(prop_m)
    return response


def datastream(url, thing_id, ds_id, s_type, ds_type, sensor_id, software_version):
    response = ""
    ds_id_hash = computeHashFromId(ds_id, 8, 7)
    url_ds = url + "Datastreams('" + ds_id_hash + "')"
    response = rest_request(url_ds)
    print(response.status_code)
    if (response.status_code == 404):
        ds_data = copy.deepcopy(entities.default_entities[ds_type])
        ds_data['@iot.id'] = ds_id_hash
        ds_data['Thing']['@iot.id'] = thing_id
        ds_data['Sensor'] = copy.deepcopy(entities.default_entities[s_type])
        ds_data['Sensor']['@iot.id'] = sensor_id
        ds_data['properties']['software_version'] = software_version
        response2 = rest_request(url + "Datastreams", json.dumps(ds_data))
        if (response2.status_code == 201):
            print("Created Datastream: ", url_ds)
        else:
            print("Error created ds", response2.status_code)

    else:
        print("Datastream already exists: ", url_ds)
    return response


def requestLastphenomenTimeOfDatastream(url, id_ds):
    id_ds_hash = computeHashFromId(id_ds, 8, 7)
    rurl = url + "Datastreams('" + id_ds_hash + "')"
    response = rest_request(rurl)
    if (response.status_code == 200):
        lobs = json.loads(response.text)
        if (len(lobs['value']) > 0):
            ltimes = lobs['value'][0]['phenomenonTime'].split("/")[0]

            ltime = datetime.datetime.strptime(ltimes, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            ltime = datetime.datetime.strptime('1900-01-01T00:00:00.0Z', '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        ltime = datetime.datetime.strptime('1900-01-01T00:00:00.0Z', '%Y-%m-%dT%H:%M:%S.%fZ')

    return ltime