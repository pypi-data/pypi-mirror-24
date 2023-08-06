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

import requests
import collections

from .models import codes, TomcatManagerResponse, ServerInfo


class TomcatManager:
	"""A wrapper around the tomcat manager web application
	
	"""
	
	@classmethod
	def _is_stream(self, obj):
		"""return true if this is a stream type object"""
		return all([
			hasattr(obj, '__iter__'),
			not isinstance(obj, (str, bytes, list, tuple, collections.Mapping))
		])
		
	def __init__(self, url=None, userid=None, password=None):
		self._url = url
		self._userid = userid
		self._password = password

	def _get(self, cmd, payload=None):
		"""make an HTTP get request to the tomcat manager web app
		
		returns a TomcatManagerResponse object
		"""
		url = self._url + '/text/' + cmd
		r = TomcatManagerResponse()
		r.response = requests.get(
				url,
				auth=(self._userid, self._password),
				params=payload
				)
		return r

	###
	#
	# convenience and utility methods
	#
	###
	@property
	def is_connected(self):
		"""try and connect to the tomcat server using url and authentication
		
		returns true if successful, false otherwise
		"""
		try:
			r = self._get('list')
			return r.ok
		except:
			return False

	###
	#
	# the info commands, i.e. commands that don't really do anything, they
	# just return some information from the server
	#
	###
	def list(self):
		"""list of all applications currently installed
		
			tm = TomcatManager(url)
			tmr = tm.list()
			apps = tmr.apps
		
		returns an instance of TomcatManagerResponse with an additional apps
		attribute
		
		apps is a list of tuples: (path, status, sessions, directory)
		
		path - the relative URL where this app is deployed on the server
		status - whether the app is running or not
		sessions - number of currently active sessions
		directory - the directory on the server where this app resides		
		"""
		tmr = self._get('list')
		apps = []
		for line in tmr.result:
			apps.append(line.rstrip().split(":"))		
		tmr.apps = apps
		return tmr
		
	def server_info(self):
		"""get information about the server
		
			tm = TomcatManager(url)
			r = tm.serverinfo()
			r.server_info['OS Name']
			
		returns an instance of TomcatManagerResponse with an additional server_info
		attribute. The server_info attribute is a dictionary of items about the server
		"""
		r = self._get('serverinfo')
		r.server_info = ServerInfo(r.result)
		return r

	def status_xml(self):
		"""get server status information in XML format
		
		we have lots of status stuff, so this method is named status_xml to try
		and reduce confusion with status_code and status_message
		
		Uses the '/manager/status/all?XML=true' command
		
		Tomcat 8 doesn't include application info in the XML, even though the docs
		say it does.
		
			tm = TomcatManager(url)
			tmr = tm.status_xml()
			x = tmr.result
			y = tmr.status_xml
		
		returns an instance of TomcatManagerResponse with the status xml document in
		the result attribute and in the status_xml attribute
		"""
		# this command isn't in the /manager/text url space, so we can't use _get()
		url = self._url + '/status/all'
		tmr = TomcatManagerResponse()
		tmr.response = requests.get(
				url,
				auth=(self._userid, self._password),
				params={'XML': 'true'}
				)
		tmr.result = tmr.response.text.splitlines()
		tmr.status_xml = tmr.result

		# we have to force a status_code and a status_message
		# because the server doesn't return them
		if tmr.response.status_code == requests.codes.ok:
			tmr.status_code = codes.ok
			tmr.status_message = codes.ok
		else:
			tmr.status_code = codes.fail
			tmr.status_message = codes.fail
		return tmr

	def vm_info(self):
		"""get diagnostic information about the JVM
				
			tm = TomcatManager(url)
			tmr = tm.vm_info()
			x = tmr.result
			y = tmr.vm_info
		
		returns an instance of TomcatManagerResponse with the virtual machine info in
		the result attribute and in the vm_info attribute
		"""
		tmr = self._get('vminfo')
		tmr.vm_info = tmr.result
		return tmr

	def ssl_connector_ciphers(self):
		"""get SSL/TLS ciphers configured for each connector

			tm = TomcatManager(url)
			tmr = tm.ssl_connector_ciphers()
			x = tmr.result
			y = tmr.ssl_connector_info
		
		returns an instance of TomcatManagerResponse with the ssl cipher info in the
		result attribute and in the ssl_connector_info attribute
		"""
		tmr = self._get('sslConnectorCiphers')
		tmr.ssl_connector_ciphers = tmr.result
		return tmr

	def thread_dump(self):
		"""get a jvm thread dump

			tm = TomcatManager(url)
			tmr = tm.thread_dump()
			x = tmr.result
			y = tmr.thread_dump
		
		returns an instance of TomcatManagerResponse with the thread dump in the result
		attribute and in the thread_dump attribute
		"""
		tmr = self._get('threaddump')
		tmr.thread_dump = tmr.result
		return tmr

	def resources(self, type=None):
		"""list the global JNDI resources available for use in resource links for context config files
		
			tm = TomcatManager(url)
			r = tm.resources()
			resources = r.resources
		
		pass the optional fully qualified java class name of the resource type you are
		interested in. For example, you might pass javax.sql.DataSource to acquire
		the names of all available JDBC data sources
		
		returns an instance of TomcatManagerResponse with an additional resources
		attribute
		
		resources is a list of tuples: (resource, class)
		"""
		if type:
			r = self._get('resources', {'type': str(type)})
		else:
			r = self._get('resources')

		resources = {}
		for line in r.result:
			resource, classname = line.rstrip().split(':',1)
			if resource[:7] != codes.fail + ' - ':
				resources[resource] = classname.lstrip()
		r.resources = resources
		return r


	def find_leakers(self):
		"""list apps that leak memory
		
		This command triggers a full garbage collection on the server. Use with
		extreme caution on production systems.
		
		Explicity triggering a full garbage collection from code is documented to be
		unreliable. Furthermore, depending on the jvm, there are options to disable
		explicit GC triggering, like ```-XX:+DisableExplicitGC```. If you want to make
		sure this command triggered a full GC, you will have to verify using something
		like GC logging or JConsole.
		
			tm = TomcatManager(url)
			tmr = tm.find_leaks()
			leakers = tmr.leakers

		returns an instance of TomcatManagerResponse with an additional leakers
		attribute. If leakers in an empty list, then no leaking apps were found.
		
		The tomcat manager documentation says that it can return duplicates in this
		list if the app has been reloaded and was leaking both before and after the
		reload. The list returned by the leakers attribute will have no duplicates in
		it
		
		"""
		tmr = self._get('findleaks', {'statusLine': 'true'})
		leakers = []
		for line in tmr.result:
			leakers.append(line.rstrip())
		# remove duplicates by changing it to a set, then back to a list		
		tmr.leakers = list(set(leakers))
		return tmr

	def sessions(self, path, version=None):
		"""return a list of the sessions in an application at a given path
	
			tm = TomcatManager(url)
			tmr = tm.sessions('/manager')
			x = tmr.result
			y = tmr.sessions
		
		returns an instance of TomcatManagerResponse with the session summary in the
		result attribute and in the sessions attribute
		"""
		params = {}
		params['path'] = path
		if version:
			params['version'] = version
		r = self._get('sessions', params)
		if r.ok: r.sessions = r.result
		return r

	###
	#
	# the action commands, i.e. commands that actually effect some change on
	# the server
	#
	###
	def expire(self, path, version=None, idle=None):
		"""expire sessions idle for longer than idle minutes

			tm = TomcatManager(url)
			tmr = tm.sessions('/manager')
			x = tmr.result
			y = tmr.sessions
			
		Arguments:
		path     the path to the app on the server whose sessions you want to expire
		idle     sessions idle for more than this number of minutes will be expired
		         use idle=0 to expire all sessions
		
		returns an instance of TomcatManagerResponse with the session summary in the
		result attribute and in the sessions attribute
		"""
		params = {}
		params['path'] = path
		if version:
			params['version'] = version
		if idle:
			params['idle'] = idle		
		r = self._get('expire', params)
		if r.ok: r.sessions = r.result
		return r
	
	def start(self, path, version=None):
		"""start the application at a given path
	
			tm = TomcatManager(url)
			tmr = tm.start('/someapp')
			tmr.raise_on_status()
		
		returns an instance of TomcatManagerResponse
		"""
		params = {}
		params['path'] = path
		if version:
			params['version'] = version
		return self._get('start', params)

	def stop(self, path, version=None):
		"""stop the application at a given path
	
			tm = TomcatManager(url)
			tmr = tm.stop('/someapp')
			tmr.raise_on_status()
		
		returns an instance of TomcatManagerResponse
		"""
		params = {}
		params['path'] = path
		if version:
			params['version'] = version
		return self._get('stop', params)

	def reload(self, path, version=None):
		"""reload the application at a given path
	
			tm = TomcatManager(url)
			tmr = tm.reload('/someapp')
			tmr.raise_on_status()
		
		returns an instance of TomcatManagerResponse
		"""
		params = {}
		params['path'] = path
		if version:
			params['version'] = version
		return self._get('reload', params)

	def deploy(self, path, localwar=None, serverwar=None, version=None, update=False):
		"""Deploy applications to the tomcat server
		
		Specify either localwar or serverwar, but not both. localwar reads a war file
		from the local filesystem and sends it to the tomcat server to deploy.
		serverwar deploys a file available on the server file system.
		
		:param path: The path on the server to deploy this war to, i.e. /sampleapp
		:param localwar: (optional) The path (specified using your particular
			operating system convention) to a war file on the local file system. This
			will be sent to the server for deployment.
		:param serverwar: (optional) The java-style path (use slashes not backslashes) to
			the war file on the server. Don't include ``file:`` at the beginning.
		:param version: (optional) For tomcat parallel deployments, the version to use
			for this version of the app
		:param update: (optional) Whether to undeploy the existing path
			first (default False)
		:return: :class:`TomcatManagerResponse <TomcatManagerResponse>` object
		:rtype: tomcatmanager.TomcatManagerResponse		
		"""
		params = {}
		params['path'] = path
		if update:
			params['update'] = 'true'
		if version:
			params['version'] = version

		if localwar and serverwar:
			raise ValueError('can not deploy localwar and serverwar at the same time')
		elif localwar:
			# PUT a local stream
			url = self._url + '/text/deploy'
			if self._is_stream(localwar):
				warobj = localwar
			else:
				warobj = open(localwar, 'rb')	

			r = TomcatManagerResponse()
			r.response = requests.put(
					url,
					auth=(self._userid, self._password),
					params=params,
					data=warobj,
					)
		elif serverwar:
			params['war'] = serverwar
			r = self._get('deploy', params)
		else:
			r = self._get('deploy', params)

		return r

	def undeploy(self, path, version=None):
		"""Undeploy the application at a given path
		
		:param path: The path of the application to undeploy
		:param version: The version to undeploy
		:return: :class:`TomcatManagerResponse <TomcatManagerResponse>` object
		:rtype: tomcatmanager.TomcatManagerResponse		
				
		If an application was deployed using a version, then a version is required to
		undeploy the application.
		"""
		params = {'path': path}
		if version:
			params['version'] = version
		return self._get('undeploy', params)
