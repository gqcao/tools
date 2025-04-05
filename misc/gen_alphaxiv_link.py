import requests
from tqdm import tqdm
import sys
import os
import re
from pdb import set_trace

# load text one line at a time..
def loadstr(filename,converter=str):
    return [converter(c.strip()) for c in open(filename).readlines()]

def writestr(filename,texts):
    with open(filename, 'w') as outfile:
        for i in range(len(texts)):
            line = str(texts[i]) + '\n'
            outfile.write(line)

def replace_with_alphaxiv_url(arxiv_id):
    alphaxiv_id = arxiv_id.replace("arxiv", "alphaxiv")
    return alphaxiv_id

def fetch_alphaxiv_link(paper_title):
    # Define the arXiv API query URL with the title search
    url = f'http://export.arxiv.org/api/query?search_query=ti:"{paper_title}"&start=0&max_results=1'
    response = requests.get(url) 
    alphaxiv_id = None 
    if response.status_code == 200:
        # Parse the response
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.content)
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id').text
            alphaxiv_id = replace_with_alphaxiv_url(arxiv_id)
        return alphaxiv_id 
    else:
        print("Paper not found on arXiv")
        return None

def remove_arxiv_if_exists(paper_name):
    file_path = os.environ.get("HOME")  + "/Dropbox/papers/" + paper_name
    if os.path.isfile(file_path):
        try:
            # Remove the file
            os.remove(file_path)
            print(f"File '{file_path}' has been removed.")
        except Exception as e:
            print(f"Error removing file: {e}")

def gen_markdown(paper_names, alphaxiv_list, filename):
    texts = []
    for i in range(len(paper_names)):
        if alphaxiv_list[i] is None:
            line = "- [" + paper_names[i] + "]" + "("+ os.environ.get("HOME")  + "/Dropbox/papers/" + paper_names[i] + ")"
            texts.append(line)
        else:
            line = "- [" + paper_names[i] + "]" + "(" + alphaxiv_list[i] + ")"
            texts.append(line)
            remove_arxiv_if_exists(paper_names[i])
    writestr(filename.split('.')[0] + ".md", texts)

def get_all_paper_links(paper_names):
    alphaxiv_list = []
    for paper in tqdm(paper_names, total=len(paper_names), desc="Fetch links"):
        paper = paper.rstrip(".pdf")
        if "arXiv" in paper:
            alphaxiv_id = "http://alphaxiv.org/abs/" + paper[paper.index('_')+1:]
        else:
            paper = re.findall(r'\b[a-zA-Z]+\b', paper)
            paper = ' '.join(paper)
            alphaxiv_id = fetch_alphaxiv_link(paper)
        alphaxiv_list.append(alphaxiv_id)
    return alphaxiv_list

if __name__ == "__main__":
    filename = sys.argv[1]
    paper_names = loadstr(filename, converter=str)
    alphaxiv_list = get_all_paper_links(paper_names)
    gen_markdown(paper_names, alphaxiv_list, filename)
