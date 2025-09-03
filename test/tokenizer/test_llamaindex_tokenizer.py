from src.libs.record_time import record_time
from src.tokenizer.llamaindex_tokenizer import LlamaIndexSemanticTokenizer


@record_time
def test_semantic_splitter_node_parser():
    embed_model = r"E:\huggingface_cache\hub\models--BAAI--bge-large-zh-v1.5\bge-large-zh-v1.5"
    tokenizer = LlamaIndexSemanticTokenizer(embed_model=embed_model, breakpoint_percentile_threshold=95)
    # 这段文本在水果和交通工具之间有非常清晰的语义断点。
    text = (
        "智能手机是现代社会不可或缺的通信工具。它集成了电话、相机、网络浏览器等多种功能。"
        "随着技术的发展，手机的计算能力甚至超过了十年前的个人电脑。"
        "各大品牌每年都会发布新款旗舰机型以吸引消费者。"
        "长江是亚洲第一长河，全长约6300公里。它发源于青藏高原，最终注入东海。"
        "长江流域是中国经济最发达的地区之一，养育了数亿人口。"
        "著名的三峡大坝就建在长江之上。"
    )
    records = tokenizer.tokenize(text)

    print(f"Total Records: {len(records)}")
    for record in records:
        print(f"Record ID: {record.id}")
        print(f"Content: {record.content}")
        print("-" * 40)

    # 1. 检查返回的是一个列表
    assert isinstance(records, list)
    # 2. 检查列表是否被成功分割成两块
    assert len(records) == 2
    # 3. 检查分割点是否正确
    assert "智能手机" in records[0].content
    assert "长江" in records[1].content
    print("\n--- 中文测试通过 ---")