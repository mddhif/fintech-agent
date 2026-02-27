from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from data.fintech_banking_docs import FINTECH_BANKING_FAQ_DOCS
from data.fintech_support_docs import FINTECH_SUPPORT_DOCS
from supabase.client import Client, create_client
from langchain_community.vectorstores import SupabaseVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

embedding_model = OpenAIEmbeddings()

# Supabase retrieval

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

fintech_banking_retriever = SupabaseVectorStore(
    client=supabase,
    embedding=embedding_model,
    table_name="fintech_banking_documents",
    query_name="fintech_banking_match_documents"
).as_retriever()

fintech_support_retriever = SupabaseVectorStore(
    client=supabase,
    embedding=embedding_model,
    table_name="fintech_support_documents",
    query_name="fintech_support_match_documents"
).as_retriever()


# In Memory retrieval
'''
fintech_banking_store = InMemoryVectorStore.from_documents([], embedding_model)
fintech_banking_store.add_documents(FINTECH_BANKING_FAQ_DOCS)
fintech_banking_retriever = fintech_banking_store.as_retriever()


fintech_support_store = InMemoryVectorStore.from_documents([], embedding_model)
fintech_support_store.add_documents(FINTECH_SUPPORT_DOCS)
fintech_support_retriever = fintech_support_store.as_retriever()
'''