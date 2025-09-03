from abc import ABC, abstractmethod

from src.tokenizer.record import Record


class BaseTokenizer(ABC):
    """分词抽象类，定义统一的分词接口"""

    @abstractmethod
    def tokenize(self, text: str) -> Record:
        """
        将输入的字符串分词，返回 Record 对象
        :param text: 原始字符串
        :return: Record(tokens=..., metadata=...)
        """
        pass
