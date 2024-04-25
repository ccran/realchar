from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from llama_index import SimpleDirectoryReader

loader = SimpleDirectoryReader("./data")
documents = loader.load_data()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.create_documents(
    texts=[d.text for d in documents],
)

for doc in docs:
    if len(doc.page_content) > 500:
        print(len(doc.page_content))
print(f'docs总大小:{len(docs)}')
embeddings = HuggingFaceEmbeddings(model_name='/home/lihao/workspace/chatchat/Langchain-Chatchat-0.2.9/bge-m3')
data = embeddings.embed_documents(texts=[x.page_content for x in docs])
print(f'data总大小:{len(data)}')
