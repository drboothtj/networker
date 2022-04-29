'''
Read and write files

Functions:
    change_extension(filename, new_extension) -> new_filename
    read_tsv(database_file) -> database
    write_to_file(write_lines, write_name)
'''
import pandas as pd

def change_extension(filename, new_extension):
    '''Takes a file name and changes the extension to the string provided'''
    new_filename = filename.split('.')[0] + '.' + new_extension
    return new_filename

def read_tsv(database_file):
    '''Read a TSV file to a pandas dataframe'''
    database = pd.read_csv(database_file, sep='\t', header=None)
    database.columns = ['query', 'subject', 'identity']
    return database

def write_to_file(filename, write_lines):
    '''Write a list line by line into a new file'''
    file = open(filename, "a")
    for line in write_lines:
        file.write(line + '\n')
    file.close()
