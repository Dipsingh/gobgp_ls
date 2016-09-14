import zmq
import networkx as nx

class Node(object):
    _instance_track = []
    def __init__(self,node_name,iso_system_id,router_id):
        self.node_name = node_name
        self.iso_system_id = iso_system_id
        self.router_id = router_id
        self.prefix_metric = {}
        self._instance_track.append(self)
        self.label_base = None
        self.label_range = None
        self.node_sid = None

    def add_prefix_metric(self,prefix,metric):
        self.prefix_metric[prefix] = metric
    @classmethod
    def get_instance(cls):
        return cls._instance_track


def parse_nodes(json_message):
    G=nx.MultiDiGraph()
    for key in json_message:
        if key['paths']:
            for attr in key['paths']:
                if attr['nlri']['nlritype'] == "node":
                    iso_id = attr['nlri']['nodeid']
                    for pathattr in attr['attrs']:
                        if pathattr['type'] == 29:
                            for node_attr in pathattr['LSAttributeValue']:
                                if node_attr['type'] == 1026:
                                    name=node_attr['NodeName']
                                if node_attr['type'] == 1028:
                                    router_id = node_attr['value']
                                if node_attr['type'] == 1034:
                                    #BASE+RANGE
                                    label_range = node_attr['labelRange']
                                    for labelbase in node_attr['labelstart']:
                                        label_base = labelbase['label']
                    node_instance = Node(name,iso_id,router_id)
                    if label_base != None and label_range != None:
                        node_instance.label_range = label_range
                        node_instance.label_base = label_base

    for key in json_message:
        if key['paths']:
            for attr in key['paths']:
                if attr['nlri']['nlritype'] == "prefix":
                    for pathattr in attr['attrs']:
                        if pathattr['type'] == 14:
                            for item in pathattr['value']:
                                prefix_len = item['prefix']+"/"+str(item['prefixlen'])
                                for node in Node.get_instance():
                                    if node.iso_system_id == item['nodeid']:
                                        node.add_prefix_metric(prefix_len,str(0))
    for key in json_message:
        if key['paths']:
            for attr in key['paths']:
                if attr['nlri']['nlritype'] == 'prefix':
                    for node in Node.get_instance():
                        if node.iso_system_id == attr['nlri']['nodeid']:
                            for patthattr in attr['attrs']:
                                if patthattr['type'] == 29:
                                    for lsattr in patthattr['LSAttributeValue']:
                                        if lsattr['type'] == 1158:
                                            node.node_sid =lsattr['prefixsid']


    for node in Node.get_instance():
        print (node.node_name,node.node_sid)

    for node in Node.get_instance():
        G.add_node(node.iso_system_id)
        G.node[node.iso_system_id]['router_id'] = node.router_id
        G.node[node.iso_system_id]['iso_id'] = node.iso_system_id
        G.node[node.iso_system_id]['prefix_metric'] = node.prefix_metric
        G.node[node.iso_system_id]['name'] = node.node_name
        G.node[node.iso_system_id] ['labelrange'] = node.label_range
        G.node[node.iso_system_id] ['labelbase'] = node.label_base
        G.node[node.iso_system_id] ['nodesid'] = node.node_sid

    return (G)

def parse_links(json_message):
    edge_dict = {}
    attr_dict = {}
    for key in json_message:
        if key['paths']:
            for attr in key['paths']:
                if attr['nlri']['nlritype'] == "link":
                    source_node = attr['nlri']['localnode']
                    dest_node = attr['nlri']['remotenode']
                    local_ip = attr['nlri']['localip']
                    remote_ip = attr['nlri']['remoteip']
                    attr_dict ['local_ip'] = local_ip
                    attr_dict ['remote_ip'] = remote_ip
                    for item in attr['attrs']:
                        if item['type'] == 29:
                            for pathattr in item['LSAttributeValue']:
                                if pathattr['type']== 1028:
                                    source_router_id = pathattr['value']
                                    attr_dict['source_router_id'] = source_router_id
                                if pathattr['type']== 1030:
                                    dest_router_id = pathattr['value']
                                    attr_dict['dest_router_id'] = dest_router_id
                                if pathattr['type']== 1089:
                                    max_link_bandwidth = pathattr['MaxLinkBW']
                                    attr_dict['max_link_bandwidth'] = max_link_bandwidth
                                if pathattr['type']== 1092:
                                    te_metric = pathattr['value']
                                    attr_dict['te_metric'] = te_metric
                                if pathattr['type']== 1095:
                                    igp_metric = pathattr['value']
                                    attr_dict['igp_metric'] = igp_metric
                                if pathattr['type']== 1091:
                                    unreserved_bw = pathattr['UnresvBW']['0']
                                    attr_dict['unreserved_bw'] = unreserved_bw
                                if pathattr['type']== 1099:
                                    if pathattr['AdjSidFlags'] == 48:
                                        adj_sid_label = pathattr['AdjLabel']
                                        attr_dict['adj_sid_label']=adj_sid_label
                                if pathattr['type']== 1088:
                                    color = "white"
                                    attr_dict['color'] = color
                                edge_dict[source_node,dest_node] = dict(attr_dict)
    return (edge_dict)


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:9999")
    socket.send(b"SendTopology")
    json_message = socket.recv_json()

    graph_nodes=parse_nodes(json_message)
    edge_dict = parse_links(json_message)



if __name__ == "__main__":
    main()