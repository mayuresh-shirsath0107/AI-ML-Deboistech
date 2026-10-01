"""
Project Memory & Documentation MCP
==================================

A small FastMCP server that lets an AI assistant keep long-term notes about a
project OUTSIDE the chat window, as Markdown files on disk.

It exposes exactly three MCP primitives:

    TOOL      save_project_memory        -> writes / updates project memory  (action)
    RESOURCE  project://{project_name}   -> reads project memory back        (read-only data)
    PROMPT    project_documentation      -> reusable documentation template  (user-selected)

Run locally (stdio):   python server.py

----------------------------------------------------------------------------
WHICH PATHS DO *YOU* NEED TO SET?
----------------------------------------------------------------------------
1. Inside this file: NOTHING. Memory is stored in the "projects" folder next
   to this file, so it works on any machine after `git clone`.

2. OPTIONAL: to store memories somewhere else, set the environment variable
       PROJECT_MEMORY_DIR=<a folder on your PC>
   e.g.  C:\\Users\\<you>\\Documents\\project-memory   (Windows)
         /home/<you>/project-memory                    (Linux / macOS)

3. In Claude Desktop's config file (claude_desktop_config.json) you MUST give
   the full path to (a) your Python and (b) this server.py.
   See README.md -> "Connecting to Claude Desktop" for the exact JSON.
----------------------------------------------------------------------------

NOTE: This server talks to the client over stdio, so never use print() in this
file. Anything written to stdout would corrupt the MCP protocol messages.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

from fastmcp import FastMCP
from pydantic import BaseModel  # installed automatically together with fastmcp

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

# Default: <repo>/projects   (relative to this file, no personal paths).
# Optional override: set the PROJECT_MEMORY_DIR environment variable.
PROJECTS_DIR = Path(os.environ.get("PROJECT_MEMORY_DIR") or BASE_DIR / "projects")

MEMORY_FILENAME = "project_memory.md"
SUMMARIES_DIRNAME = "summaries"
NOT_PROVIDED = "Not provided"

# (heading in the Markdown file, name of the tool argument that fills it)
SECTIONS: list[tuple[str, str]] = [
    ("Project Overview", "conversation_summary"),
    ("Requirements", "requirements"),
    ("Technologies", "technologies"),
    ("Important Decisions", "important_decisions"),
    ("Current Status", "current_status"),
    ("Problems and Solutions", "problems_and_solutions"),
    ("Future Improvements", "future_improvements"),
    ("Next Steps", "next_steps"),
]
LAST_UPDATED = "Last Updated"


class SaveResult(BaseModel):
    """Structured result returned by the save_project_memory tool."""

    status: str  # "success" or "error"
    project: str  # sanitized project name (empty string on error)
    path: str  # path of project_memory.md (empty string on error)
    summary_file: str  # path of the timestamped summary (empty string on error)
    message: str  # human readable explanation


# ---------------------------------------------------------------------------
# Helper functions (plain Python - NOT exposed through MCP)
# ---------------------------------------------------------------------------


def sanitize_project_name(name: str) -> str:
    """Turn a user-supplied project name into a safe folder name.

    Only letters, digits, spaces, "_" and "-" are kept. Everything else
    (including "/", "\\" and ".") becomes "_", and leading/trailing
    separators are removed. So "../../secret" becomes "secret" and can never
    point outside the projects folder.

    Raises ValueError if nothing usable is left.
    """
    cleaned = re.sub(r"[^A-Za-z0-9 _-]", "_", name.strip())
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned[:64].strip(" _.-")
    if not cleaned:
        raise ValueError("Project name is empty or has no usable characters.")
    return cleaned


def get_project_dir(name: str) -> Path:
    """Return projects/<safe name>, and double-check it stays inside PROJECTS_DIR."""
    folder = (PROJECTS_DIR / sanitize_project_name(name)).resolve()
    if PROJECTS_DIR.resolve() not in folder.parents:
        raise ValueError("Project folder must be inside the projects directory.")
    return folder


def display_path(path: Path) -> str:
    """Show paths relative to the repo when possible (nicer output, no personal paths)."""
    try:
        return path.relative_to(BASE_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def parse_sections(text: str) -> dict[str, str]:
    """Read an existing project_memory.md back into {heading: text}.

    Only our own known headings are treated as section boundaries, so if the
    saved text itself contains a "## Something" line it is kept as content.
    """
    known = {heading for heading, _ in SECTIONS} | {LAST_UPDATED}
    sections: dict[str, str] = {}
    current: str | None = None
    lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("## ") and line[3:].strip() in known:
            if current:
                sections[current] = "\n".join(lines).strip()
            current, lines = line[3:].strip(), []
        elif current:
            lines.append(line)
    if current:
        sections[current] = "\n".join(lines).strip()
    sections.pop(LAST_UPDATED, None)
    return sections


def render_memory(project: str, sections: dict[str, str], timestamp: str) -> str:
    """Build the full Markdown text of project_memory.md."""
    parts = [f"# {project} — Project Memory\n"]
    for heading, _ in SECTIONS:
        parts.append(f"## {heading}\n\n{sections.get(heading) or NOT_PROVIDED}\n")
    parts.append(f"## {LAST_UPDATED}\n\n{timestamp}\n")
    return "\n".join(parts)


def save_memory(project_name: str, values: dict[str, str]) -> SaveResult:
    """Core logic of the tool: validate, create folder, merge, write files."""
    try:
        project = sanitize_project_name(project_name)
        folder = get_project_dir(project_name)
    except ValueError as error:
        return SaveResult(
            status="error", project="", path="", summary_file="", message=str(error)
        )

    folder.mkdir(parents=True, exist_ok=True)
    memory_file = folder / MEMORY_FILENAME

    # Keep older information: an empty argument does not erase an existing section.
    existing: dict[str, str] = {}
    if memory_file.exists():
        existing = parse_sections(memory_file.read_text(encoding="utf-8"))

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    merged: dict[str, str] = {}
    submitted: list[str] = []
    for heading, arg in SECTIONS:
        new_text = (values.get(arg) or "").strip()
        if new_text:
            merged[heading] = new_text
            submitted.append(f"## {heading}\n\n{new_text}\n")
        else:
            merged[heading] = existing.get(heading) or NOT_PROVIDED

    memory_file.write_text(render_memory(project, merged, timestamp), encoding="utf-8")

    # One small timestamped file per save, so there is a history of what was added.
    summaries = folder / SUMMARIES_DIRNAME
    summaries.mkdir(exist_ok=True)
    summary_file = summaries / f"{now.strftime('%Y-%m-%d-%H%M%S')}-summary.md"
    summary_file.write_text(
        f"# {project} — Summary ({timestamp})\n\n" + "\n".join(submitted),
        encoding="utf-8",
    )

    return SaveResult(
        status="success",
        project=project,
        path=display_path(memory_file),
        summary_file=display_path(summary_file),
        message="Project memory saved successfully.",
    )


def read_memory(project_name: str) -> str:
    """Core logic of the resource: return the saved Markdown, or a friendly message."""
    name = unquote(project_name)  # "My%20Project" -> "My Project"
    try:
        memory_file = get_project_dir(name) / MEMORY_FILENAME
    except ValueError as error:
        return f"Invalid project name: {error}"
    if not memory_file.is_file():
        return f"Project memory for '{name}' does not exist yet."
    return memory_file.read_text(encoding="utf-8")


def build_documentation_prompt(project_name: str, conversation_content: str) -> str:
    """Build the instruction text used by the prompt."""
    if conversation_content.strip():
        source = f"Here is the project discussion to organize:\n\n---\n{conversation_content}\n---"
    else:
        source = "Use the project discussion from this conversation as your source material."

    return f"""You are helping me write persistent project documentation for the project "{project_name}".

