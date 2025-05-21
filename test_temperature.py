from util import generate_response, parse_code_blobs, parse_json_blocks

import logging
logging.basicConfig(level=logging.DEBUG)


def test_planets_0():
    response = generate_response(
        "deepseek-r1-14b",
        "helpful_assistant",
        "planet_names0",
        temperature=0
    )
    print(response)


def test_planets_1():
    response = generate_response(
        "deepseek-r1-14b",
        "helpful_assistant",
        "planet_names1",
        temperature=1
    )
    print(response)

