#!/usr/bin/env python
from __future__ import print_function  # Print function in Python 2 and 3

import argparse
import sys
from coapthon.server.coap import CoAP
from class_resources import BasicResource, ObservableResource, CPUResource, MemResource, PsutilResource
"""
    Server CoAP for observe tracker
"""

__author__ = 'Fco R Tendero'

def ignore_listen_exception(exception, server):
    type = exception.__class__.__name__
    print(type)
    return True

def main(args):
    # IP and Port configuration
    ip = "0.0.0.0"
    port = 5683

    # Create the CoAP server
    server = CoAP(
        (ip, port),
        multicast=args.multicast,
        cb_ignore_listen_exception=ignore_listen_exception
    )

    # Register resources
    server.add_resource('info/', BasicResource(coap_server=server))
    server.add_resource('time/', ObservableResource(coap_server=server))
    server.add_resource('cpu/', CPUResource(coap_server=server))
    server.add_resource('memory/', MemResource(coap_server=server))
    server.add_resource('psutil/', PsutilResource(coap_server=server))

    try:
        # Start listening for incoming requests
        server.listen()

    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")
        sys.exit(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-M', '--multicast',
        help="Whether IP is multicast or not, default: True",
        type=bool,
        default=True
    )

    main(parser.parse_args())