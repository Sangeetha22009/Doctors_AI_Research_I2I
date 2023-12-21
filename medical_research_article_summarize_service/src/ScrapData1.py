import logging
import os
import openai
from paperscraper.pubmed import get_and_dump_pubmed_papers
from llama_index import VectorStoreIndex
from llama_index.node_parser import SimpleNodeParser
from paperscraper.pdf import save_pdf_from_dump
from datetime import datetime

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
# openai.api_key  = os.environ['OPENAI_API_KEY']
os.environ["OPENAI_API_KEY"] = ""
openai_api_key = os.environ.get('OPENAI_API_KEY')

from llama_index import(
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    TreeIndex,
    load_index_from_storage
)

from llama_index.response_synthesizers import (
    ResponseMode,
    get_response_synthesizer,
)
response_synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.COMPACT
)

start_dates = '2023/01/01'      
end_dates = '2023/01/02'
modified_start_date = start_dates.replace('/', '_')
modified_end_date = end_dates.replace('/', '_')
currentDirectory = os.getcwd()
selectedCategoreies = ['Omicron']
categoryFileName = '-'.join(selectedCategoreies)
categoryPdfFileName = categoryFileName + modified_start_date + modified_end_date + '.pdf'
categoryDirectory = os.path.join(currentDirectory, categoryPdfFileName)
output_filepath = categoryFileName + modified_start_date + modified_end_date+ '.jsonl'
summarizedPrompt = "Please generate a concise summary, focusing on the main arguments, conclusions, and significant details within the document. The summary should be clear and informative, providing a condensed overview of the paper's content"
questionsOnSummary = "What are all the references used"
retrieved_index = ""
summarizedResponse = ""


def getdirectory():
    if not os.path.exists(categoryDirectory):
     os.makedirs(categoryDirectory)
     print(f"Directory '{categoryDirectory}' created successfully.")
    else:
     print(f"Directory '{categoryDirectory}' already exists.")

def fetch_papers_for_categories(selectedCategoreies):
    try:
        getdirectory()   
    # Check if the file exist
        print(output_filepath)
        if os.path.exists(output_filepath):
            print(f"The file '{selectedCategoreies}' exists.")
        else:
            get_and_dump_pubmed_papers(selectedCategoreies, output_filepath,start_date=start_dates, end_date=end_dates)
            save_pdf_from_dump(output_filepath, pdf_path=categoryDirectory, key_to_save='doi')
        response = store_data_on_llama()
        return response
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return None
    
def store_data_on_llama():
    try:
       filelists = get_files_for_summarization()
       reader = SimpleDirectoryReader(input_files= filelists)
       pdf_documents = reader.load_data()
       pdf_index = VectorStoreIndex.from_documents(pdf_documents)
       pdf_index.storage_context.persist(persist_dir="persist_index")
       storage_context = StorageContext.from_defaults(persist_dir="persist_index")
       retrieved_index = load_index_from_storage(storage_context)
       query_engine = retrieved_index.as_query_engine()
    #    result = saveResponse("Summary" + query_engine.query(summarizedPrompt).response)
       result = query_engine.query(summarizedPrompt)
       print(result)
       return result
    #    saveResponse("Questionnaire" + query_engine.query(questionsOnSummary).response)
       
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return None


def get_files_for_summarization():
    try:
        
      filelists = []
      files_list = os.listdir(categoryDirectory) 
      for file_name in files_list:
          file_path = os.path.join(categoryDirectory, file_name)
          if os.path.isfile(file_path):  # Check if it's a file
           file_size = os.path.getsize(file_path)
           if not file_size > 500 * 1024:
               filelists.append(file_path)
      
      return filelists
       
    except Exception as e:
        print(f"Error getting files : {e}")
        return None
    
def saveResponse(summarizedResponse):
    try:
       
       file_name = "Repsone.txt"
       new_file_path = os.path.join(categoryDirectory, file_name)
       if not os.path.exists(new_file_path):
        with open(new_file_path, 'w') as file:
         file.write(summarizedResponse)
       else:
        with open(new_file_path, 'a') as file:
         file.write(summarizedResponse)   
        
    except Exception as e:
        print(f"Error Saving papers: {e}")
        return None
    
def query_indexed_data(query_from_summarizer):
    try:
        storage_context = StorageContext.from_defaults(persist_dir="persist_index")
        retrieved_index = load_index_from_storage(storage_context)
        query_engine = retrieved_index.as_query_engine()
        query_response = query_engine.query(query_from_summarizer)
        return query_response
    #    print(response)
    except Exception as e:
        logging.error(f"exception occurred {e}")
        
# getdirectory()    
# fetch_papers_for_categories(selectedCategoreies)




