'''
Create and manipulate pyvis networks

Functions:
    get_new_network() -> network
    plot_network(network, sources, targets, weights) -> network
    annotate_network(network) -> network
    get_node_list(network) -> node_list
    def get_subnetwork_nodes(node, network) -> node_list
'''

from pyvis.network import Network

def get_new_network():
    '''Create an empty network'''
    network = Network(height='100%', width='75%', bgcolor='white', font_color='black')
    network.barnes_hut()
    network.show_buttons(filter_=True)
    return network

def plot_network(network, sources, targets, weights):
    '''Plot nodes to a network using a list of sources, targets and weights'''
    edge_data = zip(sources, targets, weights)
    for edge in edge_data:
        source = edge[0]
        destination = edge[1]
        weight = edge[2]
        network.add_node(source, source, title=source)
        network.add_node(destination, destination, title=destination)
        network.add_edge(source, destination, value=weight)
    return network

def annotate_network(network):
    '''Colour and annotate specific nodes in a network'''
    colourme = 'BGC' ## change this to add colour definition
    neighbor_map = network.get_adj_list()
    for node in network.nodes:
        neighbours = len(neighbor_map[node['id']])
        title = '<br>' + str(neighbours) + ' neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
        node['title'] += title
        node['value'] = neighbours
        if colourme in node['id']:
            node['color'] = 'red'
    return network

def get_node_list(network):
    '''Return a list of nodes from a network'''
    node_list = []
    for node in network.nodes:
        node_list.append(node['id'])
    return node_list

def get_subnetwork_nodes(node, network):
    '''return a list of nodes from a subnetwork'''
    node_list = []
    node_list.append(node)
    neighbor_map = network.get_adj_list()
    old_length = 1
    new_length = 2
    while old_length != new_length:
        old_length = new_length
        for node_of_interest in node_list:
            for neighbour in neighbor_map[node_of_interest]:
                if neighbour not in node_list:
                    node_list.append(neighbour)
        new_length = len(node_list)
    return node_list
