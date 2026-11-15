"""Automated checks for the CMPSC 100 Final Project.

Every project is different, so these checks read the shape of the code in src
rather than running it: they parse each file as Python and look for classes,
methods, docstrings, hardware, lists, dictionaries, loops and decisions. Strings
and comments do not count, so a word in a comment cannot pass a check. The one
check that runs code imports each class file on a pretend board, which catches a
syntax error or a missing import without needing your hardware.

When a check fails, the assertion message says what was found and what was
expected. gatorgrade does not show that message itself; it prints the pytest
command to run.
"""

import ast
import io
import subprocess
import sys
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def files():
    return sorted(path for path in SRC.glob("*.py") if path.name != "__init__.py")


def tree(path):
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as error:
        raise AssertionError(f"src/{path.name} has a syntax error on line {error.lineno}: {error.msg}") from None


def class_files():
    """The files in src other than main.py that define at least one class."""
    found = {}
    for path in files():
        if path.name == "main.py":
            continue
        classes = [node for node in tree(path).body if isinstance(node, ast.ClassDef)]
        if classes:
            found[path] = classes
    return found


def need_classes():
    found = class_files()
    assert found, "found no class files in src yet: write each class in its own file, such as src/sensor.py"
    return found


def all_nodes():
    for path in files():
        yield from ast.walk(tree(path))


def calls(name):
    """Calls such as ADC(4), Pin(...) or PWM(...), written as name(...) or machine.name(...)."""
    found = []
    for node in all_nodes():
        if isinstance(node, ast.Call):
            func = node.func
            if (isinstance(func, ast.Name) and func.id == name) or (isinstance(func, ast.Attribute) and func.attr == name):
                found.append(node)
    return found


def mentions(node, word):
    return any(isinstance(sub, ast.Attribute) and sub.attr == word for sub in ast.walk(node))


def test_main_brings_the_classes_together():
    main = SRC / "main.py"
    assert main.exists(), "src/main.py is missing: it is the file that runs your project"
    module = tree(main)
    assert ast.get_docstring(module), "src/main.py needs a docstring at the top that says what the project does"
    names = {path.stem for path in class_files()}
    imported = {node.module for node in ast.walk(module) if isinstance(node, ast.ImportFrom)}
    imported |= {alias.name for node in ast.walk(module) if isinstance(node, ast.Import) for alias in node.names}
    used = sorted(names & imported)
    assert len(used) >= 2, (
        f"src/main.py imports from {used or 'none'} of your class files, expected at least 2: "
        f"for example, from sensor import Sensor"
    )
    functions = [node.name for node in module.body if isinstance(node, ast.FunctionDef)]
    assert "main" in functions, "src/main.py needs a main() function, as in the labs"


def test_there_are_at_least_two_class_files():
    found = class_files()
    assert len(found) >= 2, (
        f"found classes in {len(found)} file(s) in src besides main.py, expected at least 2: one class to a file, "
        f"and a team has at least one file for each person"
    )


def test_each_class_has_init_and_two_more_methods():
    for path, classes in need_classes().items():
        for cls in classes:
            methods = [node.name for node in cls.body if isinstance(node, ast.FunctionDef)]
            others = [name for name in methods if name != "__init__"]
            assert "__init__" in methods and len(others) >= 2, (
                f"class {cls.name} in src/{path.name} has the methods {methods}, expected __init__ and at least two more"
            )


def test_methods_return_values():
    found = []
    for path, classes in class_files().items():
        for cls in classes:
            for method in cls.body:
                if isinstance(method, ast.FunctionDef) and method.name != "__init__":
                    if any(isinstance(node, ast.Return) and node.value is not None for node in ast.walk(method)):
                        found.append(f"{cls.name}.{method.name}")
    assert len(found) >= 2, (
        f"found {len(found)} method(s) that return a value ({found}), expected at least 2: a method that answers "
        f"a question about its object returns the answer"
    )


def test_each_class_and_function_has_a_docstring():
    need_classes()
    missing = []
    for path in files():
        for node in ast.walk(tree(path)):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not ast.get_docstring(node):
                missing.append(f"{node.name} in src/{path.name}")
    assert not missing, f"these have no docstring: {', '.join(missing)}. Say in one sentence what each one does"


def test_the_project_reads_an_input():
    inputs = [node for node in calls("Pin") if mentions(node, "IN")] + calls("ADC") + calls("DHT22")
    assert inputs, (
        "found no input on the board: a button is Pin(number, Pin.IN, Pin.PULL_UP), the light sensor and the "
        "chip's temperature sensor are read with ADC, and the DHT22 is dht.DHT22(Pin(number))"
    )


def test_the_project_drives_an_output():
    outputs = [node for node in calls("Pin") if mentions(node, "OUT")] + calls("PWM")
    assert outputs, "found no output on the board: an LED is Pin(number, Pin.OUT), and the buzzer is PWM(Pin(number))"


def test_the_project_uses_a_list_and_a_dictionary():
    nodes = list(all_nodes())
    lists = [node for node in nodes if isinstance(node, ast.List)] + calls("list") + calls("append")
    dicts = [node for node in nodes if isinstance(node, ast.Dict)] + calls("dict")
    assert lists, "found no list in src: for example, a list of readings, scores or Pins"
    assert dicts, "found no dictionary in src: for example, a dictionary of lights, counts or settings"


def test_the_project_uses_a_loop_and_a_decision():
    nodes = list(all_nodes())
    assert any(isinstance(node, (ast.For, ast.While)) for node in nodes), "found no for or while loop in src"
    ifs = [node for node in nodes if isinstance(node, ast.If) and not (
        isinstance(node.test, ast.Compare) and isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__")]
    assert ifs, "found no if statement in src, besides the one that calls main()"


def test_each_class_file_imports_on_a_pretend_board():
    for path in need_classes():
        result = subprocess.run(
            [sys.executable, "-c", f"import mockro\nimport {path.stem}"],
            cwd=SRC, capture_output=True, text=True, timeout=10, check=False,
        )
        last = result.stderr.strip().splitlines()[-1:] or [""]
        assert result.returncode == 0, f"importing src/{path.name} stopped with: {last[0]}"


def test_no_file_has_a_todo():
    for path in files():
        assert "TODO" not in path.read_text(encoding="utf-8"), (
            f"src/{path.name} still has a TODO marker: delete each one once its code is written, including Author"
        )


def test_each_file_has_two_comments():
    for path in files():
        text = path.read_text(encoding="utf-8")
        found = [tok.string for tok in tokenize.generate_tokens(io.StringIO(text).readline)
                 if tok.type == tokenize.COMMENT and "TODO" not in tok.string]
        assert len(found) >= 2, (
            f"src/{path.name} has {len(found)} comment(s) besides TODO markers, expected at least 2: say why, not what"
        )


def git(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)
    return result.stdout


def test_pull_requests_were_merged():
    subjects = git("log", "--merges", "--format=%s").splitlines()
    merged = [subject for subject in subjects if "pull request" in subject.lower()]
    assert len(merged) >= 2, (
        f"found {len(merged)} merged pull requests, expected at least 2. Merge with Merge pull request, not Squash "
        f"and merge, and pull main before you run this check"
    )
