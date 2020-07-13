#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'Alban Mathieu'
__date__ = '10-07-2020'

import sys
import argparse
import textwrap
#import pandas as pd
#import requests as rq
from pathlib import Path
#from bs4 import BeautifulSoup as bs
from Bio import SeqIO
#####################################
def warn(msg):
    """Utils: print a warning
    """
    print(f"\033[93m{msg}\033[0m")

##########################################################################
#surveys_df = pd.read_csv(f, sep = ",")
def read_sample_data(query:Path=None):
    """Read input sample file.
    """
    if query is None:
        raise Exception("query is empty.")
    if not query.is_file():
        raise Exception(f"query file '{query}' does not exist.")
    data = None
    with query.open('rb') as f:
        data = [line.decode("utf-8") for line in f]
    return data

##########################################################################
def read_fasta(fasta:Path=None):
    """Read input fasta file.

    """
    mdata = None
    if fasta is None:
        warn("fasta filepath is empty.")
        #fasta_data = []
    else:
        if not fasta.is_file():
            raise Exception(f"fasta file '{fasta}' does not exist.")
        with SeqIO.parse(fasta, "fasta") as f:
            #fasta_data = [seq for seq in f]
            for seq in f:
                yield seq #créé un générateur , n'est plus une focntion et ne charge pas en mem
    #return fasta_data

##########################################################################
def write_result(output:Path=None, result_data=None):
    """Write end results to file
    """
    if output is None:
        raise Exception("output is empty.")
    if result_data is None:
        raise Exception("Result dataset is empty.")
    with open(output, "w") as output_handle:
        SeqIO.write(result_data, output_handle, "fasta")

##########################################################################
def process_sample(query:Path=None, fasta:Path=None, results_dir:Path=None):
    """Main process

    Create a new fasta file based on query ids.
    """

    # result var
    final_results = []

    # fasta
    #fasta = read_fasta(fasta = fasta) peut pas faire comme ca comme c'est un générateur

    # result file
    result_output = results_dir.joinpath(f"{output.stem}.fasta")

    # sample data
    query_data = read_sample_data(query = query)

    # parsing
    ## dans la liste des ID de fasta
    for fasta in read_fasta(fasta = fasta):
        str1 = fasta.id.split(" ")[0].strip()
        ## est ce que je l'ai dans ma liste d'interêt
        if str1 in query_data:
            # je veux stocker l'id et la sequence, mais est ce que ca va garder le format fasta pour le SeqIO.write?
            final_results.append(fasta) # (()) pas ca sinon interpreté tuple
    # write result
    write_result(output=result_output,result_data=final_results)


##########################################################################
def get_argparser():
    """Create the argument parser
    """
    parser = argparse.ArgumentParser(prog = "Parse and filter fasta",
                                     add_help=True,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent("""\
    extract fasta sequences based on list of reads id
    """))
    # attr
    parser.add_argument("-q", "--query", type=str, help="A path to the read id list", required=True)
    parser.add_argument("-f", "--fasta", type=str, help="A path to the fasta file", required=True)
    parser.add_argument("-o", "--output",type=str, help="A path to results file", required=True)
    #
    return parser




def main(*args, **kwargs):
    """Main function
    """

    # create result dir
    res_dir = write_result(kwargs["output"])
    # exec
    process_sample(query=kwargs["query"],
                   fasta=kwargs["fasta"],
                   results_dir=res_dir)
    # yay
    print(f"fasta selection '{kwargs['query']}' done.")

if __name__ == '__main__':
    # build arg parser, top level parser
    parser = get_argparser()

    # parse arguments
    parsed_args, _ = parser.parse_known_args()

    # args and kwargs
    kw = {
        "query": Path(parsed_args.query) if parsed_args.query is not None else None,
        "fasta": Path(parsed_args.fasta) if parsed_args.fasta is not None else None,
        "output": Path(parsed_args.output) if parsed_args.output is not None else None,
    }
    # exec
    main(**kw)
