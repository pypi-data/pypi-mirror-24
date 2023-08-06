#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class StartDomainRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cns', 'qcloudcliV1', 'StartDomain', 'cns.api.qcloud.com')

	def get_domain(self):
		return self.get_params().get('domain')

	def set_domain(self, domain):
		self.add_param('domain', domain)


