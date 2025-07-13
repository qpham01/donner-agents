#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from my_coder.crew import MyCoder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

assignment = "Write a python program that calculates the first {count} terms \
    of this series, multiplying the total by 4: 1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ... \
    for the unit test validate to 2 decimal places only."

def run():
    """
    Run the crew.
    """
    inputs = {'assignment': assignment, 'count': 100}
    
    try:
        result = MyCoder().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
