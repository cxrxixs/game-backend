# myapp/hooks.py


def exclude_api_paths(result, generator, request, public):
    """
    Exclude paths that start with '/api/' from the OpenAPI schema.
    """
    # Check if result has a 'paths' key
    if isinstance(result, dict) and "paths" in result:
        original_paths = result["paths"]
        # Filter out any path starting with '/api/'
        filtered_paths = {path: methods for path, methods in original_paths.items() if not path.startswith("/api/")}
        result["paths"] = filtered_paths
    return result
