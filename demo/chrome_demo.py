from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import logging
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from llama_index import SimpleDirectoryReader

formatter = "%(asctime)s - %(funcName)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s"
logger = logging.getLogger("chrome_demo")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
ch_format = logging.Formatter(formatter)
console_handler.setFormatter(ch_format)
logger.addHandler(console_handler)

# 加载embbeding
embedding_function = SentenceTransformerEmbeddings(
    model_name='/home/lihao/workspace/chatchat/Langchain-Chatchat-0.2.9/bge-m3')
# 创建chroma
chroma = Chroma(
    collection_name="llm",
    embedding_function=embedding_function,
    persist_directory="./chroma.db",
)
# 序列化数据到chroma
loader = SimpleDirectoryReader("./data")
documents = loader.load_data()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.create_documents(
    texts=[d.text for d in documents],
)
logger.info(f'docs总大小:{len(docs)}')
chroma.add_documents(docs)
