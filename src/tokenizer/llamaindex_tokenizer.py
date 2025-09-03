import uuid
import re
from typing import List, Optional, Callable

from llama_index.core import Document
from llama_index.core.node_parser import SemanticSplitterNodeParser, SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src.tokenizer.base_tokenizer import BaseTokenizer
from src.tokenizer.record import Record, RecordMetaData


# 定义一个能够处理中文标点的句子分割函数
def chinese_sentence_splitter(text: str) -> List[str]:
    # 使用正则表达式按中文标点符号分割句子
    sentences = re.split(r'([。！？\n])', text)
    # 将标点符号重新附加到句子末尾
    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
    # 如果有遗留的最后一句（没有结尾标点），则添加
    if len(sentences) * 2 < len(re.split(r'([。！？\n])', text)):
        sentences.append(re.split(r'([。！？\n])', text)[-1])

    # 过滤掉空字符串
    return [s.strip() for s in sentences if s.strip()]


class LlamaIndexSemanticTokenizer(BaseTokenizer):
    def __init__(self, embed_model: str = "BAAI/bge-large-zh-v1.5",
                 breakpoint_percentile_threshold: int = 95,
                 device: Optional[str] = None,
                 sentence_splitter: Optional[Callable[[str], List[str]]] = chinese_sentence_splitter):
        """
        :param embed_model: 使用的 HuggingFace embedding 模型名称
        :param breakpoint_percentile_threshold: 分割断点的百分比阈值。
        :param device: 计算设备, 如 "cpu", "cuda"。如果为 None, 则自动检测。
        :param sentence_splitter: 用于将文本分割成句子的函数。默认为中文优化版。
        """
        self.embed_model = HuggingFaceEmbedding(
            model_name=embed_model,
            device=device
        )

        self.splitter = SemanticSplitterNodeParser(
            embed_model=self.embed_model,
            breakpoint_percentile_threshold=breakpoint_percentile_threshold,
            sentence_splitter=sentence_splitter
        )

    def tokenize(self, text: str) -> List[Record]:
        documents = [Document(text=text)]
        nodes = self.splitter.get_nodes_from_documents(documents)

        records = []
        for node in nodes:
            records.append(Record(
                id=uuid.uuid4().hex,
                content=node.get_content(),
                metadata=RecordMetaData()
            ))
        return records