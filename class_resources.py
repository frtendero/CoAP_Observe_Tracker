#!/usr/bin/env python
import threading
import time

import psutil
from coapthon.resources.resource import Resource

'''
    CoAP Resources  used in class.
'''

__author__ = 'Cristian Martin'


# Basic resource to show information
class BasicResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,
                                            observable=False)
        self.payload = "Hello Class! This is an example resource."
        self.resource_type = "urn:oma:lwm2m:oma:1"
        self.interface_type = "sensor"
        self.content_type = "text/plain"
        self._coap_server = coap_server

    # Add a new resource to the server with the URI received as payload
    def render_POST(self, request):
        self._coap_server.add_resource(request.payload, BasicResource(coap_server=self._coap_server))
        return self

    # Update the resources
    def render_PUT(self, request):
        self.payload = request.payload
        return self

    # Return the status of the resource
    def render_GET(self, request):
        return self

    # Remove the resource
    def render_DELETE(self, request):
        return True


# Observable resource
class ObservableResource(Resource):
    def __init__(self, name="ObservableResource", coap_server=None):
        super(ObservableResource, self).__init__(name, coap_server, visible=True,
                                                 observable=True, allow_children=False)
        self.resource_type = "urn:oma:lwm2m:ext:3333"
        self.interface_type = "sensor"
        self.content_type = "text/plain"
        self.payload = str(time.ctime())
        self.max_age = 20
        self.update(True)

    # Return the status of the resource
    def render_GET(self, request):
        self.payload = str(time.ctime())
        return self

    # Add a new resource to the server with the URI received as payload
    def render_POST(self, request):
        self._coap_server.add_resource(request.payload, ObservableResource(coap_server=self._coap_server))
        return self

    # Function to notify the observers when timeout expires
    def update(self, first=False):
        if not self._coap_server.stopped.isSet():

            # Create a timer thread to notify
            timer = threading.Timer(self.max_age, self.update)
            timer.setDaemon(True)
            timer.start()

            if not first and self._coap_server is not None:
                self._coap_server.notify(self)
                self.observe_count += 1

    # Remove the resource
    def render_DELETE(self, request):
        return True


class CPUResource(Resource):
    def __init__(self, name="CPUResource", coap_server=None):
        super(CPUResource, self).__init__(name, coap_server, visible=True,
                                          observable=False)
        # self.payload = "Hello Class! This is an example resource."
        self.resource_type = "cpu"
        self.interface_type = "sensor"
        self.content_type = "text/plain"
        self._coap_server = coap_server

        # Return the status of the resource

    def render_GET(self, request):
        self.payload = str(psutil.cpu_percent())
        return self


class MemResource(Resource):
    def __init__(self, name="MemResource", coap_server=None):
        super(MemResource, self).__init__(name, coap_server, visible=True,
                                          observable=False)
        # self.payload = "Hello Class! This is an example resource."
        self.resource_type = "memory"
        self.interface_type = "sensor"
        self.content_type = "text/plain"
        self._coap_server = coap_server

        # Return the status of the resource

    def render_GET(self, request):
        self.payload = str(psutil.virtual_memory().percent)
        # self.payload = str(getattr(psutil, self.operation))
        return self

    # Add a new resource to the server with the URI received as payload
    def render_POST(self, request):
        self._coap_server.add_resource(request.payload, MemResource(coap_server=self._coap_server),
                                       operation=request.payload)
        return self


class PsutilResource(Resource):
    def __init__(self, name="PsutilResource", coap_server=None):
        super(PsutilResource, self).__init__(name, coap_server, visible=True,
                                             observable=False)
        # self.payload = "Hello Class! This is an example resource."
        self.resource_type = "memory"
        self.interface_type = "psutil"
        self.content_type = "text/plain"
        self._coap_server = coap_server

    # Return the status of the resource
    def render_GET(self, request):
        self.payload = str(getattr(psutil, self.operation))
        return self

    # Add a new resource to the server with the URI received as payload
    def render_POST(self, request):
        self._coap_server.add_resource(request.payload,
                                       MemResource(coap_server=self._coap_server, operation=request.payload))
        return self

    # Update the resources
    def render_PUT(self, request):
        self.payload = request.payload
        return self

    # Remove the resource
    def render_DELETE(self, request):
        return True