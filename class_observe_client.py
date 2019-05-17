#!/usr/bin/env python
from __future__ import print_function  # Print function in Python 2 and 3

from time import sleep

from coapthon import defines
from coapthon.client.helperclient import HelperClient
import logging

import argparse

'''
    CoAP Client for Observe Tracker
'''

__author__ = 'Fco R Tendero'

# Observe callback receive function
def observe_callback(response):
    print(response.payload)

def main(args):
    logging.disable(logging.DEBUG)  # Disable DEBUG logging

    observables = [] # global list where observed paths are saved

    while (True):
        sleep(5)

        client = HelperClient(server=(args.host, args.port))
        response = client.discover()

        try:
            resources_list = response.payload.split(",")
            observable_paths = []

            for resource in resources_list:
                elems = str(resource).split(";")

                if "obs" in elems:
                    observable_path = elems[0]
                    observable_path = observable_path.translate(
                        str.maketrans({'<': '', '>': ''})
                    )

                    # only append if path it has not been observed yet
                    if observable_path not in observables:
                        observable_paths.append(observable_path)
                        observables.extend(observable_paths)
                        #client.observe(observable_path, observe_callback)

            # for path in observable_paths:
            for path in observables:
                client.observe(path, observe_callback)

        except (AttributeError) as e:
            print("Attribute Error")
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host',
        help="IP direction of the CoAP server, default: MULTICAST",
        default=defines.ALL_COAP_NODES
    )
    parser.add_argument(
        '-p', '--port',
        help="Port where CoAP server is listening, default: 5683",
        default=5683
    )
    main(parser.parse_args())