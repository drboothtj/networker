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

### Usage Case 3: Print Histogram
WIP

### Usage Case 4: Custom Colouring of Nodes
WIP


## Example Data
Example data and output can be found in the example_data folder. The file example.faa was used to generate the DIAMOND database and, subsequentally, the network ('example.html') and the node list ('example.txt').

## To Do
1. Specify node for subnetwork analysis.
2. Enable custom coloring of nodes.
3. Use nodes list to extract regions.
4. Create -hi --histogram to print histogram
5. Update example data


