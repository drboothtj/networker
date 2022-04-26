'''
Read and write files

Functions:
    read_tsv(database_file) -> database
    write_to_file(write_lines, write_name)
'''
import pandas as pd

def read_tsv(database_file):
    '''Read a TSV file to a pandas dataframe'''
    database = pd.read_csv(database_file, sep='\t', header=None)
    database.columns = ['query', 'subject', 'identity']
    return database

def write_to_file(write_lines, write_name):
    '''Write a list line by line into a new file'''
    file = open(write_name, "a")
    for line in write_lines:
        file.write(line + '\n')
    file.close()
