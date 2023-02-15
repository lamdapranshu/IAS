#IMPORTS
import json
import sys

#TEMPLATES
function_template="""

def {func_name}(*args):
    fname=\"{func_name}\"
    num={num_of_params}
    name_of_params=[{params}]
    return_type=\"{rtype}\"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
        # connecting to the server
        s.connect((IP, PORT))
        req=request(\"{func_name}\",len(args))
        cnt=0
        mes={{}}
        mes["fname"]=fname
        mes["return_type"]=return_type
        mes["num"]=num
        for prm_val in args:
            p={{}}
            p["type"]=str(type(prm_val))
            p["value"]=prm_val
            mes[name_of_params[cnt]]=p
            cnt+=1
        smes=json.dumps(mes)
        s.send(smes.encode())
        response = s.recv(4096)
        return response.decode()
        
    except socket.error as err:
        print ("socket creation failed with error ",err)
        return err

"""
class_template="""
import socket 
import sys
import pickle
IP=\"{}\"
PORT={}
import json
class param:
    param_name=None
    param_type=None
    param_value=None
    def __init__(self,name,type,value):
        self.param_name=name
        self.param_type=type
        self.param_value=value
class request:
    name_of_func=None
    no_of_params=None
    list_of_params=[]
    return_type=None
    def __init__(self,namef,no_params):
        self.name_of_func=namef
        self.no_of_params=no_params
    def add_params(self,param):
        self.list_of_params.append(param)
"""
j=None
print("Give IP")
ip=input()
print("Give Port")
port=input()
cname=sys.argv[1]

with open(cname,'r') as file:
    j=json.load(file)
with open('rpc_client.py','w') as f:
    f.write(class_template.format(ip,port))
    for i in j["remote_procedures"]:
        name=i["procedure_name"]
        print(name)
        name_params=[]
        print(i["procedure_name"])
        for k in i["parameters"]:
            pr="\""+k["parameter_name"]+"\""
            name_params.append(pr)
        cnt=len(name_params)
        name_params=",".join(name_params)
        rt=i["return_type"]
        temp=function_template
        temp=temp.format(
            func_name=name,
            params=name_params,
            num_of_params=cnt,
            rtype=rt
        )
        f.write(temp)