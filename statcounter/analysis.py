import numpy as np
import pandas as pd
import sys
sys.path.append("/home/gcao/Projects/retrieval/misc")
from fileproc import loadstr

def main():
    csv = pd.read_csv('logs.csv')
    csv = csv[csv["IP Address"]!="78.73.133.16"]
    csv = csv.drop(columns=["Visitor Label","Web Page","Referring Link","Search Keywords","Type","Google Ranking","Original Link"])
    print(csv)

if __name__ == '__main__':
    main()
