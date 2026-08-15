#!/usr/bin/env python3
"""
Ömer Kara SDLC Skill - Project context initialization
Fetches tasks and documentation from n8n task API
Supports task and document management
"""

import os
import json
import httpx
import asyncio
import sys
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
    
    # Offer interactive mode
    print("Would you like to manage tasks/documents? (y/n)")
    response = input("Enter choice: ").strip().lower()
    if response == 'y':
        await handle_interactive_commands(task_token, task_api, task_project)

async def create_task(task_token: str, task_api: str, task_project: str, title: str, priority: str = "medium", assignee: str = None):
    """Create a new task in n8n"""
    headers = {"X-Task-Token": task_token}
    payload = {
        "project": task_project,
        "title": title,
        "priority": priority,
        "status": "todo"
    }
    if assignee:
        payload["assignee"] = assignee
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{task_api}/tasks/create",
                json=payload,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            task = response.json().get("task", {})
            print(f"✅ Created task: {title} (#{task.get('id')})")
            return task
    except Exception as e:
        print(f"❌ Failed to create task: {e}")
        return None


async def update_task(task_token: str, task_api: str, task_id: str, status: str = None, title: str = None, priority: str = None):
    """Update an existing task"""
    headers = {"X-Task-Token": task_token}
    payload = {"id": task_id}
    if status:
        payload["status"] = status
    if title:
        payload["title"] = title
    if priority:
        payload["priority"] = priority
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{task_api}/tasks/update",
                json=payload,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            print(f"✅ Updated task #{task_id}")
            return response.json().get("task")
    except Exception as e:
        print(f"❌ Failed to update task: {e}")
        return None


async def upsert_document(task_token: str, task_api: str, task_project: str, name: str, content: str):
    """Create or update a document (PROMPT, SCOPE, etc.)"""
    headers = {"X-Task-Token": task_token}
    payload = {
        "project": task_project,
        "name": name,
        "content": content
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{task_api}/documents/upsert",
                json=payload,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            print(f"✅ Saved document: {name}")
            return response.json().get("document")
    except Exception as e:
        print(f"❌ Failed to save document: {e}")
        return None


async def delete_task(task_token: str, task_api: str, task_id: str):
    """Delete a task"""
    headers = {"X-Task-Token": task_token}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{task_api}/tasks/delete",
                json={"id": task_id},
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            print(f"✅ Deleted task #{task_id}")
            return True
    except Exception as e:
        print(f"❌ Failed to delete task: {e}")
        return False


async def handle_interactive_commands(task_token: str, task_api: str, task_project: str):
    """Allow interactive task/document management"""
    print()
    print("💡 Available commands:")
    print("   create-task <title>              Create new task")
    print("   update-task <id> <status>        Update task status (todo, in_progress, done)")
    print("   save-doc [name]                  Save document (prompts for type if not specified)")
    print("   delete-task <id>                 Delete task")
    print("   doc-types                        Show all available document types")
    print("   help                             Show this help message")
    print("   exit                             Exit skill")
    print()
    print("Examples:")
    print("   save-doc DESIGN_SYSTEM           → Prompt for content")
    print("   update-task 1 in_progress        → Start task")
    print("   create-task Add login flow       → Create new task")
    print()
    print("💡 Tip: Use 'doc-types' to see all available document types")
    print()
    
    while True:
        try:
            cmd = input("Command: ").strip().split(" ", 1)
            if not cmd or not cmd[0]:
                continue
            
            command = cmd[0]
            args = cmd[1] if len(cmd) > 1 else ""
            
            if command == "exit":
                print("👋 Goodbye!")
                break
            elif command == "help":
                print()
                print("💡 Available commands:")
                print("   create-task <title>              Create new task")
                print("   update-task <id> <status>        Update task status (todo, in_progress, done)")
                print("   save-doc [name]                  Save document (prompts for type if not specified)")
                print("   delete-task <id>                 Delete task")
                print("   doc-types                        Show all available document types")
                print("   help                             Show this help message")
                print("   exit                             Exit skill")
                print()
                print("Examples:")
                print("   save-doc DESIGN_SYSTEM           → Prompt for content")
                print("   update-task 1 in_progress        → Start task")
                print("   create-task Add login flow       → Create new task")
                print()
                continue
            elif command == "create-task":
                if not args:
                    title = input("Task title: ").strip()
                else:
                    title = args
                if title:
                    await create_task(task_token, task_api, task_project, title)
            elif command == "update-task":
                parts = args.split(" ", 1)
                if len(parts) >= 2:
                    task_id, status = parts[0], parts[1]
                    await update_task(task_token, task_api, task_id, status=status)
                else:
                    print("Usage: update-task <id> <status>")
            elif command == "save-doc":
                if args.strip():
                    name = args.strip()
                else:
                    print("Document types:")
                    print("  Project: PROMPT, SCOPE, ARCHITECTURE, DEPLOYMENT")
                    print("  Design: DESIGN, DESIGN_SYSTEM, UI_GUIDELINES, STYLE_GUIDE,")
                    print("          DESIGN_TOKENS, WIREFRAMES, PROTOTYPES, COMPONENT_LIBRARY,")
                    print("          ACCESSIBILITY, BRAND_GUIDELINES")
                    name = input("Document name: ").strip().upper()
                
                if name:
                    print(f"Enter content for {name} (Ctrl+D or Ctrl+Z then Enter to finish):")
                    lines = []
                    try:
                        while True:
                            line = input()
                            lines.append(line)
                    except EOFError:
                        pass
                    content = "\n".join(lines)
                    if content.strip():
                        await upsert_document(task_token, task_api, task_project, name, content)
                    else:
                        print("No content provided")
                else:
                    print("Document name required")
            elif command == "delete-task":
                task_id = args.strip()
                if task_id:
                    await delete_task(task_token, task_api, task_id)
                else:
                    print("Usage: delete-task <id>")
            elif command == "doc-types":
                print()
                print("📋 Available Document Types:")
                print()
                print("🎯 Project Documents:")
                print("   PROMPT          — Project requirements and objectives")
                print("   SCOPE           — Project scope and boundaries")
                print("   ARCHITECTURE    — Architecture decisions and patterns")
                print("   DEPLOYMENT      — Deployment guide and procedures")
                print()
                print("🎨 Design Documents:")
                print("   DESIGN          — General design overview")
                print("   DESIGN_SYSTEM   — Design system specification")
                print("   UI_GUIDELINES   — UI/UX guidelines and standards")
                print("   STYLE_GUIDE     — Visual style guide")
                print("   DESIGN_TOKENS   — Colors, typography, spacing, etc.")
                print("   WIREFRAMES      — Wireframe documentation")
                print("   PROTOTYPES      — Prototype specifications")
                print("   COMPONENT_LIBRARY — Component library docs")
                print("   ACCESSIBILITY   — Accessibility guidelines (WCAG, a11y)")
                print("   BRAND_GUIDELINES — Brand guidelines and identity")
                print()
                print("💡 Usage: save-doc <type_name>")
                print()
                continue
            else:
                print(f"Unknown command: {command}")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
    
    # Check for command-line arguments
    if len(sys.argv) > 1:
        # Could be used for non-interactive mode
        pass
