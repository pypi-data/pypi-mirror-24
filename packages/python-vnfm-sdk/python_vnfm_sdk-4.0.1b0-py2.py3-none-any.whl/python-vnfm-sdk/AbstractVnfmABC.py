# Copyright (c) 2015 Fraunhofer FOKUS. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import ConfigParser
import json
import logging
import threading
import uuid

import operator

from exceptions import PyVnfmSdkException

import abc
import os
import pika
from utils.Utilities import get_map

__author__ = 'lto'

log = logging.getLogger("org.openbaton.python.vnfm.sdk") \
 \
    # TODO improve this
ENDPOINT_TYPES = ["RABBIT", "REST"]


class ManagerEndpoint(object):
    def __init__(self, type, endpoint, endpoint_type, description=None, enabled=True, active=True):
        self.type = type
        self.endpoint = endpoint
        self.endpoint_type = endpoint_type
        self.description = description
        self.enabled = enabled
        self.active = active

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    pass


def check_endpoint_type(endpoint_type):
    if endpoint_type not in ENDPOINT_TYPES:
        raise PyVnfmSdkException("The endpoint type must be in %s" % ENDPOINT_TYPES)


def get_nfv_message(action, vnfr, vnfc_instance=None, vnfr_dependency=None, exception=None, vim_instances=None,
                    keys=None, user_data=None):
    if action == "INSTANTIATE":
        return {"action": action, "virtualNetworkFunctionRecord": vnfr}
    if action == "ERROR":
        return {"action": action, "virtualNetworkFunctionRecord": vnfr, "nsrId": vnfr.get("parent_ns_id"),
                "exception": exception}
    if action == "MODIFY":
        return ""
    if action == "GRANT_OPERATION":
        return {"action": action, "virtualNetworkFunctionRecord": vnfr}
    if action == "ALLOCATE_RESOURCES":
        if user_data is None or user_data == "":  user_data = "none"
        return {
            "action": action,
            "virtualNetworkFunctionRecord": vnfr,
            "vimInstances": vim_instances,
            "keyPairs": keys,
            "userdata": user_data
        }
    if action == "RELEASE_RESOURCES":
        return {"action": action, "virtualNetworkFunctionRecord": vnfr}
    if action == "START":
        return {"action": action, "virtualNetworkFunctionRecord": vnfr, "vnfcInstance": vnfc_instance,
                "vnfrDependency": vnfr_dependency}
    pass


