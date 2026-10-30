import sys

from shopflow.__main__ import main


def test_cli_runs_pipeline(monkeypatch, capsys):
    pipeline_result = {
        "loaded": {
            "customers": 9,
            "products": 10,
            "orders": 8,
            "order_items": 15
        },
        "rejected": {
            "customers": 1,
            "products": 0,
            "orders": 2,
            "order_items": 0
        },
        "errors": []
    }

    def fake_run_pipeline(data_directory, database_path):
        assert data_directory == "data/raw"
        assert database_path == "data/shopflow.db"
        return pipeline_result

    monkeypatch.setattr(
        "shopflow.__main__.run_pipeline",
        fake_run_pipeline
    )

    monkeypatch.setattr(
        sys,
        "argv",
        ["shopflow"]
    )

    assert main() == 0

    output = capsys.readouterr().out

    assert "pipeline completed successfully" in output
    assert "customers: 90.0%" in output
    assert "products: 100.0%" in output
    assert "Validation errors: 0" in output