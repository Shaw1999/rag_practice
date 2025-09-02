# RAG技术选型

## 环境准备
```python
import torch
print(torch.__version__)       # 2.8.0+cu129
print(torch.version.cuda)      # 12.9
print(torch.cuda.is_available())    # True
print(torch.cuda.get_device_name(0))    # NVIDIA GeForce RTX 3080 Laptop GPU
```

## 读取数据
### 纯文本

### docx
数据特征
- 纯文本
- 表格
- 公式
- 图片

## 分词
### LlamaIndex

## embedding
### 

## 转换为标准格式数据
```text
src/data_loader/record.py
```

## 转换为标准入库数据
### Milvus

## 存入向量数据库
### Milvus

## 检索&上下文补充
### Milvus

## LLM请求
- 推理模型
- 非推理模型

## 数据迭代
