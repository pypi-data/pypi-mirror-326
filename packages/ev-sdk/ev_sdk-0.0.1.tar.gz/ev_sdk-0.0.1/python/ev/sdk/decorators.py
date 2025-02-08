from functools import wraps
from typing import Optional, Dict, List, Any
import inspect
import os

def job(
    name: str,
    python_version: str,
    dependencies: Optional[List[str]] = None,
    env_vars: Optional[Dict[str, str]] = None,
) -> Any:
    """Decorator to mark a function as a job.
    
    Args:
        name: Name of the job
        python_version: Python version to use for running the job
        dependencies: List of pip dependencies
        env_vars: Environment variables to set for the job
    
    Returns:
        A decorated function that can be run locally or submitted as a job
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Normal function call, bypasses job infrastructure"""
            return func(*args, **kwargs)

        # Attach metadata to the wrapper function
        wrapper.job_config = {
            "name": name,
            "python_version": python_version,
            "dependencies": dependencies,
            "env_vars": env_vars,
            "module_path": os.path.abspath(inspect.getfile(func)),
            "function_name": func.__name__,
        }
        return wrapper
    return decorator 