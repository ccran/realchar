# from FlagEmbedding import BGEM3FlagModel
#
# model = BGEM3FlagModel('/home/lihao/workspace/chatchat/Langchain-Chatchat-0.2.9/bge-m3',
#                        use_fp16=True)  # Setting use_fp16 to True speeds up computation with a slight performance degradation
#
# sentences_1 = ["What is BGE M3?", "Defination of BM25"]
# sentences_2 = [
#     "BGE M3 is an embedding model supporting dense retrieval, lexical matching and multi-vector interaction.",
#     "BM25 is a bag-of-words retrieval function that ranks a set of documents based on the query terms appearing in each document"]
#
# embeddings_1 = model.encode(sentences_1,
#                             batch_size=12,
#                             max_length=8192,
#                             # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
#                             )['dense_vecs']
# embeddings_2 = model.encode(sentences_2)['dense_vecs']
# similarity = embeddings_1 @ embeddings_2.T
# print(similarity)
# # [[0.6265, 0.3477], [0.3499, 0.678 ]]

from sentence_transformers import SentenceTransformer
sentences_1 = ["样例数据-1", "样例数据-2"]
sentences_2 = ["样例数据-3", "样例数据-4"]
model = SentenceTransformer('/home/lihao/workspace/chatchat/Langchain-Chatchat-0.2.9/bge-m3')
embeddings_1 = model.encode(sentences_1, normalize_embeddings=True)
embeddings_2 = model.encode(sentences_2, normalize_embeddings=True)
similarity = embeddings_1 @ embeddings_2.T
print(similarity)