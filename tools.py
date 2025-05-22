# based on smolagents/src/smolagents/tools.py and smolagents/src/smolagents/agents.py

from typing import Optional, Dict, Union, Any
from packaging import version
from functools import lru_cache

from ftlagents.tools import get_json_schema
from local_python_executor import FinalAnswerException


class Tool:

    name: str
    description: str
    inputs: Dict[str, Dict[str, Union[str, type, bool]]]
    output_type: str
    return_value: Any
    called_with_args: Any
    called_with_kwargs: Any

    def __init__(self, name, description, inputs, output_type, return_value):
        self.name = name
        self.description = description
        self.inputs = inputs
        self.output_type = output_type
        self.return_value = return_value
        self.called_with_args = None
        self.called_with_kwargs = None

    def __call__(self, *args, **kwargs):
        self.called_with_args = args
        self.called_with_kwargs = kwargs
        return self.return_value


DEFAULT_TOOL_DESCRIPTION_TEMPLATE = """
- {{ tool.name }}: {{ tool.description }}
    Takes inputs: {{tool.inputs}}
    Returns an output of type: {{tool.output_type}}
"""


def get_tool_description_with_args(tool: Tool, description_template: Optional[str] = None) -> str:
    if description_template is None:
        description_template = DEFAULT_TOOL_DESCRIPTION_TEMPLATE
    compiled_template = compile_jinja_template(description_template)
    tool_description = compiled_template.render(
        tool=tool,
    )
    return tool_description


@lru_cache
def compile_jinja_template(template):
    try:
        import jinja2
        from jinja2.exceptions import TemplateError
        from jinja2.sandbox import ImmutableSandboxedEnvironment
    except ImportError:
        raise ImportError("template requires jinja2 to be installed.")

    if version.parse(jinja2.__version__) < version.parse("3.1.0"):
        raise ImportError(f"template requires jinja2>=3.1.0 to be installed. Your version is {jinja2.__version__}.")

    def raise_exception(message):
        raise TemplateError(message)

    jinja_env = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)
    jinja_env.globals["raise_exception"] = raise_exception
    return jinja_env.from_string(template)


def get_tool_descriptions(tools: Dict[str, Tool], tool_description_template: str) -> str:
    return "\n".join([get_tool_description_with_args(tool, tool_description_template) for tool in tools.values()])


def format_prompt_with_tools(tools: Dict[str, Tool], prompt_template: str, tool_description_template: str) -> str:
    tool_descriptions = get_tool_descriptions(tools, tool_description_template)
    prompt = prompt_template.replace("{{tool_descriptions}}", tool_descriptions)
    if "{{tool_names}}" in prompt:
        prompt = prompt.replace(
            "{{tool_names}}",
            ", ".join([f"'{tool.name}'" for tool in tools.values()]),
        )
    return prompt


class FinalAnswer(Tool):
    name = "final_answer"

    def __init__(self, state, *args, **kwargs):
        self.state = state

    def forward(self, message: str = "Task was completed"):
        """
        Return the final answer

        Args:
            message: The final answer
        """

        raise FinalAnswerException(message)

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    description, inputs, output_type = get_json_schema(forward)

