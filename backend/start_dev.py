#!/usr/bin/env python3
"""
Development server startup script for Lounarilaskuri API
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable hot reload for development
        reload_dirs=["src"],  # Watch src directory for changes
    )
