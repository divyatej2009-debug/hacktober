import platform
import datetime

def get_system_diagnostic() -> dict:
    """
    Collects basic system and environment metrics to test local tool execution.
    """
    return {
        "status": "online",
        "system": platform.system(),
        "python_version": platform.python_version(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

# Tool declaration mapping for OpenAI API function calling
DIAGNOSTIC_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_system_diagnostic",
        "description": "Retrieve local system diagnostics and operational status.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}
