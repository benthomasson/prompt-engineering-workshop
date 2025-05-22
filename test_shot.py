from util import generate_response, parse_code_blobs, parse_json_blocks


def test_zero_shot():
    """
    Count from 1 to 10 as a JSON list.
    """
    response = generate_response(
        "qwen3-06b",
        "helpful_assistant",
        "zero_shot",
        temperature=0,
    )
    print(response)
    count = parse_json_blocks(response)
    print(count)
    assert count is not None
    assert count[0] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_one_shot():
    """
    Return your result as a json block like this example:

    ```json
    [1,2,3]
    ```


    Count from 1 to 10 as a JSON list.
    """
    response = generate_response(
        "qwen3-06b",
        "helpful_assistant",
        "one_shot",
        temperature=0,
    )
    print(response)
    count = parse_json_blocks(response)
    print(count)
    assert count is not None
    assert count[0] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_few_shot():
    """
    Return your result as a json block like these examples:

    ```json
    [1,2,3]
    ```

    ```json
    [4,5,6]
    ```

    ```json
    [2,4,6]
    ```

    Count from 1 to 10 as a JSON list.
    """
    response = generate_response(
        "qwen3-06b",
        "helpful_assistant",
        "few_shot",
        temperature=0,
    )
    print(response)
    count = parse_json_blocks(response)
    print(count)
    assert count is not None
    assert count[0] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
