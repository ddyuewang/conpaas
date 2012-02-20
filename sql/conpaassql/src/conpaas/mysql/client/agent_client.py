'''
Created on Jun 8, 2011

@author: ales
'''
from conpaas.web.http import _http_get, _http_post, _jsonrpc_get, _jsonrpc_post
import httplib, json
import sys


class AgentException(Exception): pass

def _check(response):
    code, body = response
    if code != httplib.OK: raise AgentException('Received http response code %d' % (code))
    try: data = json.loads(body)
    except Exception as e: raise AgentException(*e.args)
    if data['error']: raise AgentException(data['error'])
    else: return True

#===============================================================================
# def __check_reply(body):
#    try:
#        ret = json.loads(body)
#    except Exception as e: raise AgentException(*e.args)
#    if not isinstance(ret, dict): raise AgentException('Response not a JSON object')
#    if 'opState' not in ret: raise AgentException('Response does not contain "opState"')
#    if ret['opState'] != 'OK':
#        if 'ERROR' in ret['opState']: raise AgentException(ret['opState'], ret['error'])
#        else: raise AgentException(ret['opState'])
#    return ret
#===============================================================================

def get_server_state(host, port):
    method = "get_server_state"
    result = _jsonrpc_get(host, port, '/', method)
    if _check(result):
        return result
    else:
        return False

def start_server(host, port):
    method = "start_server"
    result = _jsonrpc_post(host, port, '/', method)
    if _check(result):
        return result
    else:
        return False

def printUsage():
    print 'Usage: agent_ip agent_port function function_params\n\
Functions:  get_server_state - no params\n \
            createMySQLServer - no params\n \
            restartMySQLServer - no params\n \
            stopMySQLServer - no params\n \
            configure_user - username, port \n \
            get_all_users - no params\n \
            remove_user - name \n \
            setMySQLServerConfiguration - paramid value\n \
            send_mysqldump -  location on disc\n'
    pass

def restartMySQLServer(host, port):
    method = "restartMySQLServer"
    result = _jsonrpc_post(host, port, '/', method)
    if _check(result):
        return result
    else:
        return False
    
def stop_server(host, port):
    method = "stop_server"
    result = _jsonrpc_post(host, port, '/', method)
    if _check(result):
        return result
    else:
        return False    

def configure_user(host, port, username, password):
    method = 'configure_user'
    params = {'username': username,
              'password': password}
    return _check(_jsonrpc_post(host, port, '/', method, params=params))
        
def get_all_users(host, port):
    method = "get_all_users"
    result = _jsonrpc_get(host, port, '/', method)
    if _check(result):
        return result
    else:
        return False

def remove_user(host,port,name):
    method = 'remove_user'
    params = {'username': name}
    return _check(_jsonrpc_get(host, port, '/', method, params=params))

def setMySQLServerConfiguration(host,port, param_id, val):
    params = {'action': 'setMySQLServerConfiguration',
              'id_param': param_id,
              'value': val
              }
    code, body = _http_post(host, port, '/', params= params)
    if code != httplib.OK: raise Exception('Received HTTP response code %d' % (code))
    return _check(body)

def send_mysqldump(host,port,location):
    params = {'method': 'create_with_MySQLdump'}
    files = {'mysqldump': location}
    return _check(_http_post(host, port, '/', params, files=files))
    
    #method = 'create_with_MySQLdump'
    #params = {
    #          'action': 'create_with_MySQLdump'}
    #_jsonrpc_post(host, port, '/', method, params=params)
    
    #code, body = _http_post(host, port, '/', params= params, files={'mysqldump':location})
    #if code != httplib.OK: raise Exception('Received HTTP response code %d' % (code))
    #return __check_reply(body)

def set_up_replica_master(host,port):
    params = {
              'action': 'set_up_replica_master'}
    code, body = _http_post(host, port, '/', params= params)
    if code != httplib.OK: raise Exception('Received HTTP response code %d' % (code))
    return _check(body)

'''
    @param master_host: hostname of the master node.
    @param master_log_file: filename of the master log.
    @param master_log_pos: position of the master log file.
    @param slave_server_id: id which will be written into my.cnf.

'''
def set_up_replica_slave(host,port, master_host, master_log_file, master_log_pos, slave_server_id):
    params = {
              'action': 'set_up_replica_slave',
              'master_host': master_host, 
              'master_log_file': master_log_file, 
              'master_log_pos': master_log_pos, 
              'slave_server_id': slave_server_id 
              }
    code, body = _http_post(host, port, '/', params= params)
    if code != httplib.OK: raise Exception('Received HTTP response code %d' % (code))
    return _check(body)

if __name__ == '__main__':
    if sys.argv.__len__() > 3:
        host = sys.argv[1]
        port = sys.argv[2]
        if sys.argv[3] == 'get_server_state':
            ret = get_server_state(host, port)
            print ret
        if sys.argv[3] == 'start_server':
            ret = start_server(host, port)
            print ret
        if sys.argv[3] == 'restartMySQLServer':
            ret = restartMySQLServer(host, port)
            print ret
        if sys.argv[3] == 'stop_server':
            ret = stop_server(host, port)
            print ret
        if sys.argv[3] == 'configure_user':
            ret = configure_user(host, port, sys.argv[4], sys.argv[5])
            print ret
        if sys.argv[3] == 'get_all_users':
            ret =get_all_users(host, port)
            print ret
        if sys.argv[3] == 'remove_user':
            ret = remove_user(host,port,sys.argv[4])
            print ret            
        if sys.argv[3] == 'setMySQLServerConfiguration':
            ret = setMySQLServerConfiguration(host,port, sys.argv[4], sys.argv[5])
            print ret                        
        if sys.argv[3] == 'send_mysqldump':
            ret = send_mysqldump(host,port,sys.argv[4])
            print ret            
    else:
        printUsage()        