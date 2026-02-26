from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from data.fintech_banking_docs import FINTECH_BANKING_FAQ_DOCS
from data.fintech_support_docs import FINTECH_SUPPORT_DOCS

embedding_model = OpenAIEmbeddings()


fintech_banking_store = InMemoryVectorStore.from_documents([], embedding_model)
fintech_banking_store.add_documents(FINTECH_BANKING_FAQ_DOCS)
fintech_banking_retriever = fintech_banking_store.as_retriever()


fintech_support_store = InMemoryVectorStore.from_documents([], embedding_model)
fintech_support_store.add_documents(FINTECH_SUPPORT_DOCS)
fintech_support_retriever = fintech_support_store.as_retriever()