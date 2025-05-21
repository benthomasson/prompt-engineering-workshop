from util import generate_response, parse_code_blobs, parse_json_blocks


def test_planets_0():
    response = generate_response(
        "deepseek-r1-14b",
        "helpful_assistant",
        "planet_names",
        top_p=0
    )
    print(response)


def test_planets_1():
    response = generate_response(
        "deepseek-r1-14b",
        "helpful_assistant",
        "planet_names",
        top_p=1
    )
    print(response)

