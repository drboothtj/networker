#networker version 0.0.1 by Dr. Thom Booth

#Import the following:
import sys
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pyvis.network import Network
from Bio import SeqIO

#Define functions

#function for printing to console
def print_to_system(string_to_print):
    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S]: ")
    print(current_time + string_to_print)

def write_to_file(write_lines, write_name):
    f = open(write_name, "a")
    for line in write_lines:
        f.write(line + '\n')
    f.close()         

#Check the required arguments
def check_arguments(arguments):
    number_of_arguments = len(arguments)
    if number_of_arguments > 2:
        print("Too many arguments!")
        quit()
    elif number_of_arguments < 0:
        print("Too few arguments!")
        quit()
    else:
        print_to_system("Creating a network from " + arguments[1] + "...") 

#Read the database file and clean the data
def read_tsv(database_file):
    #read the tsv
    print_to_system("Reading " + database_file + "...")
    database = pd.read_csv(database_file, sep='\t', header=None)
    database.columns = ['query','subject','identity']
    print_to_system("Read " + database_file + "!")
    return(database)
    

#Clean the data from selfhits and set an appropriate threshold 
def remove_self_hits(database):
    #first remove self hits
    print_to_system("Removing self hits...")
    self_hits = []
    for i in database.index:
            query = database['query'][i]
            subject = database['subject'][i]
            if query == subject:
                self_hits.append(i)
    size_before = len(database.index)
    database = database.drop(self_hits)
    size_after = len(database.index)
    self_hits_count = str(size_before - size_after)
    print_to_system("Removed " + self_hits_count + " self hits!")
    return(database)

#Calculate the identity cut off to provide on average 5 edges per node from the provided database
def calculate_threshold(database):
    print_to_system("Calculating identity hreshold...")
    number_of_queries = database['query'].nunique()
    reccommended_cut_off = len(database.index) - (number_of_queries*5) #we want to exclude until we have n queries*3
    #We will now use a histogram to calculate the threshold
    database_size = len(database.index)
    counts, bins = np.histogram(database.loc[:,"identity"], bins=database_size) #each entry has a bin
    threshold = bins[reccommended_cut_off]
    print_to_system("Recommended threshold calculated at " + str(threshold) + "% identity.")
    return(threshold)

#remove anything below the define identity threshold from the database
def remove_data_under_threshold(database, threshold):
    print_to_system("Removing all hits below " + str(threshold) + "% identity...")
    below_threshold = []
    for i in database.index:
        identity = float(database['identity'][i])
        if identity < threshold:
            below_threshold.append(i)
    size_before = len(database.index)
    database = database.drop(below_threshold)
    size_after = len(database.index)
    return(database)
    print_to_system(str(size_before - size_after) + " hits fall below the threshold and have been removed!")

#Generate the protein identity network from the remaining data.            
def generate_network(database):
    print_to_system("Generating network...")
    colourme = 'BGC' #nodes starting with this string will be colored red
    #Create the empty network
    prot_net = Network(height='100%', width='75%', bgcolor='white', font_color='black')
    prot_net.barnes_hut()
    prot_net.show_buttons(filter_=True)
    #parse database 
    sources = database['query']
    targets = database['subject']
    weights = database['identity']
    edge_data = zip(sources, targets, weights)
    #build database from parsed data
    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]
        prot_net.add_node(src, src, title=src)
        prot_net.add_node(dst, dst, title=dst)
        prot_net.add_edge(src, dst, value=w)
    #Add neihbour info and colour nodes. Also build a list of nodes to be output.
    neighbor_map = prot_net.get_adj_list()
    node_list = []
    for node in prot_net.nodes:
        node_list.append(node['id'])
        numberofneighbours = len(neighbor_map[node['id']])
        node['title'] += '<br>' + str(numberofneighbours) + ' neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
        node['value'] = numberofneighbours
        if (colourme in node['id']):
            node['color'] = 'red'
    #save and show the network with an appropriate name
    net_name = sys.argv[1].split('.')[0] + '.html'
    prot_net.show(net_name)
    nodes_name = sys.argv[1].split('.')[0] + '.txt'
    write_to_file(node_list, nodes_name)
    print_to_system("Network saved as " + net_name + "!")
    print_to_system("A list of nodes has been saved as " + nodes_name + "!") 
      
###Workflow###

#Print welcome message
print_to_system("Running Networker version 0.0.1") 

#Check the required arguments are present
check_arguments(sys.argv)

#Read the supplied database file as database
database = read_tsv(sys.argv[1])

#remove self hits from the database
database = remove_self_hits(database)

#using the data in database calculate an appropriate identity threshold for the network
threshold = calculate_threshold(database)

#remove data from database below the threshold
database = remove_data_under_threshold(database, threshold)

#generate the network
generate_network(database)
    
    
