#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeBmLoadBalancerListenersRequest(Request):

	def __init__(self):
		Request.__init__(self, 'lb', 'qcloudcliV1', 'DescribeBmLoadBalancerListeners', 'lb.api.qcloud.com')

	def get_loadBalancerId(self):
		return self.get_params().get('loadBalancerId')

	def set_loadBalancerId(self, loadBalancerId):
		self.add_param('loadBalancerId', loadBalancerId)

	def get_listenerIds(self):
		return self.get_params().get('listenerIds')

	def set_listenerIds(self, listenerIds):
		self.add_param('listenerIds', listenerIds)

	def get_protocol(self):
		return self.get_params().get('protocol')

	def set_protocol(self, protocol):
		self.add_param('protocol', protocol)

	def get_loadBalancerPort(self):
		return self.get_params().get('loadBalancerPort')

	def set_loadBalancerPort(self, loadBalancerPort):
		self.add_param('loadBalancerPort', loadBalancerPort)

