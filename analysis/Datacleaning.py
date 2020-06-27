from analysis.config import *

def datacleaning(path):
    #数据写入
    all_json = list()
    train_datas = list()
    filePath = path
    csv_name = os.listdir(filePath)
    csv_name.sort(key=lambda x:int(x[:-4]))

    for filename in csv_name:
        csv_data = []
        train_data = []
        with open(filePath+filename,"r", encoding='UTF-8') as fp:
            csv_data = csv.DictReader(fp)
            for i in csv_data:
                train_data.append(i)
        train_datas.append(train_data)

    sys_link = {}
    for Index,event in enumerate(train_datas):
        sys_link[str(Index)]=[]
        #节点出现次数
        node_times = {}
        #节点出现警报种类次数
        node_kinds = {}
        #根因
        root_node = ""
        """
        node_kinds ={
            "name":{"xxx","xxx"}
        }
        """
        '''if not haveroot(event) : 
            continue'''
        for one_data in event:
            nodename = one_data['triggername'].split()[0][2:]
            if one_data['is_root'] == "1":
                root_node=nodename
            cause = "".join(one_data['triggername'].split()[1:])
            if nodename not in node_times:
                node_times[nodename] = 1
                node_kinds[nodename] = set()
                node_kinds[nodename].add(cause)
            else:
                node_times[nodename] += 1
                node_kinds[nodename].add(cause)
        z = list()
        for num in node_times.values():
            z.append(normalization(num,node_times))
        for index,i in enumerate(node_times):
            node_times[i] = z[index]

        the_sys_dict = dict()
        w_node_labels = dict()
        #对于每个系统的
        for index,nodesname in enumerate(sys_node_json.keys()):
            the_first = 0
            the_sys_link = {nodesname:[]}
            color_map = []
            nodes = sys_node_json[nodesname]
            first_nodes = set()
            second_nodes = set()
            third_nodes = set()
            four_nodes = set()
            node_labels = {}
            pos = dict()
            G = nx.DiGraph()
            G.clear()
            for node in nodes:
                for next_node in node_json[node]:
                    G.add_edge(node,next_node)
            for node in G.nodes:
                if node in node_times:
                    color_map.append(RGB_to_Hex(node_times[node]))
                    if node ==  root_node:
                       node_labels[node] = "ROOT"+str(len(node_kinds[node]))+"__"+node
                       if node_times[node] != 0 :
                           w_node_labels[node] = {"kinds":str(len(node_kinds[node])),"times":node_times[node],'root':1}
                    else:
                        node_labels[node] = str(len(node_kinds[node]))+"__"+node
                        if node_times[node] != 0 :
                            w_node_labels[node] = {"kinds":str(len(node_kinds[node])),'root':0}
                else:
                    color_map.append('blue')
            #将sys内nodes归类
            for node in nodes:
                if G.in_degree(node) == 0:
                    first_nodes.add(node)
                    for x,y in G.edges(node):
                        second_nodes.add(y)
                        for a,b in G.edges(y):
                            third_nodes.add(b)
                            for c,d in G.edges(b):
                                four_nodes.add(d)
                                if G.edges(d):
                                    print(1)


            np_node_times = np.array([ x   for x in node_times.keys() if node_times[x]>0 ])
            np_first = np.array(list(first_nodes))
            np_second = np.array(list(second_nodes))
            np_third = np.array(list(third_nodes))
            true_first = list(np.intersect1d(np_first,np_node_times))
            true_second = list(np.intersect1d(np_second,np_node_times))
            true_third = list(np.intersect1d(np_third,np_node_times))
            the_sys_dict[nodesname] = dict()

            the_sys_dict[nodesname]["true_first"] = true_first
            the_sys_dict[nodesname]["true_second"] = true_second
            the_sys_dict[nodesname]["true_third"] = true_third
            

            
            if len(true_first) != 0:
                the_sys_dict[nodesname]['first'] = true_first
                the_sys_dict[nodesname]['value'] = len(true_first)
                the_sys_dict[nodesname]['kind'] = 'only'
            else:
                the_sys_dict[nodesname]['value'] = 0

            if len(true_second) != 0:
                if the_sys_dict[nodesname]['value'] :
                    the_sys_dict[nodesname]['value'] *= len(true_second)
                    the_sys_dict[nodesname]['kind'] = 'link'
                else:
                    the_sys_dict[nodesname]['value'] = len(true_second)
                
            if len(true_third) != 0 :
                the_sys_dict[nodesname]['third'] = true_third
                if len(true_second) != 0 :
                    the_sys_dict[nodesname]['value'] *= len(true_third)
                    the_sys_dict[nodesname]['kind'] = 'link'
                else:
                    the_sys_dict[nodesname]['kind'] = 'only'
                    the_sys_dict[nodesname]['value'] += len(true_third)

            #pos.update( (n, (1, i)) for i, n in enumerate(first_nodes) )
            #pos.update( (n, (2, i)) for i, n in enumerate(second_nodes) )
            #pos.update( (n, (3, i)) for i, n in enumerate(third_nodes) )
            #pos.update( (n, (4, i)) for i, n in enumerate(four_nodes) )
            #nx.draw(G,pos=pos,node_color = color_map, labels=node_labels,with_labels=True)
            #plt.show()
            #plt.savefig(str(Index)+'/'+str(index+1)+".png")
            #plt.cla()
        the_sys_dict['node_detail'] = w_node_labels
        all_json.append(the_sys_dict)
    return all_json
