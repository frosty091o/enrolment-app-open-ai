"""Lab 7 MCP server exposing four read-only project tools."""

from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

from tools import (
    get_student_count,
    get_students_by_subject,
    list_project_files,
    read_ci_report,
)


mcp = MCPServer("Student Enrolment MCP")
AVAILABLE_TOOLS = ("student_count", "students_by_subject", "project_files", "ci_report")


@mcp.tool()
def student_count() -> dict:
    """Count the students in the enrolment database."""
    return get_student_count()


@mcp.tool()
def students_by_subject(subject_code: str) -> list:
    """List students enrolled in one subject code."""
    return get_students_by_subject(subject_code)


@mcp.tool()
def project_files(directory_path: str = ".") -> list:
    """List project file and folder names within the project root."""
    return list_project_files(directory_path)


@mcp.tool()
def ci_report(report_path: str = "reports/report.json") -> dict:
    """Read the Lab 5 CI report JSON."""
    return read_ci_report(report_path)


if __name__ == "__main__":
    print("Starting Student Enrolment MCP Server", flush=True)
    print("Available tools: " + ", ".join(AVAILABLE_TOOLS), flush=True)
    security = TransportSecuritySettings(
        allowed_hosts=["localhost:*", "127.0.0.1:*", "mcp-server:*"],
        allowed_origins=[],
    )
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        stateless_http=True,
        json_response=True,
        transport_security=security,
    )
