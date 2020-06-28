from analysis.config import *

def findrootnode(dataclean_json,sysdata_json):
    list_root_node = {}
    '''
        {
            "index":name
        }
    '''
    for index,syssdata in enumerate(sysdata_json):
        if not kindssys(sysdata_json[syssdata][-1]):
            #print(index,haverootdetail2(train_datas[index]),"无根因")
            list_root_node[str(index)] = 0
            continue
        #有根因的
        else:
            all_root_node = {}
            w_all_root_node = {}
            nodedata = dataclean_json[index]
            single_sys = list(sysdata_json[str(index)][-1].keys())
            for Index,link in enumerate(sysdata_json[syssdata][:-1][0]):
                F_sys,S_sys,w = link
                single_sys = list(np.setdiff1d(single_sys,[F_sys,S_sys]))
                if sysdata_json[syssdata][-1][F_sys] + sysdata_json[syssdata][-1][S_sys] == "1.01.0":
                    continue
                labels = dict()
                G = nx.DiGraph()
                G.clear()
                plt.cla()
                

                true_first = nodedata[F_sys]['true_first']
                true_second = nodedata[F_sys]['true_second']
                true_third = nodedata[F_sys]['true_third']
                S_true_first = nodedata[S_sys]['true_first']
                S_true_second = nodedata[S_sys]['true_second']
                S_true_third = nodedata[S_sys]['true_third']
                    
                pos = dict()
                pos.update( (n, (1, i)) for i, n in enumerate(true_first) )
                pos.update( (n, (2, i)) for i, n in enumerate(true_second) )
                pos.update( (n, (3, i)) for i, n in enumerate(true_third) )
                pos.update( (n, (4, i)) for i, n in enumerate(S_true_first) )
                pos.update( (n, (5, i)) for i, n in enumerate(S_true_second) )
                pos.update( (n, (6, i)) for i, n in enumerate(S_true_third) )
                    
                for a in true_third:
                    for b in S_true_first:
                        G.add_edge(a,b)
                        labels[a] = a +" "+ str(nodedata['node_detail'][a]['kinds'])+" "+F_sys+" "+str(nodedata['node_detail'][a]['root'])
                        labels[b] = b +" "+ str(nodedata['node_detail'][b]['kinds'])+" "+S_sys+" "+str(nodedata['node_detail'][b]['root'])
                    
                if len(true_second) != 0 :
                    for a in true_second:
                        for b in true_third:
                            G.add_edge(a,b)
                            labels[a] = a +" "+ str(nodedata['node_detail'][a]['kinds'])+" "+F_sys+" "+str(nodedata['node_detail'][a]['root'])
                            labels[b] = b +" "+ str(nodedata['node_detail'][b]['kinds'])+" "+F_sys+" "+str(nodedata['node_detail'][b]['root'])
                                
                    if len(true_first)!=0:
                        for a in true_first:
                            for b in true_second:
                                G.add_edge(a,b)
                                labels[a] = a +" "+ str(nodedata['node_detail'][a]['kinds'])+" "+F_sys+" "+str(nodedata['node_detail'][a]['root'])
                                labels[b] = b +" "+ str(nodedata['node_detail'][b]['kinds'])+" "+F_sys+" "+str(nodedata['node_detail'][b]['root'])
                                
                if len(S_true_second) != 0 :
                    for a in S_true_first:
                        for b in S_true_second:
                            G.add_edge(a,b)
                            labels[a] = a +" "+ str(nodedata['node_detail'][a]['kinds'])+" "+S_sys+" "+str(nodedata['node_detail'][a]['root'])
                            labels[b] = b +" "+ str(nodedata['node_detail'][b]['kinds'])+" "+S_sys+" "+str(nodedata['node_detail'][b]['root'])
                                    
                    if len(S_true_third)!=0:
                        for a in S_true_second:
                            for b in S_true_third:
                                G.add_edge(a,b)
                                labels[a] = a +" "+ str(nodedata['node_detail'][a]['kinds'])+" "+S_sys+" "+str(nodedata['node_detail'][a]['root'])
                                labels[b] = b +" "+ str(nodedata['node_detail'][b]['kinds'])+" "+S_sys+" "+str(nodedata['node_detail'][b]['root'])
                #根因结点判断
                weight = 0
                last_node = {}
                for node in G.nodes():
                    if G.out_degree(node)==0:
                        last_node[node] = labels[node].split()[2]
                if len(last_node) == 1:
                    last_node_name = list(last_node.keys())[0]
                    last_node_sys = last_node[last_node_name]
                    #该节点是否等于1
                    if nodedata['node_detail'][last_node_name]['kinds'] != "1":
                        all_root_node[last_node_name] = last_node_sys
                        w_all_root_node[last_node_name] = weight
                    else:
                        #前一节点个数是否唯一
                        node_result = predecessors(G,last_node_name,nodedata,weight+1)
                        nodename = node_result[0]
                        weight = node_result[1]
                        all_root_node[nodename] = labels[nodename].split()[2]
                        w_all_root_node[nodename] = weight
                else:#判断是否存在后续sys
                    flag = 0
                    if len(nodedata[S_sys]["true_third"]) != 0:
                        last_syss =  sys_json[S_sys]
                        for last_sys in last_syss:
                            if len(nodedata[last_sys]["true_first"]) != 0:
                                flag = 1
                    
                    #是否存在后续sys
                    if flag == 1:
                        continue
                    else:
                        the_last_node_nums = 0
                        the_last_node_name = ''
                        for the_last_node in last_node:
                            if nodedata['node_detail'][the_last_node]['kinds'] != "1":
                                the_last_node_nums += 1
                                the_last_node_name = the_last_node
                        #判断几个不等于1的
                        if the_last_node_nums == 1:
                            all_root_node[the_last_node_name] = labels[the_last_node_name].split()[2]
                            w_all_root_node[the_last_node_name] = weight+1
                        elif the_last_node_nums == 0:
                            node_predecessors = set()
                            for the_last_node in last_node:
                                result = predecessors(G,the_last_node,nodedata,weight+1)
                                node_predecessors.add(result)
                            if len(node_predecessors) == 1:
                                nodename = list(node_predecessors)[0][0]
                                weight = list(node_predecessors)[0][1]
                                all_root_node[nodename] = labels[nodename].split()[2]
                                w_all_root_node[nodename] = weight
                            else:
                                print(index,the_last_node_nums)
                        else:
                            print(index,last_node)
                            
                            
                        
                        
                #绘图
                
                #nx.draw(G,pos=pos,labels=labels,with_labels=True)
                #plt.title(str(index)+' '+F_sys+" "+S_sys)
                #try:
                #    os.mkdir('3.图片/'+str(index))
                #except:
                #    pass

                #figure = plt.gcf()
                #figure.set_size_inches(15, 8)
                #plt.savefig('3.图片/'+str(index)+"/"+str(Index)+".png")
                #plt.show()
                plt.cla()
            
            #单点部分
            if len(single_sys) != 0:
                for singlesys in single_sys:
                    if sysdata_json[str(index)][-1][singlesys] != "1.0":
                        labels = dict()
                        G = nx.DiGraph()
                        G.clear()
                        plt.cla()
                        
                        true_first = nodedata[singlesys]['true_first']
                        true_second = nodedata[singlesys]['true_second']
                        true_third = nodedata[singlesys]['true_third']

                        pos = dict()
                        pos.update( (n, (1, i)) for i, n in enumerate(true_first) )
                        pos.update( (n, (2, i)) for i, n in enumerate(true_second) )
                        pos.update( (n, (3, i)) for i, n in enumerate(true_third) )

                        for a in true_first:
                            for b in true_second:
                                G.add_edge(a,b)
                                labels[a] = a +" "+ str(nodedata['node_detail'][a]['kinds'])+" "+singlesys+" "+str(nodedata['node_detail'][a]['root'])
                                labels[b] = b +" "+ str(nodedata['node_detail'][b]['kinds'])+" "+singlesys+" "+str(nodedata['node_detail'][b]['root'])

                        for a in true_second:
                            for b in true_third:
                                G.add_edge(a,b)
                                labels[a] = a +" "+ str(nodedata['node_detail'][a]['kinds'])+" "+singlesys+" "+str(nodedata['node_detail'][a]['root'])
                                labels[b] = b +" "+ str(nodedata['node_detail'][b]['kinds'])+" "+singlesys+" "+str(nodedata['node_detail'][b]['root'])

                        #绘图
                
                        #nx.draw(G,pos=pos,labels=labels,with_labels=True)
                        #plt.title(str(index)+' '+F_sys+" "+S_sys)
                        #try:
                        #    os.mkdir('3.图片/'+str(index))
                        #except:
                        #    pass

                        #figure = plt.gcf()
                        #figure.set_size_inches(15, 8)
                        #plt.savefig('3.图片/'+str(index)+"/"+str(Index)+".png")
                        #plt.show()
                        plt.cla()
                        
                        #根因结点判断
                        weight = 0
                        last_node = {}
                        for node in G.nodes():
                            if G.out_degree(node)==0:
                                last_node[node] = labels[node].split()[2]
                        if len(last_node) == 1:
                            last_node_name = list(last_node.keys())[0]
                            last_node_sys = last_node[last_node_name]
                            #该节点是否等于1
                            if nodedata['node_detail'][last_node_name]['kinds'] != "1":
                                all_root_node[last_node_name] = last_node_sys
                                w_all_root_node[last_node_name] = weight
                            else:
                                #前一节点个数是否唯一
                                node_result = predecessors(G,last_node_name,nodedata,weight+1)
                                nodename = node_result[0]
                                weight = node_result[1]
                                all_root_node[nodename] = labels[nodename].split()[2]
                                w_all_root_node[nodename] = weight
                        else:#判断是否存在后续sys
                            the_last_node_nums = 0
                            the_last_node_name = ''
                            for the_last_node in last_node:
                                if nodedata['node_detail'][the_last_node]['kinds'] != "1":
                                    the_last_node_nums += 1
                                    the_last_node_name = the_last_node
                            #判断几个不等于1的
                            if the_last_node_nums == 1:
                                all_root_node[the_last_node_name] = labels[the_last_node_name].split()[2]
                                w_all_root_node[the_last_node_name] = weight+1
                            elif the_last_node_nums == 0:
                                node_predecessors = set()
                                for the_last_node in last_node:
                                    result = predecessors(G,the_last_node,nodedata,weight+1)
                                    node_predecessors.add(result)
                                if len(node_predecessors) == 1:
                                    nodename = list(node_predecessors)[0][0]
                                    weight = list(node_predecessors)[0][1]
                                    all_root_node[nodename] = labels[nodename].split()[2]
                                    w_all_root_node[nodename] = weight
                                else:
                                    print(index,the_last_node_nums)
                            else:
                                print(index,last_node)
            if len(all_root_node) != 0:
                delete_node = set()
                for node_1 in all_root_node:
                    for node_2 in all_root_node:
                        if all_root_node[node_2] in sys_json[all_root_node[node_1]]:
                            delete_node.add(node_1)
                for delete_node_name in list(delete_node):
                    all_root_node.pop(delete_node_name)
                    w_all_root_node.pop(delete_node_name)
                list_root_node[str(index)] = min(w_all_root_node, key=w_all_root_node.get)
                #print(index,min(w_all_root_node, key=w_all_root_node.get),haverootdetail2(train_datas[index])[1])

    #print(all,right)

    return list_root_node

    
