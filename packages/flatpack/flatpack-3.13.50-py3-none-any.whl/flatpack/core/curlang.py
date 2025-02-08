import shlex

from lark import Lark, Transformer

curlang_grammar = r"""
start: statement+
statement: cmd_stmt | delete_stmt | fail_stmt | find_stmt | get_stmt | make_stmt | pass_stmt | print_stmt | use_stmt 

cmd_block: "{" cmd_content? "}"
cmd_content: /[^}]+/
cmd_stmt: "cmd" (cmd_block | RAW) ";"?

delete_stmt: "delete" STRING ";"?
fail_stmt: "fail" STRING
find_stmt: KEYWORD STRING block "else" STRING ";"?
get_stmt: "get" STRING "as" STRING (block)?
make_stmt: "make" STRING ";"?
pass_stmt: "pass" STRING
print_stmt: "print" STRING

module_list: module ("," module)*
module: CNAME (":" CNAME)?
use_stmt: "use" module_list ";"?

block: "{" statement+ "}"
KEYWORD: "!find" | "find"

COMMENT: /#[^\n]*/
RAW: /[^\n]+/
STRING: /"([^"\\]*(\\.[^"\\]*)*)"/

%import common.CNAME
%import common.WS
%ignore WS
%ignore COMMENT
"""


class CurlangTransformer(Transformer):
    def block(self, items):
        return items

    def cmd_block(self, items):
        return items[0] if items else ""

    def cmd_content(self, items):
        return items[0].value if hasattr(items[0], "value") else items[0]

    def cmd_stmt(self, items):
        return {"type": "cmd", "command": items[0].strip(), "runtime": "bash"}

    def delete_stmt(self, items):
        return {"type": "delete", "target": items[0], "runtime": "bash"}

    def fail_stmt(self, items):
        return {"type": "fail", "message": items[0], "runtime": "bash"}

    def find_stmt(self, items):
        return {
            "type": "find",
            "negated": (items[0] == "!find"),
            "filename": items[1],
            "block": items[2],
            "message": items[3],
            "runtime": "bash"
        }

    def get_stmt(self, items):
        r = {
            "type": "get",
            "url": items[0],
            "destination": items[1],
            "runtime": "bash"
        }

        if len(items) > 2:
            r["block"] = items[2]
        return r

    def make_stmt(self, items):
        return {"type": "make", "target": items[0], "runtime": "bash"}

    def pass_stmt(self, items):
        return {"type": "pass", "message": items[0], "runtime": "bash"}

    def print_stmt(self, items):
        return {"type": "print", "message": items[0], "runtime": "bash"}

    def use_stmt(self, items):
        modules = items[0]
        lines = []

        for mod in modules:
            if isinstance(mod, tuple):
                alias, mod_name = mod

                if alias.islower():
                    lines.append(f"import {mod_name} as {alias}")
                else:
                    lines.append(f"from {mod_name} import {alias}")
            else:
                lines.append(f"import {mod}")
        return {"type": "use", "runtime": "python", "imports": lines}

    def module_list(self, items):
        return items

    def module(self, items):
        if len(items) == 2:
            return (items[0], items[1])
        return items[0]

    def start(self, items):
        return items

    def statement(self, items):
        return items[0] if len(items) == 1 else items

    def RAW(self, token):
        return token.value

    def STRING(self, token):
        return token.value[1:-1]


parser = Lark(
    curlang_grammar,
    parser="lalr",
    transformer=CurlangTransformer()
)


