"""
Created on September, 2011

   This module gives a client methods to trigger a manager methods. See module :py:mod:`conpaas.mysql.server.manager.internals`.

   :platform: Linux, Debian
   :synopsis: Internals of ConPaaS MySQL Servers.
   :moduleauthor: Ales Cernivec <ales.cernivec@xlab.si> 

"""

from conpaas.web.http import _http_get, _http_post, HttpError, _jsonrpc_get,\
    _jsonrpc_post
import httplib, json
import sys
from threading import Thread
from conpaas.mysql.server.manager.internals import get_node_info

class ManagerException(Exception): pass

class ClientError(Exception): pass

def _check(response):
    code, body = response
    if code != httplib.OK: raise HttpError('Received http response code %d' % (code))
    try: data = json.loads(body)
    except Exception as e: raise ClientError(*e.args)
    if data['error']: raise ClientError(data['error'])
    else: return data['result']

def __check_reply(body):
    try:
        ret = json.loads(body)
    except Exception as e: raise ManagerException(*e.args)
    if not isinstance(ret, dict): raise ManagerException('Response not a JSON object')
    if 'opState' not in ret: raise ManagerException('Response does not contain "opState"')
    if ret['opState'] != 'OK':
        if 'ERROR' in ret['opState']: raise ManagerException(ret['opState'], ret['error'])
        else: raise ManagerException(ret['opState'])
    return ret

def printUsage():
    print 'Usage: service_ip service_port function function_params\n\
Functions:  getLog\n \
            list_nodes\n \
            get_node_info [serviceid] \n \
            get_service_info\n \
            add_nodes [number] \n \
            remove_nodes id [serviceid] \n \
            remove_nodes count [number] \n \
            get_service_performance \n'
    pass

def list_nodes(host, port):
    method = 'list_nodes'
    return _check(_jsonrpc_get(host, port, '/', method))

def get_node_info(host, port, serviceNodeId):
    method = 'get_node_info'
    params = {'serviceNodeId': serviceNodeId}
    return _check(_jsonrpc_get(host, port, '/', method, params=params))

def get_service_info(host, port):
    method = 'get_service_info'
    return _check(_jsonrpc_get(host, port, '/', method))

def add_nodes(host, port, count):
    params = {}
    params['count'] = int(count)
    method = 'add_nodes'
    return _check(_jsonrpc_post(host, port, '/', method, params=params))

def getLog(host, port):
    method = 'getLog'
    return _check(_jsonrpc_get(host, port, '/', method))

def remove_nodes_count(host, port, count):
    method = 'remove_nodes'
    params={}
    params['count'] = int(count)
    return _check(_jsonrpc_post(host, port, '/', method, params=params))

def remove_nodes_id(host, port, serviceNodeId):
    method = 'remove_nodes'
    params={}
    params['serviceNodeId'] = serviceNodeId
    return _check(_jsonrpc_post(host, port, '/', method, params=params))

def configure_user(host, port, vmid, username, password):
    method = 'configure_user'
    params = {'serviceNodeId': vmid,
              'username': username,
              'password': password}
    return _check(_jsonrpc_post(host, port, '/', method, params=params))

def get_service_performance(host, port):
    method = 'get_service_performance'
    return _check(_jsonrpc_get(host, port, '/', method))

if __name__ == '__main__':
    if sys.argv.__len__() in (4, 5,6,7):
        host = sys.argv[1]
        port = sys.argv[2]
        if sys.argv[3] in ("getLog"):
            ret = getLog(host, port)
            print ret
        if sys.argv[3] in ("list_nodes"):
            ret = list_nodes(host, port)
            print ret            
        if sys.argv[3] in ("add_nodes"):            
            ret = add_nodes(host, port, sys.argv[4])
            print ret            
        if sys.argv[3] in ("get_service_info"):
            ret = get_service_info(host, port)
            print ret            
        if sys.argv[3] in ("remove_nodes"):            
            if sys.argv[4] == 'count':
                ret = remove_nodes_count(host, port, sys.argv[5])
            if sys.argv[4] == 'id':
                ret = remove_nodes_id(host, port, sys.argv[5])                
            print ret            
        if sys.argv[3] in ("get_node_info"):   
            serviceNodeId = sys.argv[4]         
            ret = get_node_info(host, port, serviceNodeId)
            print ret    
        if sys.argv[3] in ("get_service_performance"):          
            ret = get_service_performance(host, port)
            print ret
        if sys.argv[3] in ("configure_user"):
            serviceNodeId = sys.argv[4]
            username = sys.argv[5]
            password = sys.argv[6]
            ret = configure_user(host, port, serviceNodeId, username, password)
            print ret    
    else:
        printUsage()