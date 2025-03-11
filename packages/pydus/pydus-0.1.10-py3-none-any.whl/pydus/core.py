import builtins
import requests

class PyDusHelper:
    def __init__(self):
        self.api_url = "https://pydusk.onrender.com/help"
        self.call_count = 0
    
    def get_help(self, query: str) -> str:
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

_helper = None

def help(obj=None):
    global _helper
    
    if _helper is None:
        _helper = PyDusHelper()
    
    _helper.call_count = (_helper.call_count + 1) % 5
    
    if _helper.call_count != 0:
        return builtins.__help__(obj)
    
    if obj is None:
        return builtins.__help__()
    
    if isinstance(obj, str):
        response = _helper.get_help(obj)
        print(response)
        return
    
    try:
        obj_type = type(obj).__name__
        obj_doc = getattr(obj, '__doc__', '')
        obj_name = getattr(obj, '__name__', str(obj))
        
        query = f"Explain Python object: {obj_name} of type {obj_type}.\n"
        if obj_doc:
            query += f"Documentation: {obj_doc}\n"
        
        response = _helper.get_help(query)
        print(response)
        
    except Exception as e:
        return builtins.__help__(obj)

def install():
    if not hasattr(builtins, '__help__'):
        builtins.__help__ = builtins.help
    builtins.help = help

def restore():
    if hasattr(builtins, '__help__'):
        builtins.help = builtins.__help__
        delattr(builtins, '__help__')

if not hasattr(builtins, '__help__'):
    builtins.__help__ = builtins.help

builtins.help = help 