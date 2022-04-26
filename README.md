# networker

## Description

This repository contains scripts to create and analyse protein (or nucleotide) identity networks.

## Scirpts

### 1. networker.py
**Usage:**

`python networker.py proteinseqs.faa`

or,

`python networker.py diamondorblastdatabase.tsv`

If provided with a DIAMOND or BLAST table (.tsv), or an amino acid fasta file (.faa) 'networker.py' will produce a protein/nucleotide identity network ('xxx.html') and a list of nodes used in the network ('xxx.txt'). 

It is recommended that you use .faa as an input, however if you want to use your own table, the file must have the format: `qseqid | sseqid | pident`

For example, to make a usable DIAMOND search:

`diamond makedb --db example --in example.faa`

`diamond blastp --db example --query example.faa --out example.tsv --outfmt 6 qseqid sseqid pident`

All steps are currently automatic, including thresholding. However, the recommended threshold should work for most putposes. In future, you will be able to provide a custom threshold.

### 2. subnetworker.py 
WIP

### 3. histogramer.py
WIP

## Example Data
Example data and output can be found in the example_data folder. The file example.faa was used to generate the DIAMOND database and, subsequentally, the network ('example.html') and the node list ('example.txt').

## To Do
1. Specify node for subnetwork analysis.
2. Enable custom coloring of nodes.
3. Use nodes list to extract regions.
4. Create 'histogramer.py' to assist with threshold analysis.
5. Update example data
