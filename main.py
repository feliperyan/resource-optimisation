from cons_based_resource_alloc.cakespies import runExample

import uvicorn
import os

port = os.environ.get("PORT", "8000")
port = int(port)

if __name__ == "__main__":
    uvicorn.run("cons_based_resource_alloc.server:app", host="0.0.0.0", port=port, log_level="info")
