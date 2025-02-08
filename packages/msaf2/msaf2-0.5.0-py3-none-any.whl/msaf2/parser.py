import argparse

parser = argparse.ArgumentParser()
conf_group = parser.add_mutually_exclusive_group()
conf_group.add_argument("-c", "--config", help="configuration file, yaml format")
conf_group.add_argument("--generate", help="Create a template.yaml configuration file", action='store_true')

main_group = parser.add_mutually_exclusive_group()
main_group.add_argument("--pdqt", help="archive specified directory as a pdqt file", nargs=1)
main_group.add_argument("--query", help="the fasta files to query", nargs='+')
main_group.add_argument("--merge", help="the msa files to merge", nargs='+')

parser.add_argument("--bp", help="target databases group blueprint")
parser.add_argument("--list", help="list available databases to query OR MSA to merge", action='store_true')
parser.add_argument("-p", "--pthread", help="worker threads cap", type=int, default=5)
parser.add_argument("--output", help="result writing folder", default="msas")
parser.add_argument("-v", "--verbosity", type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO',
                    help="increase output verbosity")
parser.add_argument("-w", "--warn", help="Detailed warnings file", default="msaf2.warnings")
parser.add_argument("-q", "--quiet", help="Don't log detailed warning", action='store_true')
parser.add_argument("--into", help="the resulting merged msa files [sto or a3m]", type=str, default="merged_msa.a3m")
