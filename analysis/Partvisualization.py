from analysis.config import *
import re

def partvisualization(nodedetail,rootnode,rootcause):
    node=list()
    edge=list()
    G = nx.Graph()
    G.clear()
    for index,nodename in enumerate(nodedetail):
        for sys in sys_node_json:
            if nodename in sys_node_json[sys]:
                sysname = sys
                break
        kinds = nodedetail[nodename]["kinds"]
        kind = str(nodedetail[nodename]["kind"])
        kind = re.sub(r", ",'<br>',kind)
        kind = re.sub(r"{|}",'',kind)
        kind = re.sub(r"[*]+",'*',kind)
        kind = kind.replace(rootcause,"<font color='#FF0000'>"+rootcause+"</font>" )
        times = str(nodedetail[nodename]["times"])
        G.add_node(index)
        if(nodename == rootnode):
            rootindex = index
            node.append({
            'id': index,
            'label': sysname+" "+ nodename,
            'chosen':False,
            'color': 
                { 
                  'border': 'yellow',
                  'background': 'yellow',
                },
            'title': '<span>告警信息种类数：</span>'+kinds+"<br>"+"<span>告警信息：次数：</span><br>"+kind+"<br><span>一共告警次数：</span>"+times+"<span>次</span>",
            'size':100
            })
        else:
            node.append({
            'id': index,
            'label': sysname+" "+ nodename,
            'chosen':False,
            'color': 
                { 
                  'border': 'green',
                  'background': 'green',
                },
            'title': '<span>告警信息种类数：</span>'+kinds+"<br>"+"<span>告警信息：次数：</span><br>"+kind+"<br><span>一共告警次数：</span>"+times+"<span>次</span>",
            'size':100
            })
        for sonnode in node_json[nodename]:
            if sonnode in nodedetail:
                the_id = list(nodedetail.keys()).index(sonnode)
                G.add_edge(index,the_id)
                edge.append({
                  "from":index,
                  "to":the_id
                })

    node = [i for i in node if nx.has_path(G,i["id"],rootindex)]
    return node,edge
