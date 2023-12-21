import tiktoken
import os
from llama_index.text_splitter import SentenceSplitter
from paperscraper.pubmed import get_and_dump_pubmed_papers
from llama_index.node_parser import SimpleNodeParser
from paperscraper.pdf import save_pdf_from_dump
from llama_index import(
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage
)
# from llama_index.vector_stores import DeepLakeVectorStore
import logging

covid = ['COVID-19','SARS-CoV-2']
# ai = ['Artificial intelligence', 'Deep learning', 'Machine learning']
# mi = ['Medical imaging']
selectedCategories = [covid]
output_filepath='covid19_ai_imaging.jsonl'
summarizedPrompt = "Please generate a concise summary, focusing on the main arguments, conclusions, and significant details within the document. The summary should be clear and informative, providing a condensed overview of the paper's content"
# os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""

def fetch_papers_for_categories(summarizer_categories):
    try: 
        selectedCategories = '_'.join(summarizer_categories)
        print(selectedCategories)
        output_filepath = f"{selectedCategories}.jsonl" 
        print(output_filepath)  
        # Check if the file exist
        if os.path.exists(output_filepath):
            print(f"The file '{output_filepath}' exists.")
        else:
            start_dates = '2021/12/01'      
            end_dates = '2021/12/31'
            get_and_dump_pubmed_papers(selectedCategories, output_filepath,start_date=start_dates, end_date=end_dates)
            save_pdf_from_dump(output_filepath, pdf_path='.', key_to_save='doi')
        summarized_response = store_data_on_llama()
        return summarized_response
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return None
    
def store_data_on_llama():
    try:
        reader = SimpleDirectoryReader(input_files=["10.3233_XST-211050.pdf"])
        pdf_documents = reader.load_data()
        pdf_index = VectorStoreIndex.from_documents(pdf_documents)
    
        pdf_index.storage_context.persist(persist_dir="persist_index")
        storage_context = StorageContext.from_defaults(persist_dir="persist_index")
        retrieved_index = load_index_from_storage(storage_context)
        query_engine = retrieved_index.as_query_engine()
        response = query_engine.query(summarizedPrompt)
        # print(response)
        return response
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return e
    
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
 
def llama_sentence_splitter():
    text_splitter = SentenceSplitter(
    separator=" ", chunk_size=1024, chunk_overlap=20,
    paragraph_separator="\n\n\n", secondary_chunking_regex="[^,.;。]+[,.;。]?",
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode)
    node_parser = SimpleNodeParser.from_defaults(text_splitter=text_splitter)
    
# fetch_papers_for_categories(selectedCategoreies)
# query_indexed_data()
