"""Graph export tests for visual logic flow (LFL-11)."""

from pathlib import Path

import pytest

from logiclock.core import (
    export_dot,
    export_mermaid,
    graphviz_is_available,
    parse_module_logic,
    render_dot_with_graphviz,
)

_FIXTURE_MODULE = Path(__file__).resolve().parent / "fixtures" / "sample_module.py"
_SNAP_MERMAID = (
    Path(__file__).resolve().parent / "snapshots" / "graph_fixture_module.mmd"
)
_SNAP_DOT = Path(__file__).resolve().parent / "snapshots" / "graph_fixture_module.dot"


def test_mermaid_export_matches_snapshot() -> None:
    parsed = parse_module_logic(_FIXTURE_MODULE, decorated_only=False)
    expected = _SNAP_MERMAID.read_text(encoding="utf-8")
    assert export_mermaid(parsed) == expected


def test_mermaid_output_has_renderable_shape() -> None:
    parsed = parse_module_logic(_FIXTURE_MODULE, decorated_only=False)
    text = export_mermaid(parsed)
    assert text.startswith("flowchart TD")
    assert '{"' in text
    assert "-->" in text


def test_dot_export_matches_snapshot() -> None:
    parsed = parse_module_logic(_FIXTURE_MODULE, decorated_only=False)
    expected = _SNAP_DOT.read_text(encoding="utf-8")
    assert export_dot(parsed) == expected


def test_function_filter_only_exports_one_function() -> None:
    parsed = parse_module_logic(_FIXTURE_MODULE, decorated_only=False)
    out = export_mermaid(parsed, function_name="plain_check")
    assert "plain_check()" in out
    assert "apply_discount()" not in out


def test_graphviz_render_is_optional_when_installed(tmp_path: Path) -> None:
    if not graphviz_is_available():
        pytest.skip("Graphviz not installed in this environment")
    parsed = parse_module_logic(_FIXTURE_MODULE, decorated_only=False)
    dot_text = export_dot(parsed)
    out = tmp_path / "graph.svg"
    render_dot_with_graphviz(dot_text, output_path=out, output_format="svg")
    assert out.exists()
