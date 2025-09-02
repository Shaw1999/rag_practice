from src.libs.project_logger import logger
from src.libs.record_time import record_time

EMBEDDING_PATH = r"E:\huggingface_cache\hub\models--BAAI--bge-large-zh-v1.5\bge-large-zh-v1.5"

@record_time
def test_sentence_to_embedding():
    from sentence_transformers import SentenceTransformer

    # 加载模型（第一次会自动下载到本地缓存）
    model = SentenceTransformer(EMBEDDING_PATH)

    sentences = ["人工智能正在改变世界", "我喜欢机器学习"]
    embeddings = model.encode(sentences, normalize_embeddings=True)  # 建议归一化

    logger.info(f"Embedding 向量维度: {embeddings.shape}")
    logger.info(f"第一个句子的向量前10维: {embeddings[0][:10]}")


def test_similarity():
    from sentence_transformers import SentenceTransformer, util

    model = SentenceTransformer(EMBEDDING_PATH)

    sentences = ["人工智能正在改变世界", "我喜欢机器学习"]
    embeddings = model.encode(sentences, normalize_embeddings=True)

    cos_sim = util.cos_sim(embeddings[0], embeddings[1])
    logger.info("句子相似度:", cos_sim.item())