#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from resourceconfig import ResourceConfig

class Node(BaseObject):
	"""
	
	"""

	__config = {
		
		"3b1c1b58-056d-4fc4-80ef-13d02199ae3a" : OperationConfig("/labs/proxy/chain/api/v1/network/create", "create", [], []),
		
		"3914f8c6-b71d-45fe-b854-ccf27165dff7" : OperationConfig("/labs/proxy/chain/api/v1/network/invite", "create", [], []),
		
		"467e61cf-03d6-4694-a035-e0793f5c5ccf" : OperationConfig("/labs/proxy/chain/api/v1/network/join", "create", [], []),
		
		"a2ff8211-6337-40a9-9d55-55dc486da0b9" : OperationConfig("/labs/proxy/chain/api/v1/network/node/{address}", "read", [], []),
		
		"4cca1d38-b997-469d-9e04-e217666091fb" : OperationConfig("/labs/proxy/chain/api/v1/network/node", "query", [], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUID)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative())


	@classmethod
	def provision(cls,mapObj):
		"""
		Creates object of type Node

		@param Dict mapObj, containing the required parameters to create a new object
		@return Node of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("3b1c1b58-056d-4fc4-80ef-13d02199ae3a", Node(mapObj))






	@classmethod
	def invite(cls,mapObj):
		"""
		Creates object of type Node

		@param Dict mapObj, containing the required parameters to create a new object
		@return Node of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("3914f8c6-b71d-45fe-b854-ccf27165dff7", Node(mapObj))






	@classmethod
	def join(cls,mapObj):
		"""
		Creates object of type Node

		@param Dict mapObj, containing the required parameters to create a new object
		@return Node of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("467e61cf-03d6-4694-a035-e0793f5c5ccf", Node(mapObj))










	@classmethod
	def read(cls,id,criteria=None):
		"""
		Returns objects of type Node by id and optional criteria
		@param str id
		@param dict criteria
		@return instance of Node
		@raise ApiException: raised an exception from the response status
		"""
		mapObj =  RequestMap()
		if id:
			mapObj.set("id", id)

		if criteria:
			if (isinstance(criteria,RequestMap)):
				mapObj.setAll(criteria.getObject())
			else:
				mapObj.setAll(criteria)

		return BaseObject.execute("a2ff8211-6337-40a9-9d55-55dc486da0b9", Node(mapObj))







	@classmethod
	def query(cls,criteria):
		"""
		Query objects of type Node by id and optional criteria
		@param type criteria
		@return Node object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("4cca1d38-b997-469d-9e04-e217666091fb", Node(criteria))


