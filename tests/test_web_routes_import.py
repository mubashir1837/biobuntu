def test_web_routes_package_import():
    """Ensure `web.routes` is recognized as a package (no heavy imports)."""
    import importlib

    pkg = importlib.import_module("web.routes")
    assert pkg is not None
