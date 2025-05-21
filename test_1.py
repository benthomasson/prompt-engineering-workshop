from util import generate_response, parse_code_blobs, parse_json_blocks
from local_python_executor import LocalPythonInterpreter


def test_hello_world():
    interp = LocalPythonInterpreter([], {})
    response = generate_response(
        "deepseek-r1-14b",
        "helpful_code_assistant",
        "hello_world",
    )
    print(response)
    code = parse_code_blobs(response)
    assert code is not None, "No code found"
    print(code)
    output, execution_logs, is_final_answer, trace = interp(code, {})
    print(output)
    print(execution_logs)
    print(is_final_answer)
    print(trace)
    assert "hello" in execution_logs.lower()
    assert "world" in execution_logs.lower()


def test_json_block():
    response = generate_response(
        "deepseek-r1-14b",
        "helpful_assistant",
        "count_json",
    )
    print(response)
    count = parse_json_blocks(response)
    print(count)
    assert count is not None
    assert count[0] == [1,2,3,4,5,6,7,8,9,10]


def test_json_block_qwen():
    response = generate_response(
        "qwen3-14b",
        "helpful_assistant",
        "count_json",
    )
    print(response)
    count = parse_json_blocks(response)
    print(count)
    assert count is not None
    assert count[0] == [1,2,3,4,5,6,7,8,9,10]


def test_json_block_qwen2():
    response = generate_response(
        "qwen3-14b",
        "helpful_assistant",
        "count_json2",
    )
    print(response)
    count = parse_json_blocks(response)
    print(count)
    assert count is not None
    assert count[0] == [1,2,3,4,5,6,7,8,9,10]


def test_json_block_granite32():
    response = generate_response(
        "granite3-2-8b",
        "helpful_assistant",
        "count_json2",
    )
    print(response)
    count = parse_json_blocks(response)
    print(count)
    assert count is not None
    assert count[0] == [1,2,3,4,5,6,7,8,9,10]
