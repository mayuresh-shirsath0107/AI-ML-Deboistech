# Project Memory MCP — Project Memory

## Project Overview

Student assignment (MCP Fundamentals, 40 marks): a FastMCP server called "Project Memory & Documentation MCP" that stores long-running project knowledge (decisions, architecture, bugs, status, TODOs) as Markdown files outside the chat. Each project gets its own folder under projects/<name>/ with project_memory.md and a summaries/ folder. The server exposes exactly three MCP primitives: one tool, one resource template and one prompt.

## Requirements

- Exactly 1 tool, 1 resource (template) and 1 prompt, no extra primitives
- Tool: save_project_memory (writes/updates Markdown, returns structured result)
- Resource: project://{project_name} (read-only, text/markdown, friendly message when missing)
- Prompt: project_documentation (reusable template, never saves files)
- Path-safe project names, no machine-specific paths, no secrets or .env committed
- Deliverables: server.py, pyproject.toml/requirements.txt, .gitignore, README (with WHY for each primitive), docs (system design, testing, assignment mapping), tests, diagram
- All three primitives verified via MCP Inspector or Claude Desktop

## Technologies

Python, FastMCP (fastmcp>=2.10), pydantic (comes with fastmcp), pathlib, pytest, MCP Inspector (npx), uv, Claude Desktop (stdio), Markdown files for storage

## Important Decisions

- Markdown files instead of a database: simple, readable by humans and MCP clients
- One folder per project so projects never mix
- Empty fields on update keep old values instead of wiping them; new projects show "Not provided"
- Project names are sanitized (e.g. ../../x becomes x) and the final folder is checked to stay inside projects/
- Core logic lives in plain helper functions; decorated MCP functions are thin wrappers, which makes testing easy
- .gitignore ignores personal project memories but keeps projects/.gitkeep and the Demo-FINITI example
- Inspector command npx @modelcontextprotocol/inspector python server.py chosen because it works across FastMCP versions

## Current Status

Project files were generated: server.py, README, docs, tests, pyproject.toml, requirements.txt, .gitignore, LICENSE, demo project. The 15 plain-Python logic tests were run against stubs and passed; the FastMCP protocol tests could not be run in the build environment. The user configured Claude Desktop with uv (--directory ... run server.py) and the server connected, so the tool is being tested live now.</current_status>
<parameter name="problems_and_solutions">- fastmcp/pytest could not be installed in the build sandbox (no network): logic was tested with stubs, and the user must run the real tests locally
- Connector showing "starting" in Claude Desktop: run uv run server.py once in a terminal so dependencies download, then fully quit and reopen Claude Desktop
- Python 3.14 in use (__pycache__ shows cpython-314): if install fails, use uv run --python 3.12
- Stray test_server.py in project root and a duplicate "project-memory-mcp copy" folder should be removed before pushing to GitHub</problems_and_solutions>
<parameter name="future_improvements">Not decided yet. The assignment limits the server to exactly three primitives, so no list/delete/search tools.

## Problems and Solutions

Not provided

## Future Improvements

Not provided

## Next Steps

- Check that projects/Project Memory MCP/project_memory.md and a summaries/ file were created
- Read the memory back through the project://Project Memory MCP resource in a new chat
- Try the project_documentation prompt from the + menu
- Take screenshots of tool, resource and prompt for docs/testing.md
- Run python -m pytest locally and the MCP Inspector
- Add your name to LICENSE, delete the duplicate folder, then push to GitHub</next_steps>

## Last Updated

2026-10-01 17:43:33
