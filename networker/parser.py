#imports
import argparse

#create the parser
parser = argparse.ArgumentParser(
    "networker",
    description="networker:  a python package to generate and analyse protein similarity networks.",
    epilog="Written by Dr. Thom Booth, 2022."
    )

#create arguments
parser.add_argument(
    '-f',
    '--faa',
    nargs='?',
    default=None,
    help='path to a fasta file containing amino acid sequences'
    )
parser.add_argument(
    '-t',
    '--tsv',
    nargs='?',
    default=None,
    help='path to a .tsv containing BLASTP results'
    )
parser.add_argument(
    '-n',
    '--node',
    nargs='?',
    default=None,
    help='the name of a node for subnetwork analysis'
    )
parser.add_argument(
    '-th',
    '--threshold',
    nargs='?',
    default=None,
    help='custom identity threshold'
    )

args = parser.parse_args()
print(args.faa)
print(args.tsv)
print(args.node)
    