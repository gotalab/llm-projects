import asyncio

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import pinecone
import nest_asyncio

from langchain.document_loaders.sitemap import SitemapLoader



def get_website_data_from_sitemap(sitemap_url):
    nest_asyncio.apply()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sitemap_loader = SitemapLoader(
        web_path=sitemap_url
    )
    # sitemap_loader.requests_per_second = 2
    # Optional: avoid `[SSL: CERTIFICATE_VERIFY_FAILED]` issue
    # sitemap_loader.requests_kwargs = {"verify": False}
    docs = sitemap_loader.load()
    return docs

# url = "https://jobs.excelcult.com/wp-sitemap-posts-post-1.xml"

def split_data(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    docs_chunks = text_splitter.split_documents(docs)
    return docs_chunks

def get_embeddings():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

def push_to_pinecone(pinecone_api_token, pinecone_environment, pinecone_index_name, embeddings, docs):
    pinecone.init(
        api_key=pinecone_api_token,
        environment=pinecone_environment,
    )
    index_name = pinecone_index_name
    index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    return index

def pull_from_pinecone(pinecone_api_token, pinecone_environment, pinecone_index_name, embeddings):
    pinecone.init(
        api_key=pinecone_api_token,
        environment=pinecone_environment,
    )
    index_name = pinecone_index_name
    index = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
    return index


def get_similar_docs(index, query, k=2):
    similar_docs = index.similarity_search(query, k=k)
    return similar_docs
