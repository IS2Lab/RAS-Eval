import ast
import json
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


def parse_toolkits(toolkit_paths: list[str]) -> dict[str, int]:
    count = {}
    for path in toolkit_paths:
        toolkit_name = path.split("/")[-1]
        count[toolkit_name] = 0
        with open(f"{path}/function/{toolkit_name}.py", "r") as file:
            code = file.read()
        tree = ast.parse(code)
        dependencies = []
        commands = []
        tools: list[ast.FunctionDef] = []
        helpers = []
        for i, subtree in enumerate(tree.body):
            if isinstance(subtree, ast.FunctionDef):
                if subtree.name.startswith("_"):
                    helpers.append(subtree)
                else:
                    tools.append(subtree)
                    # print(ast.unparse(subtree))
            elif isinstance(subtree, (ast.Import, ast.ImportFrom)):
                dependencies.append(subtree)
            else:
                commands.append(subtree)
        framework_dependencies = []
        for tool_tree in tools:
            tool_name = tool_tree.name
            framework_dependencies.append(ast.ImportFrom(
                module=f"src.toolkits.real.{toolkit_name}.function.{toolkit_name}", 
                names=[ast.alias(name=tool_name)], 
                level=0
            ))
            print(ast.unparse(framework_dependencies[-1]))
        langgraph_code = ""
        mcp_code = ""
        for dependency in framework_dependencies:
            langgraph_code += ast.unparse(dependency) + "\n"
            mcp_code += ast.unparse(dependency) + "\n"
        if not os.path.exists(f"{path}/langgraph"):
            os.makedirs(f"{path}/langgraph")
        if not os.path.exists(f"{path}/mcp"):
            os.makedirs(f"{path}/mcp")
        with open(f"{path}/langgraph/{toolkit_name}.py", "w") as file:
            file.write(langgraph_code)
        with open(f"{path}/mcp/{toolkit_name}.py", "w") as file:
            file.write(mcp_code)

    # Check compiled result
    for path in toolkit_paths:
        toolkit_name = path.split("/")[-1]
        with open(f"{path}/function/{toolkit_name}.py", "r") as file:
            code = file.read()  
            exec(code)
        with open(f"{path}/langgraph/{toolkit_name}.py", "r") as file:
            code = file.read()
            exec(code)
        with open(f"{path}/mcp/{toolkit_name}.py", "r") as file:
            code = file.read()
            exec(code)
        

temp = """
from ..function.toolkit import tool
"""

def main():
    toolkit_paths = [
        "src/toolkits/real/amap_toolkit",
        "src/toolkits/real/word_toolkit",
        "src/toolkits/real/excel_toolkit",
        "src/toolkits/real/ppt_toolkit",
        "src/toolkits/real/calendar_toolkit",
        "src/toolkits/real/arxiv_toolkit",
        "src/toolkits/real/clock_toolkit",
        "src/toolkits/real/map_toolkit",
        "src/toolkits/real/markdown_toolkit",
        "src/toolkits/real/polygon_toolkit",
        "src/toolkits/real/sql_toolkit",
        "src/toolkits/real/stock_toolkit",
        "src/toolkits/real/system_toolkit",
        "src/toolkits/real/tavily_toolkit",
        "src/toolkits/real/weather_toolkit",
    ]
    count = parse_toolkits(toolkit_paths)
    # print(ast.dump(ast.parse(temp), indent=4))


if __name__ == "__main__":
    main()