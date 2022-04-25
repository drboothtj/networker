#networker version 0.1.0 by Dr. Thom Booth

#Import the following:
import sys
import subprocess
import numpy as np
import pandas as pd
from datetime import datetime
from pyvis.network import Network

#Define functions

#function for printing to console
def print_to_system(string_to_print):
    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S]: ")
    print(current_time + string_to_print)

def write_to_file(write_lines, write_name):
    file = open(write_name, "a")
    for line in write_lines:
        file.write(line + '\n')
    file.close()

def run_in_command_line(command):
    command = command.split(" ")
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    process.communicate()
    return process

#Check the required arguments
def check_arguments(arguments):
    number_of_arguments = len(arguments)
    if number_of_arguments > 2:
        print_to_system("ERROR: Too many arguments! Please provide only the filename.")
        quit()
    elif number_of_arguments < 2:
        print_to_system("ERROR: Too few arguments! Please provide the filename.")
        quit()
    else:
        print_to_system("Creating a network from " + arguments[1] + "...")
        return arguments[1]

def handle_files(filename):
    extension = filename.split('.')[1]
    if extension == 'faa':
        make_diamond_database(filename)
        run_diamond_search(filename)
        filename = filename.split('.')[0] + ".tsv"
    elif extension != 'tsv':
        print_to_system("ERROR: Please provide files with the extension .faa or .tsv only.")
        quit()
    return(filename)

#create a diamond database from the .faa
def make_diamond_database(filename):
    print_to_system('Making DIAMOND database...')
    makedb = "diamond makedb"
    input_ = " --in " + filename + ""
    database = " --db " + filename.split('.')[0] + ".dmnd"
    command = makedb + database + input_
    run_in_command_line(command)

#run blastp
def run_diamond_search(filename): ##neaten this code!
    print_to_system('Running DIAMOND blastP...')
    blastp = "diamond blastp"
    query = " --query " + filename
    database = " --db " + filename.split('.')[0] + ".dmnd"
    output = " --out " + filename.split('.')[0] + ".tsv"
    outfmt = " --outfmt 6 qseqid sseqid pident"
    command = blastp + database + query + output + outfmt
    run_in_command_line(command)

#Read the database file and clean the data
def read_tsv(database_file):
    #read the tsv
    print_to_system("Reading " + database_file + "...")
    database = pd.read_csv(database_file, sep='\t', header=None)
    database.columns = ['query', 'subject', 'identity']
    print_to_system("Read " + database_file + "!")
    return database

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
    return database

#Calculate the identity cut off to provide on average 3 edges per node from the provided database
def calculate_threshold(database):
    print_to_system("Calculating identity hreshold...")
    number_of_queries = database['query'].nunique()
    reccommended_cut_off = len(database.index) - (number_of_queries*3)
    #We will now use a histogram to calculate the threshold
    database_size = len(database.index)
    counts, bins = np.histogram(database.loc[:, "identity"], bins=database_size)
    for i in np.cumsum(counts):
        if  i > reccommended_cut_off:
            threshold = bins[i]
            break
    print_to_system("Recommended threshold calculated at " + str(threshold) + "% identity.")
    return threshold

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
    print_to_system(str(size_before - size_after) + " hits below the threshold and have been removed!")
    return database

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
    for edge in edge_data:
        source = edge[0]
        destination = edge[1]
        weight = edge[2]
        prot_net.add_node(source, source, title=source)
        prot_net.add_node(destination, destination, title=destination)
        prot_net.add_edge(source, destination, value=weight)
    #Add neihbour info and colour nodes. Also build a list of nodes to be output.
    neighbor_map = prot_net.get_adj_list()
    node_list = []
    for node in prot_net.nodes:
        node_list.append(node['id'])
        numberofneighbours = len(neighbor_map[node['id']])
        node['title'] += '<br>' + str(numberofneighbours) + ' neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
        node['value'] = numberofneighbours
        if colourme in node['id']:
            node['color'] = 'red'
    #save and show the network with an appropriate name
    net_name = sys.argv[1].split('.')[0] + '.html'
    prot_net.show(net_name)
    #save node list
    nodes_name = sys.argv[1].split('.')[0] + '.txt'
    write_to_file(node_list, nodes_name)
    print_to_system("Network saved as " + net_name + "!")
    print_to_system("A list of nodes has been saved as " + nodes_name + "!") 
      
###Workflow###
def main():
    #Print welcome message
    print_to_system("Running Networker version 0.0.1")
    #Get the argument
    filename = check_arguments(sys.argv)
    #Handle the files an process apropriately.
    filename = handle_files(filename)
    #Read the supplied database file as database
    database = read_tsv(filename)
    #remove self hits from the database
    database = remove_self_hits(database)
    #using the data in database calculate an appropriate identity threshold for the network
    threshold = calculate_threshold(database)
    #remove data from database below the threshold
    database = remove_data_under_threshold(database, threshold)
    #generate the network
    generate_network(database)

###run script!###
if __name__ == "__main__":
    print('Sucess!')
