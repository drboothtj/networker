'''
Main routine for networker

Functions:
    calculate_threshold(database) -> threshold
    def extract_nodes(node, database) -> new_database
    generate_network(database,filename) -> network
    remove_data_under_threshold(database, threshold) -> database
    parse_args() -> args
    remove_self_hits(database) -> database
    run_diamond(filename)
    def main()
'''

import numpy as np
from networker import console, diamond, io, network, parser, plot

def calculate_threshold(database):
    '''calculate a usable threshold for networking using a histogram'''
    number_of_queries = database['query'].nunique()
    reccommended_cut_off = len(database.index) - (number_of_queries*3)
    database_size = len(database.index)
    threshold_histogram = np.histogram(database.loc[:, "identity"], bins=database_size)
    counts, bins = threshold_histogram
    for i in np.cumsum(counts):
        if  i > reccommended_cut_off:
            threshold = bins[i]
            break
    console.print_to_system("Recommended threshold calculated at " + str(threshold) + "% identity")
    return threshold

def extract_nodes(nodes, database):
    '''extract rows from the dataframe containing the reference node'''
    drop_list = []
    for i in database.index:
        query = database['query'][i]
        subject = database['subject'][i]
        if (query not in nodes) and (subject not in nodes):
            drop_list.append(i)
    new_database = database.drop(drop_list)
    return new_database

def generate_network(database, filename, print_list=False):
    '''generate and write the similiarity network from the database'''
    console.print_to_system("Generating network...")
    protein_network = network.get_new_network()
    sources = database['query']
    targets = database['subject']
    weights = database['identity']
    protein_network = network.plot_network(protein_network, sources, targets, weights)
    protein_network = network.annotate_network(protein_network)
    protein_network.save_graph(filename)
    if print_list is True:
        lines = network.get_node_list(protein_network)
        filename = io.change_extension(filename, 'txt')
        io.write_to_file(filename, lines)
        console.print_to_system('Node list saved as ' + filename)
    return protein_network

def remove_data_under_threshold(database, threshold):
    '''remove data from the dataframe that falls below the provided identity threshold'''
    console.print_to_system("Removing all hits below " + str(threshold) + "% identity...")
    below_threshold = []
    for i in database.index:
        identity = float(database['identity'][i])
        if identity < threshold:
            below_threshold.append(i)
    size_before = len(database.index)
    database = database.drop(below_threshold)
    size_after = len(database.index)
    size_difference = str(size_before - size_after)
    console.print_to_system(size_difference + " hits below the threshold and have been removed")
    return database

def parse_args():
    '''get the arguments from the console via the parser'''
    arg_parser = parser.get_parser()
    args = arg_parser.parse_args()
    return args

def remove_self_hits(database):
    '''remove selfhits from the BLASTP table'''
    console.print_to_system("Removing self hits...")
    self_hits = []
    for i in database.index:
        query = database['query'][i]
        subject = database['subject'][i]
        if query == subject:
            self_hits.append(i)
    database = database.drop(self_hits)
    return database

def run_diamond(filename):
    '''create a DIAMOND database and run a BLASTP search using the FAA file provided'''
    console.print_to_system('Making DIAMOND database...')
    diamond.make_diamond_database(filename)
    console.print_to_system('Running DIAMOND blastP...')
    diamond.run_diamond_search(filename)

def main():
    '''run networker'''
    console.print_to_system("Running Networker version 0.2.2")
    args = parse_args()

    if args.tsv is None:
        if args.faa is None:
            console.print_to_system('No TSV or FAA provided; exiting!')
            exit()
        console.print_to_system('No TSV provided; runing DIAMOND...')
        run_diamond(args.faa)
        args.tsv = io.change_extension(args.faa, 'tsv')
        console.print_to_system('BLASTP results saved as ' + args.tsv)
    database = io.read_tsv(args.tsv)
    database = remove_self_hits(database)

    if args.threshold is None:
        console.print_to_system('No threshold provided; calculating custom threshold...')
        threshold = calculate_threshold(database)
    else:
        threshold = args.threshold

    if args.histogram is True:
        console.print_to_system('Plotting histogram...')
        filename = 'histogram_' + io.change_extension(args.tsv, 'html')
        plot.plot_histogram(database.loc[:, "identity"], filename)
        console.print_to_system('Histogram saved as ' + filename)

    database = remove_data_under_threshold(database, threshold)

    print_list = args.nodelist

    filename = io.change_extension(args.tsv, 'html')
    protein_network = generate_network(database, filename, print_list)
    console.print_to_system('Network saved as ' + filename)

    if args.node is not None:
        for node in args.node:
            nodes = network.get_subnetwork_nodes(node, protein_network)
            node_database = extract_nodes(nodes, database)
            filename = io.change_extension(node, 'html')
            generate_network(node_database, filename, print_list)
            console.print_to_system('Network saved as ' + filename)

    console.print_to_system('Networker has finished its analysis!')

if __name__ == "__main__":
    main()
