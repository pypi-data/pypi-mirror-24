#
# Copyright (c) 2007 Jared Crapo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""
tomcatmanager.models
~~~~~~~~~~~~~~~

This module contains the data objects created by and used by tomcatmanager.
"""

import requests
from requests.structures import LookupDict


class TomcatError(Exception):
	pass


class TomcatManagerResponse:
	"""The response for a Tomcat Manager command"""    

	def __init__(self, response=None):
		self._response = response
		self._status_code = None
		self._status_message = None
		self._result = None

	@property
	def response(self):
		"""contains the requsts.Response object from the request"""
		return self._response

	@response.setter
	def response(self, response):
		self._response = response
		# parse the text to get the status code and results
		if response.text:
			try:
				statusline = response.text.splitlines()[0]
				self.status_code = statusline.split(' ', 1)[0]
				self.status_message = statusline.split(' ',1)[1][2:]
				self.result = response.text.splitlines()[1:]
			except IndexError:
				pass

	@property
	def status_code(self):
		"""status of the tomcat manager command
		
		the codes can be found in tomcatmanager.codes and they are
		
		tomcatmanager.codes.ok
		tomcatmanager.codes.fail
		"""
		return self._status_code

	@status_code.setter
	def status_code(self, value):
		self._status_code = value

	@property
	def status_message(self):
		return self._status_message
	
	@status_message.setter
	def status_message(self, value):
		self._status_message = value

	@property
	def result(self):
		return self._result

	@result.setter
	def result(self, value):
		self._result = value

	@property
	def ok(self):
		"""returns True if there is a response, and if it completed ok"""
		return all([
				self.response != None,
				self.response.status_code == requests.codes.ok,
				self.status_code == codes.ok,
			 ])

	def raise_for_status(self):
		"""raise exceptions if status is not ok
		
		first calls requests.Response.raise_for_status() which will
		raise exceptions if a 4xx or 5xx response is received from the server
		
		If that doesn't raise anything, then check if we have an "FAIL" response
		from the first line of text back from the Tomcat Manager web app, and
		raise an TomcatError if necessary
		
		stole idea from requests package
		"""
		self.response.raise_for_status()
		if self.status_code != codes.ok:
			raise TomcatError(self.status_message)


class ServerInfo(dict):
	"""Discrete data about the tomcat server"""

	def __init__(self, result=None):
		"""result is the plain text from the server"""
		self._tomcat_version = None
		self._os_name = None
		self._os_version= None
		self._os_architecture = None
		self._jvm_version = None
		self._jvm_vendor = None
		self._parse(result)

	def _parse(self, result):
		"""parse up a list of lines from the server"""
		if result:
			for line in result:
				key, value = line.rstrip().split(':',1)
				self[key] = value.lstrip()
			
			self._tomcat_version = self['Tomcat Version']
			self._os_name = self['OS Name']
			self._os_version= self['OS Version']
			self._os_architecture = self['OS Architecture']
			self._jvm_version = self['JVM Version']
			self._jvm_vendor = self['JVM Vendor']
		
	@property
	def tomcat_version(self):
		"""the tomcat version string"""
		return self._tomcat_version

	@property
	def os_name(self):
		"""the operating system name"""
		return self._os_name

	@property
	def os_version(self):
		"""the operating system version"""
		return self._os_version

	@property
	def os_architecture(self):
		"""the operating system architecture"""
		return self._os_architecture

	@property
	def jvm_version(self):
		"""the java virtual machine version string"""
		return self._jvm_version

	@property
	def jvm_vendor(self):
		"""the java virtual machine vendor"""
		return self._jvm_vendor

###
#
# build status codes
#
###
_codes = {

	# 'sent from tomcat': 'friendly name'
	'OK': 'ok',
	'FAIL': 'fail',
}

codes = LookupDict(name='status_codes')

for code, title in _codes.items():
	setattr(codes, title, code)
