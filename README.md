# networker

## Description

This repository contains scripts to create and analyse protein identity networks.

## Scirpts

### 1. networker.py
**Usage:**
`python networker.py diamondorblastdatabase.tsv`

If provided with a DIAMOND or BLAST database, 'networker.py' will produce a protein identity network ('xxx.html'). It is recommended to make an all-vs-all comparison. 
The output must have the format: `qseqid | sseqid | pident`

For example, to make a usable DIAMOND search:

`diamond makedb --db example --in example.faa`

`diamond blastp --db example --query example.faa --out example.tsv --outfmt 6 qseqid sseqid pident`

All steps are currently automatic, including thresholding. However, the recommended threshold should work for most putposes. In future, you will be able to provide a custom threshold.

### 2. subnetworker.py 
WIP

### 3. histogramer.py
WIP

## To Do
1. Add a wrapper so that the input can be simplified to a fasta file.
2. Enable custom thresholds.
3. Create 'histogramer.py' to assist with threshold analysis.
4. Write the network file in a readable format.
5. Create 'subnetworker.py' for analysing subnetworks. 
6. Compile into software package.