def command_to_code(cmd):
    t = cmd.get("type")

    if t == "find":
        runtime = "bash"
        f = shlex.quote(cmd["filename"])
        m = shlex.quote(cmd["message"])
        c = ""

        if cmd.get("block"):
            c = "\n".join(command_to_code(x) for x in cmd["block"])

        if cmd["negated"]:
            code = (
                f'if [ ! -f {f} ]; then\n'
                f'{c}\n'
                f'else\n'
                f'    echo {m}\n'
                f'fi'
            )
        else:
            code = (
                f'if [ -f {f} ]; then\n'
                f'{c}\n'
                f'else\n'
                f'    echo {m}\n'
                f'fi'
            )
        return f'# runtime: {runtime}\n{code}'
    elif t == "get":
        runtime = "bash"
        u = shlex.quote(cmd["url"])
        d = shlex.quote(cmd["destination"])
        dl = shlex.quote(
            f'Downloading from {cmd["url"]} to {cmd["destination"]}'
        )

        if cmd.get("block"):
            s, f_ = process_get_inner_block(cmd["block"])
            code = (
                f'echo {dl}\n'
                f'curl -L {u} -o {d}\n'
                f'ret=$?\n'
                f'if [ $ret -eq 0 ]; then\n'
                f'    {s}\n'
                f'else\n'
                f'    {f_}\n'
                f'fi'
            )
        else:
            code = f'echo {dl}\ncurl -L {u} -o {d}'
        return f'# runtime: {runtime}\n{code}'

    elif t == "cmd":
        runtime = "bash"
        code = cmd["command"]
        return f'# runtime: {runtime}\n{code}'

    elif t == "delete":
        runtime = "bash"
        target = shlex.quote(cmd["target"])
        code = f'rm -rf {target}'
        return f'# runtime: {runtime}\n{code}'

    elif t == "make":
        runtime = "bash"
        target = shlex.quote(cmd["target"])
        code = f'mkdir -p {target}'
        return f'# runtime: {runtime}\n{code}'

    elif t == "pass":
        runtime = "bash"
        m = shlex.quote(f'PASS: {cmd["message"]}')
        code = f'echo {m}'
        return f'# runtime: {runtime}\n{code}'

    elif t == "fail":
        runtime = "bash"
        m = shlex.quote(f'FAIL: {cmd["message"]}')
        code = f'echo {m}'
        return f'# runtime: {runtime}\n{code}'

    elif t == "print":
        runtime = "bash"
        m = shlex.quote(cmd["message"])
        code = f'echo {m}'
        return f'# runtime: {runtime}\n{code}'

    elif t == "use":
        runtime = "python"
        py_code = "\n".join(cmd.get("imports", []))

        code = (
            f"send_code_to_python_and_wait << 'EOF_CODE'\n"
            f"{py_code}\n"
            f"EOF_CODE"
        )
        return f'# runtime: {runtime}\n{code}'

    else:
        runtime = "bash"
        u = shlex.quote(f'Unknown command type: {cmd}')
        code = f'echo {u}'
        return f'# runtime: {runtime}\n{code}'


def process_get_inner_block(block):
    success_cmds = []
    failure_cmds = []

    for cmd in block:
        if not isinstance(cmd, dict):
            raise ValueError(f"Expected dict in get inner block, got: {cmd}")

        if cmd["type"] == "pass":
            runtime = "bash"
            msg = shlex.quote(f'PASS: {cmd["message"]}')
            success_cmds.append(f'# runtime: {runtime}\necho {msg}')
        elif cmd["type"] == "fail":
            runtime = "bash"
            msg = shlex.quote(f'FAIL: {cmd["message"]}')
            failure_cmds.append(f'# runtime: {runtime}\necho {msg}')
        elif cmd["type"] == "print":
            runtime = "bash"
            msg = shlex.quote(cmd["message"])
            success_cmds.append(f'# runtime: {runtime}\necho {msg}')
        else:
            runtime = "bash"
            unknown = shlex.quote(f'Unknown command type in get block: {cmd}')
            success_cmds.append(f'# runtime: {runtime}\necho {unknown}')
            failure_cmds.append(f'# runtime: {runtime}\necho {unknown}')
    return ("\n".join(success_cmds), "\n".join(failure_cmds))


def run_curlang_block(code):
    try:
        ast = parser.parse(code)
    except Exception as e:
        raise ValueError(e)

    r = []

    runtimes = set()

    for cmd in ast:
        if not isinstance(cmd, dict):
            raise ValueError(f"Expected a dict, but got: {cmd}")

        r.append(command_to_code(cmd))

        if "runtime" in cmd:
            runtimes.add(cmd["runtime"])

    final_code = "\n".join(r)

    if len(runtimes) == 1:
        overall_runtime = runtimes.pop()
    else:
        overall_runtime = "mixed(" + ", ".join(runtimes) + ")"
    return {"runtime": overall_runtime, "code": final_code}
