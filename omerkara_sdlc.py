#!/usr/bin/env python3
"""
Ömer Kara SDLC Skill - Project context initialization
Fetches tasks and documentation from n8n task API
"""

import os
import json
import httpx
import asyncio
from datetime import datetime

async def main():
    """Initialize project context from n8n task API"""
    
    # Get configuration
    task_token = os.getenv("TASK_TOKEN")
    task_api = os.getenv("TASK_API", "https://n8n.omerkara.com/webhook")
    task_project = os.getenv("TASK_PROJECT")
    
    # Prompt for TASK_TOKEN if not set
    if not task_token:
        print("🔐 TASK_TOKEN required")
        print("   Get your token from: https://tasks.omerkara.com/login")
        print()
        task_token = input("Enter TASK_TOKEN: ").strip()
        if not task_token:
            print("❌ TASK_TOKEN is required")
            return
    
    # Prompt for TASK_PROJECT if not set
    if not task_project:
        print("📦 TASK_PROJECT required")
        print("   Which project are you working on?")
        print("   (e.g., rivalsense, duqme, deployment-orchestrator)")
        print()
        task_project = input("Enter TASK_PROJECT: ").strip()
        if not task_project:
            print("❌ TASK_PROJECT is required")
            return
    
    print(f"📦 Initializing project context...")
    print(f"   Project: {task_project}")
    print(f"   API: {task_api}")
    print()
    
    headers = {"X-Task-Token": task_token}
    
    # Fetch tasks
    print("📋 Loading tasks...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{task_api}/tasks",
                params={"project": task_project, "status": "open"},
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            tasks = response.json().get("tasks", [])
            print(f"   ✅ Loaded {len(tasks)} open tasks")
            for task in tasks[:5]:  # Show first 5
                print(f"      • {task.get('title')} (#{task.get('id')})")
            if len(tasks) > 5:
                print(f"      ... and {len(tasks) - 5} more")
    except Exception as e:
        print(f"   ❌ Failed to load tasks: {e}")
        return
    
    print()
    
    # Fetch documents
    print("📄 Loading documentation...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{task_api}/documents",
                params={"project": task_project},
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            documents = response.json().get("documents", [])
            doc_names = [doc.get("name") for doc in documents]
            print(f"   ✅ Loaded {len(doc_names)} documents")
            for name in doc_names:
                print(f"      • {name}")
    except Exception as e:
        print(f"   ⚠️  Failed to load documents: {e}")
        doc_names = []
    
    print()
    print("✨ Project context ready!")
    print()
    print(f"📊 Summary:")
    print(f"   • Tasks: {len(tasks)}")
    print(f"   • Documents: {len(doc_names)}")
    print(f"   • Status: Ready to develop")
    print()

if __name__ == "__main__":
    asyncio.run(main())
