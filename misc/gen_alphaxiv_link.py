import requests
from tqdm import tqdm
import sys

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

def gen_markdown(paper_names, alphaxiv_list):
    texts = []
    for i in range(len(paper_names)):
        if alphaxiv_list[i] is None:
            texts.append("- " + paper_names[i])
        else:
            line = "- [" + paper_names[i] + "]" + "(" + alphaxiv_list[i] + ")"
            texts.append(line)
    writestr("all_papers.md", texts)

def get_all_paper_links(paper_names):
    alphaxiv_list = []
    for paper in tqdm(paper_names, total=len(paper_names), desc="Fetch links"):
        if "]" in paper:
            paper = paper[paper.index(']')+1:paper.index('.')]
        alphaxiv_id = fetch_alphaxiv_link(paper)
        alphaxiv_list.append(alphaxiv_id)
    return alphaxiv_list

if __name__ == "__main__":
    filename = sys.argv[1]
    paper_names = loadstr(filename, converter=str)
    alphaxiv_list = get_all_paper_links(paper_names)
    gen_markdown(paper_names, alphaxiv_list)
