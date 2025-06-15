import ast
import json
import os
import sys
from langchain_core.utils.function_calling import convert_to_openai_function


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
        langgraph_dependencies = [
            ast.ImportFrom(
                module="langchain_core.tools",
                names=[ast.alias(name="tool")], 
                level=0
            )
        ]
        mcp_dependencies = [
            ast.ImportFrom(
                module="mcp.server.fastmcp",
                names=[ast.alias(name="FastMCP")], 
                level=0
            )
        ]
        langgraph_code = ""
        mcp_code = ""
        for dependency in langgraph_dependencies + framework_dependencies + dependencies:
            langgraph_code += ast.unparse(dependency) + "\n"
        for dependency in mcp_dependencies + framework_dependencies + dependencies:
            mcp_code += ast.unparse(dependency) + "\n"

        mcp_code += f"\n\nmcp = FastMCP('{toolkit_name}')\n"
        langgraph_code += "\n\n"

        for command in commands:
            mcp_code += ast.unparse(command) + "\n"
            langgraph_code += ast.unparse(command) + "\n"
        
        mcp_code += "\n\n"
        langgraph_code += "\n\n"

        tool_names: list[str] = []
        for tool in tools:
            tool_names.append(tool.name)

            langgraph_function = ast.FunctionDef(
                name=f"_{tool.name}",
                args=tool.args,
                body=[tool.body[0]]+[
                    ast.Return(
                        value=ast.Call(
                            func=ast.Name(id=tool.name, ctx=ast.Load()),
                            args=[],
                            keywords=[ast.keyword(arg=arg.arg, value=ast.Name(id=arg.arg, ctx=ast.Load())) for arg in tool.args.args]
                        )
                    )
                ],
                # decorator_list=[],
                decorator_list=[
                    ast.Call(
                        func=ast.Name(id="tool", ctx=ast.Load()),
                        args=[],
                        keywords=[ast.keyword(arg="parse_docstring", value=ast.Constant(value=True))]
                    )
                ],
                returns=tool.returns,
                type_params=[]
            )
            mcp_function = ast.FunctionDef(
                name=f"_{tool.name}",
                args=tool.args,
                body=[tool.body[0]]+[
                    ast.Return(
                        value=ast.Call(
                            func=ast.Name(id=tool.name, ctx=ast.Load()),
                            args=[],
                            keywords=[ast.keyword(arg=arg.arg, value=ast.Name(id=arg.arg, ctx=ast.Load())) for arg in tool.args.args]
                        )
                    )
                ],
                decorator_list=[
                    ast.Call(
                        func=ast.Attribute(value=ast.Name(id="mcp", ctx=ast.Load()), attr="tool", ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    )
                ],
                returns=tool.returns,
                type_params=[]
            )
            langgraph_code += ast.unparse(ast.fix_missing_locations(langgraph_function)) + "\n\n\n"
            mcp_code += ast.unparse(ast.fix_missing_locations(mcp_function)) + "\n\n\n" 

        main_body = ast.If(
            test=ast.Compare(
                left=ast.Name(id="__name__", ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value="__main__")]
            ),
            body=[
                ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id="mcp", ctx=ast.Load()), attr="run", ctx=ast.Load()),
                        args=[ast.Constant(value="stdio")],
                        keywords=[]
                    )
                )
            ],
            orelse=[]
        )
        mcp_code += ast.unparse(ast.fix_missing_locations(main_body)) + "\n"
        
        if not os.path.exists(f"{path}/langgraph"):
            os.makedirs(f"{path}/langgraph")
        if not os.path.exists(f"{path}/mcp"):
            os.makedirs(f"{path}/mcp")
        if not os.path.exists(f"{path}/json"):
            os.makedirs(f"{path}/json")
        with open(f"{path}/langgraph/{toolkit_name}.py", "w") as file:
            file.write(langgraph_code)
        with open(f"{path}/mcp/{toolkit_name}.py", "w") as file:
            file.write(mcp_code)

        json_functions = []
        for tool_name in tool_names:
            try:
                local_vars = {} 
                exec(f"from src.toolkits.real.{toolkit_name}.langgraph.{toolkit_name} import _{tool_name}", globals(), local_vars) 
                exec(f"tool = _{tool_name}", globals(), local_vars) 
                tool = local_vars.get('tool') 
                json_function = convert_to_openai_function(tool)
                json_function["name"] = tool_name
                json_functions.append(json_function)
            except Exception as e:
                print(f'Error compiling tool {tool_name}: {e}')

        with open(f"{path}/json/{toolkit_name}.json", "w") as file:
            file.write(json.dumps(json_functions, indent=4))
        count[toolkit_name] = len(tool_names)

    # Check compiled result
    for path in toolkit_paths:
        toolkit_name = path.split("/")[-1]
        with open(f"{path}/function/{toolkit_name}.py", "r") as file:
            code = file.read()  
            exec(code)
        with open(f"{path}/langgraph/{toolkit_name}.py", "r") as file:
            code = file.read()
            exec(code)
            
        # with open(f"{path}/mcp/{toolkit_name}.py", "r") as file:
        #     code = file.read()
        #     exec(code)
    return count
        

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
    print(count)


if __name__ == "__main__":
    main()