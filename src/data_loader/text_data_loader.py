from src.data_loader.data_loader import BaseDataLoader


class TextDataLoader(BaseDataLoader):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def read_data(self) -> str:
        """从文件中读取原始数据"""
        with open(self.filepath, "r", encoding="utf-8") as f:
            return f.read()  # 返回文件内容

    def preprocess_data(self, raw_data: str) -> str:
        """对读取的文件内容进行预处理"""
        # 比如去除多余的空白字符，换行符等
        return raw_data
