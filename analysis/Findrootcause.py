from analysis.config import *

def findcause(datacleandata,rootnode_json):
    rootcause = dict()
    for rootnodeindex in rootnode_json:
        if  rootnode_json[rootnodeindex] == 0:
            rootcause[rootnodeindex] = '无根因'
        else:
            result = findrootcause(datacleandata[int(rootnodeindex)],rootnode_json[rootnodeindex])
            rootcause[rootnodeindex] = "".join(max(result, key=result.get).split()[1:])
    return rootcause
