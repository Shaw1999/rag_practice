from abc import ABC, abstractmethod
from typing import Any

class BaseDataLoader(ABC):
    """数据处理抽象类，定义数据读取和预处理接口"""

    @abstractmethod
    def read_data(self) -> Any:
        """
        从不同的数据源读取数据（如数据库、文件、API等）
        返回的数据类型可以是任意的（如列表、字典等），具体取决于数据源
        """
        pass

    @abstractmethod
    def preprocess_data(self, raw_data: Any) -> str:
        """
        对读取的数据进行预处理，将其转换为字符串
        返回处理后的文本数据（str）
        """
        pass
