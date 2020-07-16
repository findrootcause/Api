import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import csv
import shutil

'''
# 设置matplotlib正常显示中文和负号
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
'''

#数据写入
sysfile = "E:/软件杯2020/data_release/topology/topology_edges_sys.json"
nodefile = "E:/软件杯2020/data_release/topology/topology_edges_node.json"
sys_nodefile = "E:/软件杯2020/data_release/topology/sys_and_nodes.json"


with open(sysfile) as f:
    sys_json = json.load(f)

with open(nodefile) as f:
    node_json = json.load(f)

with open(sys_nodefile) as f:
    sys_node_json = json.load(f)

def RGB_to_Hex(times):
    if times == 0:
        return "blue"
    x = str(255-4*times)
    rgb = x+","+x+","+x
    RGB = rgb.split(',')            # 将RGB格式划分开来
    color = '#'
    for i in RGB:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color


#归一化数据
def normalization(x,node_times):
    maxnumm =  max(node_times.values())
    minnum = min(node_times.values())
    mean = np.mean(list(node_times.values()))
    if x>mean:
        return round((x-minnum)/(maxnumm-minnum)*100)
    else:
        return 0

def normalization2(x,a_list):
    maxnumm =  max(a_list)
    minnum = min(a_list)
    
    return ((x-minnum)/(maxnumm-minnum+0.001) + 0.5)

 
def haveroot(event):
    for i in event:
        if i['is_root'] == "1":
            return 1
    return 0

def haverootdetail(event):
    for i in event:
        if i['is_root'] == "1":
            nodename = i['triggername'].split()[0][2:]
            cause = i['triggername']
            sysname = i['sysEname']
            return (1,sysname,nodename,cause)
    return (0,"无根因")

def haverootdetail2(event):
    for i in event:
        if i['is_root'] == "1":
            nodename = i['triggername'].split()[0][2:]
            cause = i['triggername']
            sysname = i['sysEname']
            return sysname,nodename,cause
    return "无根因"

def findrootcause(event,nodename):
    root_node_dict = dict()
    for i in event:
        name = i['triggername'].split()[0][2:]
        if nodename == name:
            cause = i['triggername']
            if cause in root_node_dict:
                root_node_dict[cause] +=1
            else:
                root_node_dict[cause] = 1
    return root_node_dict

def find_link(G,node,nodes,nodetimes):
        mode = []
        for x,y in G.out_edges(node):
                if (y in nodes) and (y in nodetimes) and (nodetimes[y] != 0):
                        if find_link(G,y,nodes,nodetimes) != [{"only":x}]:
                                newmode = {"head":x, "then":find_link(G,y,nodes,nodetimes)}
                        else:
                                newmode = {"head":x, "then":y}
                        mode.append(newmode)
                else:
                        pass
        if mode == []:
            mode = [{"only":x}]
        return mode

def predecessors(G,last_node_name,nodedata,n):
    node_predecessors = list(G.predecessors(last_node_name))
    if len(node_predecessors)==1:
        if nodedata['node_detail'][node_predecessors[0]]['kinds'] != "1" :            
            return node_predecessors[0],n
        else:
            return predecessors(G,node_predecessors[0],nodedata,n+1)
    else:
        js = 0
        js_name = ""
        for node_predecessor in node_predecessors:
            if nodedata['node_detail'][node_predecessor]['kinds'] != "1":
                js += 1
                js_name = node_predecessor
        
        if js == 1:
            return js_name,n+1
        else:
            return last_node_name,n+2

def kindssys(sysdata):
    for sys in sysdata:
        if sysdata[sys] != "1.0":
            return True
    else:
        return False 
