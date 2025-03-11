import json
import pytest
import ukb.cli
import ukb.surface


@pytest.mark.parametrize("case", ["ED", "ES", "both"])
def test_generate_surfaces_mean_healthy(case, tmp_path):
    ukb.cli.main([str(tmp_path), "--subdir", ".", "--case", case])
    assert (tmp_path / "UKBRVLV.h5").exists()
    assert (tmp_path / "parameters.json").exists()

    if case == "both":
        cases = ["ED", "ES"]
        non_cases = []
    else:
        cases = [case]
        non_cases = ["ED", "ES"]
        non_cases.remove(case)

    for name in ukb.surface.surfaces:
        for case_ in cases:
            path = tmp_path / f"{name}_{case_}.stl"
            assert path.exists()
        for case_ in non_cases:
            path = tmp_path / f"{name}_{case_}.stl"
            assert not path.exists()


def test_generate_surfaces_non_mean_healthy(tmp_path):
    mode = 1
    std = 0.3
    ukb.cli.main([str(tmp_path), "--mode", str(mode), "--std", str(std), "--subdir", "."])
    assert (tmp_path / "UKBRVLV.h5").exists()
    assert (tmp_path / "parameters.json").exists()
    params = json.loads((tmp_path / "parameters.json").read_text())
    assert params["mode"] == mode
    assert params["std"] == std

    for name in ukb.surface.surfaces:
        for case in ["ED", "ES"]:
            path = tmp_path / f"{name}_{case}.stl"
            assert path.exists()


@pytest.mark.xfail(reason="I think we have the wrong template")
def test_generate_surfaces_mean_all(tmp_path):
    ukb.cli.main([str(tmp_path), "--all", "--subdir", "."])
    assert (tmp_path / "UKBRVLV_ALL.h5").exists()
    assert (tmp_path / "parameters.json").exists()
    for name in ukb.surface.surfaces:
        for case in ["ED", "ES"]:
            path = tmp_path / f"{name}_{case}.stl"
            assert path.exists()
