# Lab 7 MCP Integration Report

The fourth Compose service runs the MCP 2.x Streamable HTTP server at `http://localhost:8000/mcp` on the host and `http://mcp-server:8000/mcp` inside Compose. Flask's `/mcp/*` routes are MCP clients, and the MCP web tab calls those routes. The agentic loop's Mode 5 independently lists and invokes the four tools through MCP, then passes actual results to the implementation and review models. Mode 6 includes the MCP review.

Observed tool results: `student_count` = 10; `students_by_subject(ASD101)` = John Smith and Sarah Jones; `project_files(.)` returned 25 visible project entries; `ci_report` read Lab 5 workflow run `35310145492` on `main`. The report contains metadata; that GitHub Actions run passed all three jobs, including the new MCP smoke check, but the tool does not infer release readiness.

Validation: four Compose containers started; the MCP tab displayed all four results in Chrome; the MCP route returned HTTP 200 for the four valid calls and HTTP 403 with MCP Mode off; 12 Python tests passed. The remaining operational limit is that this lab server has no authentication or audit log for remote deployment, so its HTTP host binding stays local.
