import pathlib
from contextlib import nullcontext as does_not_raise

import pytest

from ... import SimulatedE4CV
from ...__init__ import __version__
from ...tests.models import E4CV_CONFIG_FILE
from ...tests.models import add_oriented_vibranium_to_e4cv
from ...tests.models import e4cv_config
from ..configure import Configuration
from ..misc import ConfigurationError
from ..misc import load_yaml_file

e4cv = SimulatedE4CV(name="e4cv")
add_oriented_vibranium_to_e4cv(e4cv)


@pytest.mark.parametrize(
    "keypath, value",
    [
        ["_header.datetime", None],
        ["_header.energy_units", e4cv._wavelength.energy_units],
        ["_header.energy", e4cv._wavelength.energy],
        ["_header.hklpy2_version", __version__],
        ["_header.python_class", e4cv.__class__.__name__],
        ["_header.source_type", e4cv._wavelength.source_type],
        ["_header.wavelength_units", e4cv._wavelength.wavelength_units],
        ["_header.wavelength", e4cv._wavelength.wavelength],
        ["axes.axes_xref", e4cv.operator.axes_xref],
        ["axes.extra_axes", e4cv.operator.solver.extras],
        ["axes.pseudo_axes", e4cv.pseudo_axis_names],
        ["axes.real_axes", e4cv.real_axis_names],
        ["constraints.chi.high_limit", 180.2],
        ["constraints.omega.label", "omega"],
        ["constraints.tth.low_limit", -180.2],
        ["name", e4cv.name],
        ["sample_name", e4cv.operator.sample.name],
        ["samples.sample.lattice.a", 1],
        ["samples.sample.lattice.alpha", 90],
        ["samples.sample.name", "sample"],
        ["samples.sample.reflections_order", []],
        ["samples.sample.reflections", {}],
        ["samples.sample.U", [[1, 0, 0], [0, 1, 0], [0, 0, 1]]],
        ["samples.sample.UB", [[1, 0, 0], [0, 1, 0], [0, 0, 1]]],
        ["samples.vibranium.name", "vibranium"],
        ["samples.vibranium.reflections_order", "r040 r004".split()],
        ["samples.vibranium.reflections_order", "r040 r004".split()],
        ["samples.vibranium.reflections.r004.name", "r004"],
        ["samples.vibranium.reflections.r004.pseudos.h", 0],
        ["samples.vibranium.reflections.r004.pseudos.k", 0],
        ["samples.vibranium.reflections.r004.pseudos.l", 4],
        ["samples.vibranium.reflections.r004.reals.chi", 90],
        ["samples.vibranium.U", e4cv.operator.solver.U],
        ["samples.vibranium.UB", e4cv.operator.solver.UB],
        ["solver.engine", e4cv.operator.solver.engine_name],
        ["solver.geometry", e4cv.operator.solver.geometry],
        ["solver.mode", e4cv.operator.solver.mode],
        ["solver.name", e4cv.operator.solver.name],
        ["solver.real_axes", e4cv.operator.solver.real_axis_names],
    ],
)
def test_Configuration(keypath, value):
    agent = Configuration(e4cv)._asdict()
    assert "_header" in agent, f"{agent=!r}"
    assert "file" not in agent["_header"], f"{agent=!r}"

    for k in keypath.split("."):
        agent = agent.get(k)  # narrow the search
        assert agent is not None, f"{k=!r}  {keypath=!r}"

    if value is not None:
        assert value == agent, f"{k=!r}  {value=!r}  {agent=!r}"


def test_Configuration_export(tmp_path):
    assert isinstance(tmp_path, pathlib.Path)
    assert tmp_path.exists()

    config_file = tmp_path / "config.yml"
    assert not config_file.exists()

    # write the YAML file
    agent = Configuration(e4cv)
    agent.export(config_file, comment="testing")
    assert config_file.exists()

    # read the YAML file, check for _header.file key
    config = load_yaml_file(config_file)
    assert "_header" in config, f"{config=!r}"
    assert "file" in config["_header"], f"{config=!r}"
    assert "comment" in config["_header"], f"{config=!r}"
    assert config["_header"]["comment"] == "testing"


def test_fromdict(sim, fourc):
    config = e4cv_config()
    assert config.get("name") == "e4cv"

    with pytest.raises(ConfigurationError) as reason:
        sim.operator.configuration._fromdict(config)
    assert "solver mismatch" in str(reason)

    assert fourc.name != config["name"]
    assert len(fourc.operator.samples) == 2
    assert len(fourc.operator.constraints) == 4

    fourc.operator.reset_constraints()
    fourc.operator.reset_samples()
    assert len(fourc.operator.samples) == 1
    assert len(fourc.operator.constraints) == 4
    assert len(fourc.operator.sample.reflections) == 0

    for key, constraint in fourc.operator.constraints.items():
        assert key in config["constraints"]
        cfg = config["constraints"][key]
        assert cfg["class"] == constraint.__class__.__name__
        for field in constraint._fields:
            assert field in cfg, f"{key=!r}  {field=!r}  {constraint=!r}  {cfg=!r}"
            if field == "label":
                assert cfg[field] == getattr(constraint, field)
            else:
                assert cfg[field] != getattr(
                    constraint, field
                ), f"{key=!r}  {field=!r}  {constraint=!r}  {cfg=!r}"
    # A few pre-checks
    assert "geometry" not in config
    assert "solver" in config
    assert "geometry" in config["solver"]

    ###
    ### apply the configuration
    ###
    fourc.operator.configuration._fromdict(config), f"{fourc=!r}"

    sample = config["sample_name"]
    assert (
        sample == fourc.operator.sample.name
    ), f"{sample=!r}  {fourc.operator.sample.name=!r}"
    assert len(fourc.operator.samples) == len(
        config["samples"]
    ), f"{config['samples']=!r}"
    assert (
        fourc.operator.sample.reflections.order
        == config["samples"][sample]["reflections_order"]
    )

    assert len(fourc.operator.sample.reflections) == 3
    for refl in fourc.operator.sample.reflections.order:
        assert refl in fourc.operator.sample.reflections
    # TODO: compare reflections

    assert len(fourc.operator.constraints) == len(config["constraints"])
    for key, constraint in fourc.operator.constraints.items():
        assert key in config["constraints"]
        cfg = config["constraints"][key]
        assert cfg["class"] == constraint.__class__.__name__
        for field in constraint._fields:
            assert field in cfg, f"{key=!r}  {field=!r}  {constraint=!r}  {cfg=!r}"
            assert cfg[field] == getattr(
                constraint, field
            ), f"{key=!r}  {field=!r}  {constraint=!r}  {cfg=!r}"


def test_restore(sim, fourc):
    with pytest.raises(ConfigurationError) as reason:
        sim.operator.configuration.restore(E4CV_CONFIG_FILE)
    assert "solver mismatch" in str(reason)

    with does_not_raise():
        fourc.operator.configuration.restore(E4CV_CONFIG_FILE)

    with does_not_raise():
        fourc.operator.configuration.restore(
            E4CV_CONFIG_FILE,
            clear=True,
            restore_constraints=False,
        )