{source}

Organize the discussion into clean Markdown using exactly these sections:

# Project Overview
# Problem Being Solved
# Requirements
# Architecture / Design
# Technologies Used
# Important Decisions
# Current Progress
# Problems / Issues
# Solutions
# Future Improvements
# Next Steps
# Important Notes

Rules:
- Do not invent information. Only use what is in the discussion.
- If a section has no information, write "Not discussed yet" instead of guessing.
- Preserve important technical decisions, and include the reason for each one when it was given.
- Separate confirmed information (decided / implemented) from ideas that are only suggestions or possibilities.
- Keep the project-specific names, features and details. Do not replace them with generic wording.
- At the end, add a short list called "Missing Information" with things that are unclear or should be confirmed.
- The output must be clean Markdown that can be stored as long-term project memory.

Only produce the documentation. Do not save it anywhere in this step."""


# ---------------------------------------------------------------------------
# MCP server: exactly ONE tool, ONE resource (template) and ONE prompt
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="Project Memory & Documentation MCP",
    instructions=(
        "Keeps project knowledge in Markdown files outside the chat. "
        "Use save_project_memory to store it, read the project://{project_name} "
        "resource to load it back, and the project_documentation prompt to "
        "structure a project discussion."
    ),
)


@mcp.tool
def save_project_memory(
    project_name: str,
    conversation_summary: str,
    requirements: str = "",
    technologies: str = "",
    important_decisions: str = "",
    current_status: str = "",
    problems_and_solutions: str = "",
    future_improvements: str = "",
    next_steps: str = "",
) -> SaveResult:
    """Save or update the persistent memory of a project as a Markdown file.

    What it does:
        Creates (or updates) projects/<project_name>/project_memory.md and also
        writes a timestamped summary in projects/<project_name>/summaries/.
        This changes files on disk. Each project has its own folder, so
        different projects never mix. Fields left empty keep their old value
        when the project already exists; on a new project they show as
        "Not provided".

    When the assistant should call it:
        Call it during a conversation when important project information has
        come up that should survive after the chat ends: goals, requirements,
        architecture or technology choices, decisions and their reasons,
        bugs and fixes, progress, or a TODO list. Also call it when the user
        asks to "save", "remember" or "store" the project. Do not call it for
        small talk or for information that is not about a concrete project.
        Only write what was actually discussed - never invent details.

    Args:
        project_name: Name of the project, e.g. "FINITI". Unsafe characters
            such as "/" or ".." are replaced, so it can not leave the projects folder.
        conversation_summary: Short summary of what the project is and what was
            discussed (purpose, features, overall idea).
        requirements: Confirmed requirements or constraints. Optional.
        technologies: Languages, frameworks, libraries, tools chosen. Optional.
        important_decisions: Key decisions and why they were made. Optional.
        current_status: What is done and what is in progress. Optional.
        problems_and_solutions: Bugs or issues and how they were solved. Optional.
        future_improvements: Ideas for later, not yet decided. Optional.
        next_steps: Concrete TODO items. Optional.

    Returns:
        SaveResult with status ("success" or "error"), project (the sanitized
        name), path (project_memory.md), summary_file (the new timestamped
        summary) and message.
    """
    values = {
        "conversation_summary": conversation_summary,
        "requirements": requirements,
        "technologies": technologies,
        "important_decisions": important_decisions,
        "current_status": current_status,
        "problems_and_solutions": problems_and_solutions,
        "future_improvements": future_improvements,
        "next_steps": next_steps,
    }
    return save_memory(project_name, values)


@mcp.resource("project://{project_name}", mime_type="text/markdown")
def project_memory_resource(project_name: str) -> str:
    """Read-only project memory, addressed by URI, e.g. project://FINITI.

    Returns the contents of projects/<project_name>/project_memory.md so the
    client can load earlier project context into the conversation. It never
    creates or changes any file. If the project has no saved memory yet, a
    short "does not exist yet" message is returned instead of an error.
    """
    return read_memory(project_name)


@mcp.prompt
def project_documentation(project_name: str, conversation_content: str = "") -> str:
    """Reusable template: turn a project discussion into structured documentation.

    Selected on purpose by the user (for example from the prompt menu in
    Claude Desktop). It asks the assistant to organize the discussion into
    fixed sections (Overview, Requirements, Architecture, Decisions, Progress,
    Next Steps, ...) without inventing anything. It only produces
    instructions - it does not save files; saving is done by the
    save_project_memory tool.

    Args:
        project_name: Name of the project, e.g. "FINITI".
        conversation_content: The discussion text to organize. Optional: if
            left empty, the assistant uses the current conversation.
    """
    return build_documentation_prompt(project_name, conversation_content)


if __name__ == "__main__":
    mcp.run()  # stdio transport (default) - used by Claude Desktop and MCP Inspector
