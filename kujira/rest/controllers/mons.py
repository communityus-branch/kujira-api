"""API Controller for monitor objects.
Methods mapped:
- api/v2/clusters/fsid/mon
- api/v2/clusters/fsid/mon/name
- api/v2/clusters/fsid/mon/name/status"""

import logging

from kujira.blueprints import MON_BP
from kujira.rest.lib.request_methods import send_get
from kujira.rest.lib.parsing_methods import parse_and_return


@MON_BP.route("/<fsid>")
def all_monitors(fsid):
    response = send_get('cluster/' + fsid + '/mon')
    if response.status_code != 422:
        response = parse_and_return(mons_parse, response)
    return response


@MON_BP.route("/<fsid>/<name>")
def monitor(fsid, name):
    response = send_get('cluster/' + fsid + '/mon/' + name)
    if response.status_code != 422:
        response = parse_and_return(mons_parse, response)
    return response


def mons_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        logging.warning(e.message)
    root = {'data': []}
    attributes = {}
    if new_dict:
        data = {'type': 'mons'}
        for key, value in new_dict.iteritems():
            key = key.replace('_', '-')
            if str(key) == 'name':
                data['id'] = str(value)
                attributes[key] = value
            else:
                attributes[key] = value
        data['attributes'] = attributes
    root['data'].append(data)
    return root