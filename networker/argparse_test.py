#imports
import argparse 
import sys

parser = argparse.ArgumentParser("networker", description="networker:  a python package to generate and analyse protein similarity networks.", epilog="Written by Dr. Thom Booth, 2022.")
parser.add_argument('-t', '--test', action='store_true', help='you should not see this option >:(')

args = parser.parse_args()
print(args.test)


    