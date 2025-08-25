def test_importable():
    import importlib
    for mod in ["duckdb", "pandas"]:
        importlib.import_module(mod)
