from util import generate_response, parse_code_blobs
from local_python_executor import LocalPythonInterpreter
from tools import Tool, get_tool_descriptions, DEFAULT_TOOL_DESCRIPTION_TEMPLATE, FinalAnswer


def test_hello_world():
    interp = LocalPythonInterpreter([], {})
    response = generate_response(
        "ollama/deepseek-r1:14b",
        "smolagents_code",
        "hello_world",
        cache_prompt=True,
        replacements=dict(
            tool_descriptions="", managed_agents_descriptions="", authorized_imports=""
        ),
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


def test_hello_tools2():
    weather_tool = Tool(
        "weather",
        "Look up the weather",
        dict(location=dict(description="where to look up the weather", type="str")),
        "str",
        "cloudy",
    )
    state = {}
    tools = dict(weather=weather_tool, final_answer=FinalAnswer(state))
    interp = LocalPythonInterpreter([], tools)
    response = generate_response(
        "ollama/deepseek-r1:14b",
        "smolagents_code",
        "hello_tools2",
        cache_prompt=True,
        replacements=dict(
            tool_descriptions=get_tool_descriptions(
                tools, DEFAULT_TOOL_DESCRIPTION_TEMPLATE
            ),
            managed_agents_descriptions="",
            authorized_imports="",
        ),
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
    assert is_final_answer
    assert "cloudy" in output
