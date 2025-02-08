from __future__ import annotations

import json
from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING
from urllib import error, request

from tach.constants import GAUGE_API_BASE_URL
from tach.extension import serialize_modules_json

if TYPE_CHECKING:
    from pathlib import Path

    import pydot  # type: ignore

    from tach.extension import ProjectConfig


def generate_show_url(
    project_config: ProjectConfig,
    included_paths: list[Path] | None = None,
) -> str | None:
    included_paths = included_paths or []
    modules = project_config.filtered_modules(included_paths)
    for module in modules:
        if module.depends_on is None:
            # This is a hack to avoid bumping the API version
            module.depends_on = []
    json_data = serialize_modules_json(modules)
    json_bytes = json_data.encode("utf-8")
    req = request.Request(
        f"{GAUGE_API_BASE_URL}/api/show/graph/1.3",
        data=json_bytes,
        headers={"Content-Type": "application/json"},
    )

    try:
        # Send the request and read the response
        with request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)
            uid = response_json.get("uid")
            return f"{GAUGE_API_BASE_URL}/show?uid={uid}"
    except (UnicodeDecodeError, JSONDecodeError, error.URLError) as e:
        print(f"Error: {e}")
        return None


def generate_module_graph_dot_file(
    project_config: ProjectConfig,
    output_filepath: Path,
    included_paths: list[Path],
) -> None:
    # Local import because networkx takes about ~100ms to load
    import networkx as nx

    graph = nx.DiGraph()  # type: ignore

    def upsert_edge(graph: nx.DiGraph, module: str, dependency: str) -> None:  # type: ignore
        if module not in graph:
            graph.add_node(module)  # type: ignore
        if dependency not in graph:
            graph.add_node(dependency)  # type: ignore
        graph.add_edge(module, dependency)  # type: ignore

    modules = project_config.filtered_modules(included_paths)

    for module in modules:
        for dependency in module.depends_on or []:
            upsert_edge(graph, module.path, dependency.path)  # type: ignore

    pydot_graph: pydot.Dot = nx.nx_pydot.to_pydot(graph)  # type: ignore
    dot_data: str = pydot_graph.to_string()  # type: ignore

    output_filepath.write_text(dot_data)  # type: ignore


def generate_module_graph_mermaid(
    project_config: ProjectConfig,
    output_filepath: Path,
    included_paths: list[Path],
) -> None:
    modules = project_config.filtered_modules(included_paths)
    edges: list[str] = []
    isolated: list[str] = []
    for module in modules:
        for dependency in module.depends_on or []:
            edges.append(
                f"    {module.path.strip('<>')} --> {dependency.path.strip('<>')}"
            )
        if not module.depends_on:
            isolated.append(f"    {module.path.strip('<>')}")

    mermaid_graph = "graph TD\n" + "\n".join(edges) + "\n" + "\n".join(isolated)

    output_filepath.write_text(mermaid_graph)


__all__ = [
    "generate_show_url",
    "generate_module_graph_dot_file",
    "generate_module_graph_mermaid",
]
