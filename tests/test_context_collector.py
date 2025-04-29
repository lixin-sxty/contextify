import os
from contextify.context_collector import collect_project_context


def test_collect_context():
    context, errors, excludes = collect_project_context(".")
    assert isinstance(context, dict)
    assert "files" in context
    assert "total_files" in context
    assert isinstance(errors, list)
