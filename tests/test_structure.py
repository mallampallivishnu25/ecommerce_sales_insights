from pathlib import Path

def test_repo_structure():
    assert Path("src/ingest/ingest_olist.py").exists()
    assert Path("src/transform/sql").exists()
    assert Path("app/streamlit_app.py").exists()

def test_requirements_present():
    assert Path("requirements.txt").read_text().strip() != ""
