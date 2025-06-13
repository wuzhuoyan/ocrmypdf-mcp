import uvicorn
from fastapi import FastAPI
from fastmcp import FastMCP
from ocr_my_pdf_api import router as ocr_pdf_router
from health import router as health_router

# mcp = FastMCP(name="MyAssistantServer")

# mcp.run()
app = FastAPI()
app.include_router(ocr_pdf_router)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)
