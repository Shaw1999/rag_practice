# 说明：
# 本文件定义 RAG 记录的元数据模型，将常见 metadata 划分为7类，
# 便于结构化表达、类型检查与后续扩展。

from dataclasses import dataclass
from typing import Optional, List

# 标识与版本：用于唯一定位记录与版本追踪
@dataclass
class IdentificationVersionMeta:
    id: Optional[str] = None            # 全局唯一记录ID（通常指chunk或片段）
    doc_id: Optional[str] = None        # 原始文档ID
    chunk_id: Optional[str] = None      # 文档内片段ID（切分单元）
    hash: Optional[str] = None          # 原始内容/文件哈希（去重与变更检测）
    dataset: Optional[str] = None       # 所属数据集名称或来源集合
    version: Optional[str] = None       # 版本号或快照标识（如v1、2024-09-01）

# 源与定位：指向原文位置，便于可追溯与引用
@dataclass
class SourceLocationMeta:
    source: Optional[str] = None        # 数据源标识（如: github、web、s3、gdrive）
    url: Optional[str] = None           # 原始URL（如网页、仓库文件URL）
    path: Optional[str] = None          # 本地或仓库内路径
    page: Optional[int] = None          # 页码（PDF/幻灯片等）
    offset: Optional[int] = None        # 偏移量（字符/字节）
    line_start: Optional[int] = None    # 起始行号（代码/文本）
    line_end: Optional[int] = None      # 结束行号
    section: Optional[str] = None       # 章节名/目录节点
    heading: Optional[str] = None       # 标题/小节标题

# 文档信息：描述原始文档的基本属性
@dataclass
class DocumentInfoMeta:
    title: Optional[str] = None         # 文档标题
    author: Optional[str] = None        # 作者/维护者
    created_at: Optional[str] = None    # 创建时间（建议ISO-8601字符串）
    updated_at: Optional[str] = None    # 更新时间（建议ISO-8601字符串）
    published_at: Optional[str] = None  # 发布/生效时间（建议ISO-8601字符串）
    lang: Optional[str] = None          # 语言代码（如 zh-CN、en）
    mime_type: Optional[str] = None     # MIME类型（如 application/pdf）
    size_bytes: Optional[int] = None    # 文档大小（字节）

# 处理与可追溯：用于还原处理流程，便于审计与复现
@dataclass
class ProcessingTraceMeta:
    splitter: Optional[str] = None      # 切分器名称/策略
    chunk_size: Optional[int] = None    # 切分长度
    overlap: Optional[int] = None       # 切分重叠字符数
    pipeline: Optional[List[str]] = None# 处理流水线步骤（如 ["clean", "split", "embed"]）
    ocr: Optional[bool] = None          # 是否经过OCR识别
    embed_model: Optional[str] = None   # 向量模型名称（如 bge-large、text-embedding-3-large）
    embed_dim: Optional[int] = None     # 向量维度
    text_hash: Optional[str] = None     # 纯文本内容哈希（变更检测/缓存键）

# 关系与结构：表达层次、顺序与对话关系
@dataclass
class RelationStructureMeta:
    parent_id: Optional[str] = None     # 父节点/上级文档或聚合节点ID
    next_id: Optional[str] = None       # 同级下一个片段ID（顺序遍历）
    prev_id: Optional[str] = None       # 同级上一个片段ID
    thread_id: Optional[str] = None     # 主题/线程ID（结构化讨论/issue）
    conversation_id: Optional[str] = None # 会话ID（多轮对话上下文）

# 质量与合规：用于检索优选与合规控制
@dataclass
class QualityComplianceMeta:
    score: Optional[float] = None       # 评分（质量/相关性等）
    quality: Optional[str] = None       # 质量等级（如 high/medium/low）
    verified: Optional[bool] = None     # 是否已人工校验
    pii: Optional[bool] = None          # 是否包含个人敏感信息
    sensitive: Optional[bool] = None    # 是否敏感（策略控制）
    license: Optional[str] = None       # 许可协议（如 MIT、CC-BY-4.0）
    visibility: Optional[str] = None    # 可见性（public/private/internal）
    tags: Optional[List[str]] = None    # 标签集合（检索/过滤辅助）

# 业务/检索辅助：与业务域、产品与检索策略相关
@dataclass
class BusinessRetrievalMeta:
    doc_type: Optional[str] = None      # 文档类型（如 api_doc、spec、faq、handbook）
    domain: Optional[str] = None        # 业务域/领域（如 finance、devops）
    product: Optional[str] = None       # 产品线/模块
    keywords: Optional[List[str]] = None# 关键词列表（召回/boost）

# 组合7类到 RecordMetaData：按类别聚合，便于选择性填充
@dataclass
class RecordMetaData:
    identification: Optional[IdentificationVersionMeta] = None # 标识与版本
    source_location: Optional[SourceLocationMeta] = None       # 源与定位
    document_info: Optional[DocumentInfoMeta] = None           # 文档信息
    processing: Optional[ProcessingTraceMeta] = None           # 处理与可追溯
    relations: Optional[RelationStructureMeta] = None          # 关系与结构
    quality: Optional[QualityComplianceMeta] = None            # 质量与合规
    business: Optional[BusinessRetrievalMeta] = None           # 业务/检索辅助

# 记录实体：内容 + 聚合后的元数据
@dataclass
class Record:
    id: str                        # 记录ID（通常与 identification.id 保持一致或镜像）
    content: str                   # 文本内容（用于索引/检索/生成）
    metadata: RecordMetaData       # 元数据（7类聚合）
