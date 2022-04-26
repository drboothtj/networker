'''
Make DIAMOND databases and run searches using DIAMOND

Functions:
make_diamond_database(filename)
run_diamond_search(filename)

'''
from networker import console

def make_diamond_database(filename):
    '''Create a DIAMOND database from a fasta file'''
    makedb = "diamond makedb"
    input_ = " --in " + filename + ""
    database = " --db " + filename.split('.')[0] + ".dmnd"
    command = makedb + database + input_
    console.run_in_command_line(command)

def run_diamond_search(filename):
    '''Run BLASTP through DIAMOND'''
    blastp = "diamond blastp"
    query = " --query " + filename
    database = " --db " + filename.split('.')[0] + ".dmnd"
    output = " --out " + filename.split('.')[0] + ".tsv"
    outfmt = " --outfmt 6 qseqid sseqid pident"
    command = blastp + database + query + output + outfmt
    console.run_in_command_line(command)