class AbstractVnfm(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def instantiate(self, vnf_record, scripts, vim_instances):
        pass

    @abc.abstractmethod
    def query(self):
        """This operation allows retrieving VNF instance state and attributes."""
        pass

    @abc.abstractmethod
    def scale(self, scale_out, vnf_record, vnf_component, scripts, dependency):
        """This operation allows scaling (out / in, up / down) a VNF instance."""
        pass

    @abc.abstractmethod
    def checkInstantiationFeasibility(self):
        """This operation allows verifying if the VNF instantiation is possible."""
        pass

    @abc.abstractmethod
    def heal(self, vnf_record, vnf_instance, cause):
        pass

    @abc.abstractmethod
    def updateSoftware(self):
        """This operation allows applying a minor / limited software update(e.g.patch) to a VNF instance."""
        pass

    @abc.abstractmethod
    def modify(self, vnf_record, dependency):
        """This  operation allows making structural changes (e.g.configuration, topology, behavior, redundancy model) to a VNF instance."""
        pass

    @abc.abstractmethod
    def upgradeSoftware(self):
        """This operation allows deploying a new software release to a VNF instance."""
        pass

    @abc.abstractmethod
    def terminate(self, vnf_record):
        """This operation allows terminating gracefully or forcefully a previously created VNF instance."""
        pass

    @abc.abstractmethod
    def notifyChange(self):
        """This operation allows providing notifications on state changes of a VNF instance, related to the VNF Lifecycle."""
        pass

    @abc.abstractmethod
    def start(self, vnf_record):
        """

        :param vnf_record:
        :return:
        """
        pass

    @abc.abstractmethod
    def stop(self, vnf_record):
        """

            :param vnf_record:
            :return:
            """
        pass

    @abc.abstractmethod
    def startVNFCInstance(self, vnf_record, vnfc_instance):
        """

        :param vnf_record:
        :param vnfc_instance:
        :return:
        """
        pass

    @abc.abstractmethod
    def stopVNFCInstance(self, vnf_record, vnfc_instance):
        """

        :param vnf_record:
        :param vnfc_instance:
        :return:
        """
        pass

    @abc.abstractmethod
    def handleError(self, vnf_record):
        """

        :param vnf_record
        :return:
        """
        pass

    # TODO to be DOUBLE checked!
    @staticmethod
    def create_vnf_record(vnfd, flavor_key, vlrs, extension):

        log.debug("Requires is: %s" % vnfd.get("requires"))
        log.debug("Provides is: %s" % vnfd.get("provides"))

        vnfr = dict(lifecycle_event_history=[], parent_ns_id=extension.get("nsr-id"), name=vnfd.get("name"),
                    type=vnfd.get("type"), requires=vnfd.get("requires"), provides=dict(),
                    endpoint=vnfd.get("endpoint"),
                    packageId=vnfd.get("vnfPackageLocation"), monitoring_parameter=vnfd.get("monitoring_parameter"),
                    auto_scale_policy=vnfd.get("auto_scale_policy"), cyclicDependency=vnfd.get("cyclicDependency"),
                    configurations=vnfd.get("configurations"), vdu=vnfd.get("vdu"), version=vnfd.get("version"),
                    connection_point=vnfd.get("connection_point"), deployment_flavour_key=flavor_key,
                    vnf_address=vnfd.get("vnf_address"), status="NULL", descriptor_reference=vnfd.get("id"),
                    lifecycle_event=vnfd.get("lifecycle_event"), virtual_link=vnfd.get("virtual_link"))
        if vnfr.get("requires") is not None:
            if vnfr.get("requires").get("configurationParameters") is None:
                vnfr["requires"]["configurationParameters"] = []
        if vnfr.get("provides") is not None:
            if vnfr.get("provides").get("configurationParameters") is None:
                vnfr["provides"]["configurationParameters"] = []

        # for (VirtualDeploymentUnit virtualDeploymentUnit: vnfd.getVdu()) {
        # for (VimInstance vi: vimInstances.get(virtualDeploymentUnit.getId())) {
        # for (String name: virtualDeploymentUnit.getVimInstanceName()) {
        # if (name.equals(vi.getName()))
        # {
        # if (!existsDeploymentFlavor(
        #     virtualNetworkFunctionRecord.getDeployment_flavour_key(), vi)) {
        #     throw
        # new
        # BadFormatException(
        #     "no key "
        #     + virtualNetworkFunctionRecord.getDeployment_flavour_key()
        #     + " found in vim instance: "
        #     + vi);
        # }
        # }
        # }
        # }
        # }

        for vlr in vlrs:
            for internal_vlr in vnfr["virtual_link"]:
                if vlr.get("name") == internal_vlr.get("name"):
                    internal_vlr["exId"] = vlr.get("extId")

        return vnfr

    def on_message(self, body):
        """
        This message is in charge of dispaching the message to the right method
        :param body:
        :return:
        """
        msg = json.loads(body)

        action = msg.get("action")
        log.debug("Action is %s" % action)
        vnfr = {}
        if action == "INSTANTIATE":
            extension = msg.get("extension")
            keys = msg.get("keys")
            log.debug("Got these keys: %s" % keys)
            vim_instances = msg.get("vimInstances")
            vnfd = msg.get("vnfd")
            vnf_package = msg.get("vnfPackage")
            vlrs = msg.get("vlrs")
            vnfdf = msg.get("vnfdf")
            if vnf_package.get("scriptsLink") is None:
                scripts = vnf_package.get("scripts")
            else:
                scripts = vnf_package.get("scriptsLink")
            vnf_record = AbstractVnfm.create_vnf_record(vnfd, vnfdf.get("flavour_key"), vlrs, extension)

            grant_operation = self.grant_operation(vnf_record)
            vnf_record = grant_operation["virtualNetworkFunctionRecord"]
            vim_instances = grant_operation["vduVim"]

            if bool(self._map.get("allocate", True)):
                vnf_record = self.allocate_resources(vnf_record, vim_instances, keys).get(
                    "virtualNetworkFunctionRecord")
            vnfr = self.instantiate(vnf_record=vnf_record, scripts=scripts, vim_instances=vim_instances)

        if action == "MODIFY":
            vnfr = self.modify(vnf_record=msg.get("vnfr"), dependency=msg.get("vnfrd"))
        if action == "START":
            vnfr = self.start(vnf_record=msg.get("virtualNetworkFunctionRecord"))
        if action == "ERROR":
            vnfr = self.handleError(vnf_record=msg.get("vnfr"))
        if action == "RELEASE_RESOURCES":
            vnfr = self.terminate(vnf_record=msg.get("vnfr"))

        if len(vnfr) == 0:
            raise PyVnfmSdkException("Unknown action!")
        nfv_message = get_nfv_message(action, vnfr);
        log.debug("answer is: %s" % nfv_message)
        return nfv_message

    def on_request(self, ch, method, props, body):
        log.info("Waiting for actions")
        response = self.on_message(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        if response.get("action") == "INSTANTIATE":
            ch.basic_publish(exchange='',
                             routing_key="vnfm.nfvo.actions.reply",
                             properties=pika.BasicProperties(content_type='text/plain'),
                             body=json.dumps(response))
        else:
            ch.basic_publish(exchange='',
                             routing_key="vnfm.nfvo.actions",
                             properties=pika.BasicProperties(content_type='text/plain'),
                             body=json.dumps(response))

        log.info("Answer sent")

    def thread_function(self, ch, method, properties, body):
        threading.Thread(target=self.on_request, args=(ch, method, properties, body)).start()

    def __init__(self, type):
        log.addHandler(logging.NullHandler())
        self.type = type
        # self.dispatcher = {
        #     "INSTANTIATE": self.instantiate,
        #     "GRANT_OPERATION": None,
        #     "ALLOCATE_RESOURCES": None,
        #     "SCALE_IN": self.scale,
        #     "SCALE_OUT": self.scale,
        #     "SCALING": None,
        #     "ERROR": self.handleError,
        #     "RELEASE_RESOURCES": self.terminate,
        #     "MODIFY": self.modify,
        #     "HEAL": self.heal,
        #     "UPDATEVNFR": self.upgradeSoftware,
        #     "UPDATE": self.updateSoftware,
        #     "SCALED": None,
        #     "CONFIGURE": self.modify,
        #     "START": self.start,
        #     "STOP": self.stop
        # }
        config_file_name = "/etc/openbaton/%s/conf.ini" % self.type  # understand if it works
        log.debug("Config file location: %s" % config_file_name)
        config = ConfigParser.ConfigParser()
        config.read(config_file_name)  # read config file
        self._map = get_map(section='vnfm', config=config)  # get the data from map
        log.debug("Map is: %s" % self._map)
        logging_dir = self._map.get('log_path')

        if not os.path.exists(logging_dir):
            os.makedirs(logging_dir)

        file_handler = logging.FileHandler("{0}/{1}-vnfm.log".format(logging_dir, type))
        file_handler.setLevel(level=50)
        log.addHandler(file_handler)

        username = self._map.get("username")
        password = self._map.get("password")
        heartbeat = self._map.get("heartbeat")
        exchange_name = self._map.get("exchange")
        queuedel = True
        if not heartbeat:
            heartbeat = '60'
        if not exchange_name:
            exchange_name = 'openbaton-exchange'

        rabbit_credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._map.get("broker_ip"), credentials=rabbit_credentials,
                                      heartbeat_interval=int(heartbeat)))

        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.exchange_declare(exchange=exchange_name, type="topic", durable=True)

        self.channel.queue_declare(queue='vnfm.nfvo.actions', auto_delete=queuedel, durable=True)
        self.channel.queue_declare(queue='vnfm.nfvo.actions.reply', auto_delete=queuedel, durable=True)
        self.channel.queue_declare(queue='nfvo.%s.actions' % self.type, auto_delete=queuedel, durable=True)

    def run(self):

        self.register(self._map, self.channel, self.type)

        self.channel.basic_consume(self.thread_function, queue='nfvo.%s.actions' % self.type)

        try:
            log.info("Waiting for actions")
            self.channel.start_consuming()
        except Exception:
            self.unregister(self._map, self.channel, self.type)

    def register(self, _map, channel, type):
        # Registration
        log.info("Registering VNFM of type %s" % type)
        endpoint_type = _map.get("endpoint_type")
        log.debug("Got endpoint type: %s" % endpoint_type)
        check_endpoint_type(endpoint_type)
        manager_endpoint = ManagerEndpoint(type=type, endpoint="nfvo.%s.actions" % type, endpoint_type=endpoint_type,
                                           description="First python vnfm")
        log.debug("Sending endpoint type: " + manager_endpoint.toJSON())
        channel.basic_publish(exchange='', routing_key='nfvo.vnfm.register',
                              properties=pika.BasicProperties(content_type='text/plain'),
                              body=manager_endpoint.toJSON())

    def unregister(self, _map, channel, type):
        # UnRegistration
        log.info("Unregistering VNFM of type %s" % type)
        endpoint_type = _map.get("endpoint_type")
        check_endpoint_type(endpoint_type)
        manager_endpoint = ManagerEndpoint(type=type, endpoint="nfvo.%s.actions" % type, endpoint_type=endpoint_type,
                                           description="First python vnfm")
        log.debug("Sending endpoint type: " + manager_endpoint.toJSON())
        channel.basic_publish(exchange='', routing_key='nfvo.vnfm.unregister',
                              properties=pika.BasicProperties(content_type='text/plain'),
                              body=manager_endpoint.toJSON())

    def grant_operation(self, vnf_record):
        nfv_message = get_nfv_message("GRANT_OPERATION", vnf_record)
        log.info("Executing GRANT_OPERATION")
        result = self.exec_rpc_call(json.dumps(nfv_message))
        log.debug("grant_allowed: %s" % result.get("grantAllowed"))
        log.debug("vdu_vims: %s" % result.get("vduVim").keys())
        log.debug("vnf_record: %s" % result.get("virtualNetworkFunctionRecord").get("name"))

        return result

    def allocate_resources(self, vnf_record, vim_instances, keys):
        user_data = self.get_user_data()
        nfv_message = get_nfv_message(action="ALLOCATE_RESOURCES", vnfr=vnf_record, vim_instances=vim_instances,
                                      user_data=user_data, keys=keys)
        log.debug("Executing ALLOCATE_RESOURCES")
        result = self.exec_rpc_call(json.dumps(nfv_message))
        log.debug("vnf_record: %s" % result.get("virtualNetworkFunctionRecord").get("name"))
        return result

    def exec_rpc_call(self, nfv_message):
        result = self.channel.queue_declare(exclusive=True)
        callback_queue = result.method.queue
        response = {}
        self.channel.basic_consume(lambda res: operator.setitem(response, "result", res), no_ack=True,
                                   queue=callback_queue)
        corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=nfv_message)
        while len(response) == 0:
            self.connection.process_data_events()
        return json.loads(response["result"])

    def get_user_data(self):
        userdata_path = self._map.get("userdata_path", "/etc/openbaton/%s/userdata.sh" % self.type)
        if os.path.isfile(userdata_path):
            with open(userdata_path, "r") as f:
                return f.read()
        else:
            return None
