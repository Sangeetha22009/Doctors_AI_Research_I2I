import tiktoken
import os
from llama_index.text_splitter import SentenceSplitter
from paperscraper.pubmed import get_and_dump_pubmed_papers
# from llama_index import VectorStoreIndex
from llama_index.node_parser import SimpleNodeParser
# from llama_index import SimpleDirectoryReader
from paperscraper.pdf import save_pdf_from_dump
from llama_index import(
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage
)
from llama_index.vector_stores import DeepLakeVectorStore



covid = ['COVID-19','SARS-CoV-2']
ai = ['Artificial intelligence', 'Deep learning', 'Machine learning']
mi = ['Medical imaging']
selectedCategoreies = [covid,ai,mi]
output_filepath='covid19_ai_imaging.jsonl'
os.environ["OPENAI_API_KEY"] = ""

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
        store_data_on_llama()
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return None
    
def store_data_on_llama():
    try:
        reader = SimpleDirectoryReader(input_files=["10.3233_XST-211050.pdf"])
        pdf_documents = reader.load_data()
        parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
        pdf_nodes = parser.get_nodes_from_documents(pdf_documents)
        pdf_index = VectorStoreIndex.from_documents(pdf_documents)
    
        # vector_store = DeepLakeVectorStore(dataset_path="persist_index")
        # storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # # Load documents and build index
        # stored_index = VectorStoreIndex.from_documents(pdf_documents, storage_context=storage_context)
        # # reload an existing one
        # index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

        pdf_index.storage_context.persist(persist_dir="persist_index")
        storage_context = StorageContext.from_defaults(persist_dir="persist_index")
        retrieved_index = load_index_from_storage(storage_context)

        query_engine = retrieved_index.as_query_engine()
        response = query_engine.query("Is there anything related to Cardiovascular risk factors?")
        print(response)

        # print(pdf_nodes)
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return e
def query_indexed_data():
    vector_store = DeepLakeVectorStore(dataset_path="persist_index")
    retrieved_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = retrieved_index.as_query_engine()
    response = query_engine.query("What are the methods to indetify COVID-19 infection?")
    print(response)
 
def llama_sentence_splitter():

    text_splitter = SentenceSplitter(
  separator=" ", chunk_size=1024, chunk_overlap=20,
  paragraph_separator="\n\n\n", secondary_chunking_regex="[^,.;。]+[,.;。]?",
  tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
    )
    node_parser = SimpleNodeParser.from_defaults(text_splitter=text_splitter)
    
# fetch_papers_for_categories(selectedCategoreies)
# query_indexed_data()
