#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from my_financial_researcher.crew import MyFinancialResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'company': 'Tesla',
    }
    
    try:
        result = MyFinancialResearcher().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

