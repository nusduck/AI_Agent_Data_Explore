from e2b_code_interpreter import Sandbox
import builtins
import contextlib
import io
from typing import Any

from utils.file_operate_e2b import upload_file_to_sandbox


def eval(code: str, _locals: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    # Store original keys before execution
    original_keys = set(_locals.keys())

    try:
        with contextlib.redirect_stdout(io.StringIO()) as f:
            exec(code, builtins.__dict__, _locals)
        result = f.getvalue()
        if not result:
            result = "<code ran, no output printed to stdout>"
    except Exception as e:
        result = f"Error during execution: {repr(e)}"

    # Determine new variables created during execution
    new_keys = set(_locals.keys()) - original_keys
    new_vars = {key: _locals[key] for key in new_keys}
    return result, new_vars

def e2b_code_executor(code: str, _locals: dict[str, Any]):
    """
    Execute code in a sandbox environment with a given data path.

    Args:
        code (str): The code to execute.
        datapath (str): The path to the data file to upload to the sandbox.
    """
    #datapath = _locals["raw_data_path"]
    sandbox = Sandbox()
    #upload_file_to_sandbox(sandbox, datapath)
    result = sandbox.run_code(code)
    return result

