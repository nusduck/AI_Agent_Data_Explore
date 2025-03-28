from e2b_code_interpreter import Sandbox


def upload_file_to_sandbox(sandbox: Sandbox, local_path: str) -> str:
    """
    Upload a local file to the sandbox environment
    
    Args:
        local_path: Path to the file on local filesystem
        sandbox_path: Destination path in sandbox environment
        
    Returns:
        str: Path to the uploaded file in sandbox
    """
    # Read file from local filesystem
    with open(local_path, "rb") as file:
        # Upload file to sandbox
        sandbox.files.write(local_path, file)
    return 
