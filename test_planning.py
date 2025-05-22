from util import (
    generate_response,
    parse_answer_blocks,
)


def test_linode_doc_numbered():
    response = generate_response(
        "deepseek-r1-14b",
        "planning_numbered",
        "linode_doc",
        cache_prompt=True,
        num_ctx=8192,
    )
    print(response)
    blocks = parse_answer_blocks(response)
    print(blocks)
    assert blocks,  "No blocks list"
    assert len(blocks), "No block elements "


def test_minecraft_doc_numbered():
    response = generate_response(
        "deepseek-r1-14b",
        "planning_numbered",
        "minecraft_doc",
        cache_prompt=True,
        num_ctx=8192,
    )
    print(response)
    blocks = parse_answer_blocks(response)
    print(blocks)
    assert blocks,  "No blocks list"
    assert len(blocks), "No block elements "
