from typing import Any, Dict
from fastapi import HTTPException

def response_success(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    return {
        "status": "success",
        "data": data,
        "message": message
    }

def response_error(status_code: int, detail: str):
    raise HTTPException(
        status_code=status_code,
        detail={"status": "error", "message": detail}
    )