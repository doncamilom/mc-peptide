from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
from mitosheet.streamlit.v1.spreadsheet import _get_mito_backend

import streamlit as st
import pdf2doi
import os
import tempfile
from paper import Paper
import requests


st.set_page_config(layout="wide")


@st.cache_data
def get_dataset():
    df = pd.read_csv(
        "http://cycpeptmpdb.com/static//download/peptides/CycPeptMPDB_Peptide_All.csv"
    )
    df = df[
        [
            "CycPeptMPDB_ID",
            "Source",
            "Year",
            "Original_Name_in_Source_Literature",
            "SMILES",
            "Permeability",
            "Same_Peptides_ID",
            "Same_Peptides_Source",
            "Same_Peptides_Permeability",
            "Same_Peptides_Assay",
        ]
    ]
    return df


# Title
st.title("📂 Dataset")
st.caption("LLM Hackathon for Materials & Chemistry - EPFL Hub")



df = get_dataset()

new_dfs, code = spreadsheet(df)
# code = code if code else "# Edit the spreadsheet above to generate code"
st.code(code)


def clear_mito_backend_cache():
    _get_mito_backend.clear()


# Function to cache the last execution time - so we can clear periodically
@st.cache_resource
def get_cached_time():
    # Initialize with a dictionary to store the last execution time
    return {"last_executed_time": None}


def try_clear_cache():

    # How often to clear the cache
    CLEAR_DELTA = timedelta(hours=12)

    current_time = datetime.now()
    cached_time = get_cached_time()

    # Check if the current time is different from the cached last execution time
    if (
        cached_time["last_executed_time"] is None
        or cached_time["last_executed_time"] + CLEAR_DELTA < current_time
    ):
        clear_mito_backend_cache()
        cached_time["last_executed_time"] = current_time


try_clear_cache()


cache_doi = st.session_state
# cache_papers = st.session_state
import copy

def recommendation_api(paper_doi):
    paper = '10.1021/acs.jmedchem.0c00013'
    url = f'https://api.semanticscholar.org/recommendations/v1/papers/forpaper/doi:{paper_doi}'
    query_params = {'fields': 'title,url,year,authors,isOpenAccess,openAccessPdf', 'limit': '5'}
    api_key = ''  # Replace with the actual API key
    headers = {'x-api-key': api_key}
    papers = []
    # Send the API request
    response = requests.get(url, params=query_params, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        for paper in  response_data['recommendedPapers']:
            paper = Paper(**paper)
            papers.append(paper)
        return papers
    else: 
        None


pdf2doi.config.set('verbose',False)
uploaded_files = st.file_uploader(
    "Upload PDF files", type="pdf", accept_multiple_files=True
)

l_btn = []
def write_table_recommendations(papers:list[Paper], org_title):
    global l_btn
    colms = st.columns((3, 1, 1,1,1),gap='small')
    fields = ["Title", 'URL', 'Year',"Authors" , "Download"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)
    # st.markdown('<style>body{border-color: white;}</style>',unsafe_allow_html=True)

    for i, paper in enumerate(papers):
        if (not paper.isOpenAcess):
            continue
        colms = st.columns((3, 1, 1,1,1),gap='small')
        col1, col2, col3, col4, col5  = colms
        col1.write(paper.title)
        col2.write(paper.url)
        col3.write(paper.year)
        col4.write(', '.join(paper.authors))
        url_pdf = paper.openAccessPdf
        if url_pdf:
            button_phold = col5.checkbox('',key=len(l_btn))  # create a placeholder
            l_btn.append({'pdf_url':url_pdf,'btn_ref':button_phold, 'title':paper.title, 'org_title': org_title})
        # button_type = "⬇️"
        # do_action = button_phold.button(button_type, key=i)
        # if do_action:
        #      button_phold.empty()  #  remove button


for uploaded_file in uploaded_files:
    st.write("filename:", uploaded_file.name)
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
            f.write(uploaded_file.getvalue())


    if not uploaded_file.name in cache_doi.keys():
        results = pdf2doi.pdf2doi(os.path.join(path))
        # results = {'identifier': 'lol'}
    else:
        results = cache_doi[uploaded_file.name]
    if results:
        with st.spinner("DOI found, looking for recommendations..."):
            if uploaded_file.name + 'papers' in cache_doi.keys():
                recommended_papers = cache_doi[uploaded_file.name+'papers']
            else:
                recommended_papers = recommendation_api(results['identifier'])

                cache_doi[uploaded_file.name+'papers'] = copy.deepcopy(recommended_papers)
        if recommended_papers:
            st.success('Recommendations found for ' +  results['identifier'])
            write_table_recommendations(recommended_papers, uploaded_file.name)
        else:
            st.error('No recommendations found for ' +  results['identifier'])

        cache_doi[uploaded_file.name] = results 


if (l_btn):
    if st.button('Download'):
        # check_if_any_enable = bne
        # if l_btn.any():
            with st.spinner('Downloading PDF files'):
                for btn_pack in l_btn:
                    if btn_pack['btn_ref']:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
                        }
                        r = requests.get(btn_pack['pdf_url'], headers=headers)
                        new_folder = f'RecommendedPDFs/{btn_pack['org_title'].replace('.pdf','')}'
                        os.makedirs(new_folder, exist_ok=True)
                        with open(f'{new_folder}/{btn_pack['title']}.pdf', 'wb') as fd:
                            fd.write(r.content)
            st.success('Files downloaded')


