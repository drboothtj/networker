from pyvis.network import Network

def get_new_network():
    network = Network(height='100%', width='75%', bgcolor='white', font_color='black')
    network.barnes_hut()
    network.show_buttons(filter_=True)
    return network

def plot_network(network, sources, targets, weights):
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
    colourme = 'BGC' ## change this to add colour definition
    neighbor_map = network.get_adj_list()
    node_list = []
    for node in network.nodes:
        numberofneighbours = len(neighbor_map[node['id']])
        node['title'] += '<br>' + str(numberofneighbours) + ' neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
        node['value'] = numberofneighbours
        if colourme in node['id']:
            node['color'] = 'red'
    return network

def get_node_list(network):
    for node in network.nodes:
        node_list.append(node['id'])
    return node_list
