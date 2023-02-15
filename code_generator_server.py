import json
import sys
function_template="""
import socket 
import sys
import pickle
from server_procedures import *
import json



def validation(mes,d):
    par=[]
    if(len(d[mes["fname"]])!=(len(mes)-3)):
        return [False,par]
    for i in d[mes["fname"]]:
        print(i)
        if i in mes.keys():
            print(d[mes["fname"]][i],mes[i]["type"])
            if d[mes["fname"]][i] in mes[i]["type"]:
                print(mes[i]["value"])
                par.append(mes[i]["value"])
            else:
                return [False,par]
        else:
            return [False,par]
    return [True,par]



# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


host = "127.0.0.1"  
port = 9999
print(host)
# bind the socket to a specific IP and port
serversocket.bind((host, port))
val_dict={dict}
# queue up to 5 requests
serversocket.listen(5)
#validtion dict


while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()      
    print("Got a connection from ",str(addr))
    raw_req=clientsocket.recv(4096)
    raw_req=raw_req.decode()
    mes = json.loads(raw_req)
    val_data,params=validation(mes,val_dict)
    
    if(not val_data):
        output="Wrong Params"
        output_bytes=output.encode()
        clientsocket.send(output_bytes)
    else:
        print(len(params))
        # output=eval(\"f_name(*params)\")
        output=eval("{{}}".format(mes["fname"]))
        output=output(*params)
        if mes["return_type"] in str(type(output)):
            output=str(output)
            output_bytes=output.encode()
        else:
            output="Mismatch in return type expected and obtained"
            output_bytes=output.encode()
        
        clientsocket.send(output_bytes)



    # clientsocket.send(msg.encode('ascii'))
    clientsocket.close()

"""
try:
    cname=sys.argv[1]
    with open(cname,'r') as file:
        j=json.load(file)
    with open('rpc_server.py','w') as f:
        d={}
        # f.write(class_template.format(ip,port))
        for i in j["remote_procedures"]:
            name=i["procedure_name"]
            print(name)
            name_params=[]
            print(i["procedure_name"])
            p={}
            for k in i["parameters"]:
                p[k["parameter_name"]]=k["data_type"]
            d[name]=p
        temp=function_template
        temp=temp.format(
            f_name=name,
            dict=d
        )
        print(d)
        f.write(temp)
except Exception as e:
    print(e)