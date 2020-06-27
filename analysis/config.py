import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import csv

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
        
def haveroot(event):
    for i in event:
        if i['is_root'] == "1":
            return 1
    return 0


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

    
