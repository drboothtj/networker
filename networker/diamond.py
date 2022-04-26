from networker import console

def make_diamond_database(filename):
    console.print_to_system('Making DIAMOND database...')
    makedb = "diamond makedb"
    input_ = " --in " + filename + ""
    database = " --db " + filename.split('.')[0] + ".dmnd"
    command = makedb + database + input_
    console.run_in_command_line(command)

def run_diamond_search(filename):
    console.print_to_system('Running DIAMOND blastP...')
    blastp = "diamond blastp"
    query = " --query " + filename
    database = " --db " + filename.split('.')[0] + ".dmnd"
    output = " --out " + filename.split('.')[0] + ".tsv"
    outfmt = " --outfmt 6 qseqid sseqid pident"
    command = blastp + database + query + output + outfmt
    console.run_in_command_line(command)