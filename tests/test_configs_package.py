def test_configs_package_contains_default():
    from importlib import resources

    # confirm that the configs package exposes default.yaml
    cfg_files = resources.files("configs")
    assert cfg_files.joinpath("default.yaml").is_file()
