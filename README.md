# networker

## Description
`networker` is a python package for building and analysing protein similarity networks.

## Installation
`networker` can be installed with:

`pip install networker`

It has the following dependencies that will be installed automatically:
1. numpy
2. pandas
3. pyvis
4. plotly

It also uses DIAMOND, which must be installed seperatly.

## Usage
`networker` will take an input file and produce an interactive network. It can take either a fasta amino acid file (.faa) or a tab seperated values file (.tsv) as input.

### Usage Case 1: Create a protein network from a fasta file
The simplest method for using `networker` is to provide a .faa file. This can be done as follows:

`networker --faa file.faa`

This will produce a diamond database (file.dmnd) and run a BLAST search to produce file.tsv. It will then use these results to produce a similarity network (file.html). Given that no threshold was provided, it will also automatically calculate an appropriate identity threshold. See the next case for examples of using a custom threshold.

### Usage Case 2: Creat a protein network from tab seperated values using a custom threshold
If a .tsv containing blastp results already exists, this can be used as input. It is important that the .tsv is in the correct format. It is creates specifcially from DIAMOND using the flag `--outfmt 6 qseqid sseqid pident`. This reprisents a three column table consisting of: the query sequence id, the subject query id and the percentage identity. 

If you do not want `networker` to calculate a threshold, you can provide a custom threshold using the flag `-th` or `--threshold`. The threshold is contained as a float.

`networker --tsv file.tsv --threshold 75.25`

### Usage Case 3: Print histogram and a list of nodes
To produce a histogram showing the cummulative number of edges versus identity threshold add the flag `-hi` or `--histogram`. This can aid in deciding suitable thresholds for your dataset. To print a list of nodes from the network add the flag `-nl` or `--node_list`.

Therefore:

`networker --faa file.faa -hi -nl`

will produce file.tsv, file.dmnd and file.html as above, but also the node list (file.txt) and the histogram (histogram_file.html).

### Usage Case 4: Generate sub-networks form a list of nodes

You can also use `networker` to produce individual networks and node lists for each subwork in a given network by providing a list of node names using the `-n` or `node` flag. 

`networker --tsv file.tsv -n node1 node2 node3 -nl`

This will produce a network based on file.tsv (file.html), individual networks for each subnetwork containing the specified nodes (node1.hmtl, node2.hmtl and node3.hmtl) and, node lists for the individual nodes and the whole network (file.txt, node1.txt, node2.txt and node3.txt).

### Usage Case 5: Custom Colouring of Nodes
Coming in version 0.3.0; work in progress.

## Example Data
The example_data contains a test data set and the outputs from networker. 

The test dataset (SMCOG1119.faa) was extracted from the [MIBiG database](https://mibig.secondarymetabolites.org/). It is a collection of protein sequences reprisenting all annotated halogenases from the database. 

Firstly, `networker` was run on the dataset as follows:

`networker -f SMCOG119.faa -hi -nl -th 60`

This ran the diamond search (SMCOG1119.dmnd and SMCOG1119.tsv) and printed the threshold histogram (histogram_SMCOG1119.html), the list of nodes in the network (SMCOG1119.txt) and the network itself (SMCOG1119.html). The console output can be viewed in log_1.txt.

A second analysis was run to extract the largest subnetworks. 

`networker -f SMCOG119.faa -nl -th 60 -node BGC0001288 BGC0000822 BGC0001334 BGC0001459`

This will run as previously but will also output individual nodelists and networks for the nodes specified (BGC0001288.txt, BGC0001288.html, BGC0000822.html, BGC0000822.html ...)

## To Do
1. Enable custom coloring of nodes.
2. Select reprisentative nodes of subnetworks

