import builtins
import requests

class PyDusHelper:
    def __init__(self):
        self.api_url = "https://pydust.onrender.com/help"
    
    def get_help(self, query: str) -> str:
        """Get Python help by calling the remote API."""
        try:
            response = requests.post(
                self.api_url,
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Error: Could not connect to help service - {str(e)}"

# Create a global helper instance
_helper = None

def help(obj=None):
    """Enhanced Python help function using remote API."""
    global _helper
    
    # Initialize helper if needed
    if _helper is None:
        _helper = PyDusHelper()
    
    # If no argument, use Python's original help
    if obj is None:
        return builtins.__help__()
    
    # If it's a string, treat it as a question
    if isinstance(obj, str):
        response = _helper.get_help(obj)
        print(response)
        return
    
    # For other objects, try to get AI help
    try:
        # Get object information
        obj_type = type(obj).__name__
        obj_doc = getattr(obj, '__doc__', '')
        obj_name = getattr(obj, '__name__', str(obj))
        
        # Create a detailed query about the object
        query = f"Explain Python object: {obj_name} of type {obj_type}.\n"
        if obj_doc:
            query += f"Documentation: {obj_doc}\n"
        
        response = _helper.get_help(query)
        print(response)
        
    except Exception as e:
        # Fall back to original help if AI fails
        return builtins.__help__(obj)

def install():
    """Install the enhanced help function."""
    if not hasattr(builtins, '__help__'):
        builtins.__help__ = builtins.help
    builtins.help = help

def restore():
    """Restore Python's original help() function."""
    if hasattr(builtins, '__help__'):
        builtins.help = builtins.__help__
        delattr(builtins, '__help__')
        print("Restored original Python help()")

# Store original help function when module is imported
if not hasattr(builtins, '__help__'):
    builtins.__help__ = builtins.help

# Replace built-in help with our version
builtins.help = help 