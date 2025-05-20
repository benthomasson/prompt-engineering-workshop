import ast
import json
import logging
import os
import re
from json.decoder import JSONDecodeError
import time

import yaml
from litellm import completion

logger = logging.getLogger(__name__)

FULL_MODEL_NAMES = {
    'deepseek-r1-14b': 'ollama/deepseek-r1:14b',
}

def load_model_config(config_file="models.yaml"):
    models = {}
    with open(config_file) as f:
        for item in yaml.safe_load(f.read()):
            models[item['name']] = item['model']
    return models


def load_prompt(prompt_file_name, replacements=None):
    with open(os.path.join("prompts", prompt_file_name)) as f:
        prompt = f.read()
    if replacements:
        for key, value in replacements.items():
            key = "{{%s}}".format(key)
            prompt = prompt.replace(key, value)
    logger.info("Prompt loaded: %s", prompt)
    return prompt


def generate_response(
    model_name,
    system_prompt_file_name,
    user_prompt_file_name,
    replacements=None,
    **parameters_dict,
):
    user_prompt_text = load_prompt(user_prompt_file_name, replacements=replacements)
    system_prompt_text = load_prompt(system_prompt_file_name, replacements=replacements)
    response = completion(
        model=load_model_config()[model_name],
        messages=[
            {"role": "system", "content": system_prompt_text},
            {"role": "user", "content": user_prompt_text},
        ],
        **parameters_dict,
    )
    os.makedirs(
        os.path.join("responses", model_name, system_prompt_file_name, user_prompt_file_name),
        exist_ok=True,
    )
    result_text = response["choices"][0]["message"]["content"]
    response_output_file = os.path.join(
        "responses",
        model_name,
        system_prompt_file_name,
        user_prompt_file_name,
        f"{time.time()}.txt",
    )
    print(response_output_file)
    with open(
        response_output_file,
        "w",
    ) as f:
        f.write(result_text)
    return result_text


def find_responses(model_name, system_prompt_file_name, user_prompt_file_name):
    responses = []
    responses_dir = os.path.join(
        "responses", model_name, system_prompt_file_name, user_prompt_file_name
    )
    if os.path.exists(responses_dir):
        for response_file_name in os.listdir(
            os.path.join("responses", model_name, system_prompt_file_name, user_prompt_file_name)
        ):
            responses.append(response_file_name)
    return responses


def load_responses(model_name, system_prompt_file_name, user_prompt_file_name):
    responses = []
    responses_dir = os.path.join(
        "responses", model_name, system_prompt_file_name, user_prompt_file_name
    )
    if os.path.exists(responses_dir):
        for response_file_name in os.listdir(
            os.path.join("responses", model_name, system_prompt_file_name, user_prompt_file_name)
        ):
            with open(
                os.path.join(
                    "responses",
                    model_name,
                    system_prompt_file_name,
                    user_prompt_file_name,
                    response_file_name,
                )
            ) as f:
                responses.append((f.read(), response_file_name))
    return responses


def load_response(model_name, system_prompt_file_name, user_prompt_file_name, response_file_name):
    with open(
        os.path.join(
            "responses",
            model_name,
            system_prompt_file_name,
            user_prompt_file_name,
            response_file_name,
        )
    ) as f:
        return f.read()


# based on smolagents/src/smolagents/util.py
def parse_code_blobs(code_blob: str) -> str:
    """Parses the LLM's output to get any code blob inside. Will return the
    code directly if it's code."""
    if "<think>" in code_blob:
        code_blob = parse_answer_blocks(code_blob)[0]
    pattern = r"```(?:py|python)\n(.*?)\n\s*```"
    matches = re.findall(pattern, code_blob, re.DOTALL)
    if len(matches) == 0:
        try:  # Maybe the LLM outputted a code blob directly
            ast.parse(code_blob)
            return code_blob
        except SyntaxError as e:
            print(e)
        return None

    # Join all the code blobs together
    return "\n\n".join(match.strip() for match in matches)


def parse_json_blocks(json_block: str) -> str:
    if "<think>" in json_block:
        json_block = parse_answer_blocks(json_block)[0]
    pattern = r"```(?:json)\n(.*?)\n\s*```"
    matches = re.findall(pattern, json_block, re.DOTALL)
    if len(matches) == 0:
        try:  # Is the whole output a JSON block?
            return [json.loads(json_block)]
        except JSONDecodeError:
            pass
        return None

    return [json.loads(match) for match in matches]


def parse_yaml_blocks(yaml_block: str) -> str:
    if "<think>" in yaml_block:
        yaml_block = parse_answer_blocks(yaml_block)[0]
    pattern = r"```(?:yaml)\n(.*?)\n\s*```"
    matches = re.findall(pattern, yaml_block, re.DOTALL)
    return [yaml.safe_load(match) for match in matches]


def parse_blocks(block: str) -> str:
    if "<think>" in block:
        block = parse_answer_blocks(block)[0]
    pattern = r"```\n(.*?)\n\s*```"
    matches = re.findall(pattern, block, re.DOTALL)
    return matches


def parse_thinking_blocks(block: str) -> str:
    pattern = r"<think>\n(.*?)\n\s*</think>"
    matches = re.findall(pattern, block, re.DOTALL)
    return matches


def parse_answer_blocks(block: str) -> str:
    pattern = r"<think>\n(?:.*?)\n\s*</think>\n(.*)"
    matches = re.findall(pattern, block, re.DOTALL)
    return matches
