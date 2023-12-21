import tiktoken
import os
from llama_index.text_splitter import SentenceSplitter
from paperscraper.pubmed import get_and_dump_pubmed_papers
from llama_index import VectorStoreIndex
from llama_index.node_parser import SimpleNodeParser
from paperscraper.pdf import save_pdf_from_dump
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

covid = ['COVID-19','SARS-CoV-2']
selectedCategoreies = '_'.join(covid)
output_filepath = '_'.join(selectedCategoreies) + '.jsonl'
os.environ["OPENAI_API_KEY"] = ""
summarizedPrompt = "Please generate a concise summary, focusing on the main arguments, conclusions, and significant details within the document. The summary should be clear and informative, providing a condensed overview of the paper's content"
questionsOnSummary = "What are all the references used"
retrieved_index = ""

def fetch_papers_for_categories(selectedCategoreies):
    try:
        
    # Check if the file exist
        if os.path.exists(output_filepath):
            print(f"The file '{selectedCategoreies}' exists.")
        else:
            start_dates = '2021/12/01'      
            end_dates = '2021/12/31'
            get_and_dump_pubmed_papers(selectedCategoreies, output_filepath,start_date=start_dates, end_date=end_dates)
            save_pdf_from_dump(output_filepath, pdf_path='.', key_to_save='doi')
        sumamrized_response = store_data_on_llama()
        return sumamrized_response
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return None
    
def store_data_on_llama():
    try:
       reader = SimpleDirectoryReader(
           input_files=["10.3233_XST-211050.pdf"]
       )
       
       pdf_documents = reader.load_data()
       
       pdf_index = VectorStoreIndex.from_documents(pdf_documents)
    
       pdf_index.storage_context.persist(persist_dir="persist_index")
       storage_context = StorageContext.from_defaults(persist_dir="persist_index")
       retrieved_index = load_index_from_storage(storage_context)
       query_engine = retrieved_index.as_query_engine()
       response = query_engine.query(summarizedPrompt)
       return response
    #    print(response)
      
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return None
    
def quest_on_summarized_Data():
    try:
       storage_context = StorageContext.from_defaults(persist_dir="persist_index")
       retrieved_index = load_index_from_storage(storage_context)
       query_engine = retrieved_index.as_query_engine()
       query_response = query_engine.query(questionsOnSummary)
       return query_response
    #    print(response)
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return None
    
# fetch_papers_for_categories(selectedCategoreies)
# store_data_on_llama()


