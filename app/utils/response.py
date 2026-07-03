def success_response(data=None, meta=None, message="success"):
    return {"status": "success", "message": message, "data": data, "meta": meta}


def error_response(message="error", code=400):
    return {"status": "error", "message": message, "code": code}
