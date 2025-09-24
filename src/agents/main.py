import sys
from crew import RecamCrew
from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint
from pathlib import Path
import json
import os
import argparse

from key_info.key_info import key_info

# ------------------------------ Environment Variables ------------------------------
load_dotenv()

# ------------------------------ Args ------------------------------
parser = argparse.ArgumentParser(
    description='''
    This takes in a PDF file and performs a causality assessment of DILI using the selected algorithm.
    Fout agents will be used to perform the causality assessment. DILI informatician will extract the 
    information from the PDF file. DILI analyst will perform the causality assessment. DILI writer will 
    write the report. DILI expert will review the report.
    '''
)

parser.add_argument("--input-pdf",
                    required=True,
                    dest="input_pdf",
                    help="Path to a input PDF file containing the case report.")

parser.add_argument("--algorithm",
                    required=True,
                    dest="algorithm",
                    choices=["RECAM", "RUCAM"],
                    help="Algorithm to use for DILI causality assessment.")

parser.add_argument("--output-dir",
                    required=True,
                    dest="output_dir",
                    help="Path to a output directory.")

args = parser.parse_args()

if __name__ == "__main__":

    if args.algorithm == "RECAM":
        score_calculator_tool = "RECAM Score Calculator"

    inputs = {
        'input_pdf': args.input_pdf,
        'date': datetime.now().strftime('%Y-%m-%dT%H-%M-%S'),
        'algorithm': args.algorithm,
        'key_info': key_info[args.algorithm],
        'score_calculator_tool': score_calculator_tool,
        'output_dir': args.output_dir,
    }

    pprint(f"{inputs=}")

    results = RecamCrew().crew().kickoff(inputs=inputs)
