"""CLI tests for `logiclock graph` command."""

from pathlib import Path

from typer.testing import CliRunner

from logiclock.cli import app

_FIXTURE_MODULE = Path(__file__).resolve().parent / "fixtures" / "sample_module.py"
_SNAP_MERMAID = (
    Path(__file__).resolve().parent / "snapshots" / "graph_fixture_module.mmd"
)


def test_graph_command_mermaid_matches_snapshot() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["graph", str(_FIXTURE_MODULE)])
    assert result.exit_code == 0, result.output
    expected = _SNAP_MERMAID.read_text(encoding="utf-8").rstrip("\n")
    assert result.stdout.rstrip("\n") == expected


def test_graph_command_dot_with_function_filter() -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "graph",
            str(_FIXTURE_MODULE),
            "--format",
            "dot",
            "--function",
            "plain_check",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "digraph LogicFlow" in result.stdout
    assert "plain_check()" in result.stdout
    assert "apply_discount()" not in result.stdout
