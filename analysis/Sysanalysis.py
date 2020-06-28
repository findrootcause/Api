from analysis.config import *

def sysanalysis(train_datas,dataclean_json):
    big_sys = dict()
    for i in range(0,len(dataclean_json)):
        sys_set = set()
        the_sys = set()
        sys_relation = set()
        data_json = dataclean_json[i]
        for a_sys in data_json:
            if  "kind" not in data_json[a_sys]:
                continue
            else:
                sys_set.add(a_sys)
                
        G = nx.DiGraph()
        G.clear()
        plt.cla()
        color_map = []
        the_labels =dict()
        w_the_labels = dict()
        pos = dict()
        fir = set()
        sec = set()
        thi = set()
        fou = set()
        fiv = set()
        
        for sys in sys_set:
            G.add_node(sys)
            color_map.append(RGB_to_Hex(data_json[sys]['value']))
            for son_sys in sys_json[sys]:
                if son_sys in sys_set:
                    third_node = data_json[sys]["third"] if "third" in data_json[sys] else []
                    first_node = data_json[son_sys]["first"] if "first" in data_json[son_sys] else []
                    for node in third_node:
                        for son_node in node_json[node]:
                            if son_node in first_node:
                                sys_relation.add((sys,son_sys,(data_json[sys]['value']*data_json[son_sys]['value'])/10))
        

        tmp = set()
        for z in sys_relation:
            x,y,w = z
            G.add_edge(x,y,weight=w)
            tmp.add(x)
            tmp.add(y)
        edges = G.edges()
        weights = [G[u][v]['weight'] for u,v in edges]
        the_weights = []
        for value in weights:
               the_weights.append(normalization2(value,weights))

        for sys in sys_set:
            if G.in_degree(sys) == 0:
                fir.add(sys)
                for x,y in G.edges(sys):
                    sec.add(y)
                    for a,b in G.edges(y):
                        thi.add(b)
                        for c,d in G.edges(b):
                            fou.add(d)
                            for e,f in G.edges(d):
                                fiv.add(f)
                                if G.edges(f):
                                    print(1)
        
        pos.update( (n, (1, i)) for i, n in enumerate(fir) )
        pos.update( (n, (2, i)) for i, n in enumerate(sec) )
        pos.update( (n, (3, i)) for i, n in enumerate(thi) )
        pos.update( (n, (4, i)) for i, n in enumerate(fou) )
        pos.update( (n, (5, i)) for i, n in enumerate(fiv) )

        for sys in sys_set:
            the_sum = 0
            the_num = 0
            for sys_node in sys_node_json[sys]:
                if sys_node in data_json['node_detail']:
                    the_num += 1
                    the_sum += int(data_json['node_detail'][sys_node]["kinds"])
            the_avg = the_sum/the_num if the_num !=0 else 0
            the_labels[sys] = sys+"__"+str(round(the_avg,3))
            w_the_labels[sys] = str(round(the_avg,3))
        
        #nx.draw(G,pos=pos,edges=edges,width=weights,node_color = color_map,labels = the_labels ,with_labels=True)
        #result =  haverootdetail(train_datas[i])
        #if result[0]==0:
        #    plt.title(str(i)+" "+result[1], fontsize = 10)
        #else:
        #    plt.title(str(i)+" "+result[1]+" "+result[2]+" "+result[3], fontsize = 10)
        #plt.show()
        #plt.savefig('2.sys/'+str(i)+".png")
        plt.cla()
        #print(i,sys_relation)
        big_sys[str(i)]=[list(sys_relation),w_the_labels]

    return big_sys
     
