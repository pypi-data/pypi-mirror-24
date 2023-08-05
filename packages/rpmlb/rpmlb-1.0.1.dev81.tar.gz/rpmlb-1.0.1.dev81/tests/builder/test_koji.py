"""Tests for the KojiBuilder"""

from itertools import zip_longest
from logging import DEBUG
from pathlib import Path
from textwrap import dedent

import pytest

from rpmlb.builder.koji import KojiBuilder
from rpmlb.logging import configure_logging
from rpmlb.recipe import Recipe
from rpmlb.work import Work


@pytest.fixture
def minimal_spec_contents():
    """Text contents of a minimal SPEC file."""

    return dedent('''\
        Name:       test
        Version:    1.0
        Release:    1%{?dist}
        Summary:    Minimal spec for testing purposes

        Group:      Development/Testing
        License:    MIT
        URL:        http://test.example.com

        %description
        A minimal SPEC file for testing of RPM packaging.

        %prep

        %build

        %install

        %files

        %changelog
        * Thu Jun 22 2017 Jan Stanek <jstanek@redhat.com> 1.0-1
        - Initial package
    ''')


@pytest.fixture
def minimal_spec_path(tmpdir, minimal_spec_contents):
    """Provide a minimal SPEC file in temporary directory."""

    with tmpdir.as_cwd():
        path = Path('test.spec')

        with path.open(mode='w', encoding='utf-8') as spec_file:
            spec_file.write(minimal_spec_contents)

        yield path


@pytest.fixture
def work(valid_recipe_path):
    """Provide Work instance."""

    valid_recipe = Recipe(str(valid_recipe_path), 'rh-ror50')
    return Work(valid_recipe)


@pytest.fixture
def builder(work):
    """Provide minimal KojiBuilder instance."""

    return KojiBuilder(work, koji_epel=7)


@pytest.fixture(params=[
    KojiBuilder.DEFAULT_TARGET_FORMAT,
    'test-target',
    'fedora-{collection}-epel{epel}',
])
def target_format(request):
    """Koji target format"""

    return request.param


@pytest.fixture(params=list(range(6, 8)))
def epel(request):
    """EPEL version number"""

    return request.param


@pytest.fixture(params=[None, 'koji', 'cbs'])
def profile(request):
    """Koji profile name"""

    return request.param


@pytest.fixture(params=[True, False])
def scratch_build(request):
    """Scratch build indicator"""

    return request.param


@pytest.fixture
def cli_parameters(target_format, epel, profile, scratch_build):
    """Builder parameters as coming from the CLI"""

    return {
        'koji_epel': epel,
        'koji_profile': profile,
        'koji_target_format': target_format,
        'koji_scratch': scratch_build,
    }


def test_init_sets_attributes(work, cli_parameters):
    """Ensure that the parameters are set to appropriate values."""

    builder = KojiBuilder(work, **cli_parameters)

    assert builder.collection == work._recipe._collection_id
    assert builder.epel == cli_parameters['koji_epel']
    assert builder.profile == cli_parameters['koji_profile']
    assert builder.target_format == cli_parameters['koji_target_format']
    assert builder.scratch_build == cli_parameters['koji_scratch']


@pytest.mark.parametrize('required', ['koji_epel'])
def test_init_checks_parameters(required, work, cli_parameters):
    """Ensure that required parameters are checked by __init__."""

    del cli_parameters[required]

    with pytest.raises(ValueError):
        KojiBuilder(work, **cli_parameters)


@pytest.mark.parametrize('profile,expected_command', [
    (None, ['koji']),
    ('koji', ['koji', '--profile', 'koji']),
    ('cbs', ['koji', '--profile', 'cbs']),
])
def test_base_command_respect_profile(builder, profile, expected_command):
    """Ensure that the base_command attribute respects profile attribute."""

    builder.profile = profile
    assert builder.base_command == expected_command


@pytest.mark.parametrize('collection', ['test', 'rh-ror50'])
def test_target_respects_format(
    builder, target_format, collection, epel
):
    """Ensure that the target is properly constructed from parameters."""

    builder.target_format = target_format
    builder.collection = collection
    builder.epel = epel

    expected_target = target_format.format(collection=collection, epel=epel)
    assert builder.target == expected_target


def test_make_srpm_creates_srpm(minimal_spec_path, epel):
    """Ensure that make_srpm works as expected"""

    configure_logging(DEBUG)

    name = minimal_spec_path.stem
    expected_name = '{name}-1.0-1.el{epel}.src.rpm'.format(
        name=name,
        epel=epel,
    )

    srpm_path = KojiBuilder._make_srpm(name, epel)

    assert srpm_path.exists(), srpm_path
    assert srpm_path.name == expected_name


def test_missing_spec_is_reported(tmpdir):
    """make_srpm does not attempt to build nonexistent SPEC file"""

    configure_logging(DEBUG)

    with tmpdir.as_cwd(), pytest.raises(FileNotFoundError):
        KojiBuilder._make_srpm('test', epel=7)


def test_prepare_adjusts_bootstrap_release(builder, minimal_spec_contents):
    """Release is adjusted on bootstrap build."""

    lines = minimal_spec_contents.splitlines(keepends=True)
    lines = builder.prepare_extra_steps(lines, {
        'name': 'test',
        'bootstrap_position': 1,
    })

    release_line, = filter(lambda l: l.startswith('Release:'), lines)

    assert '.bs01%{?dist}' in release_line


@pytest.mark.parametrize('scratch,expected_commands', [
    (True, ['koji build']),
    (False, ['koji build', 'koji wait-repo'])
])
def test_build_emit_correct_commands(
    monkeypatch, builder, scratch, expected_commands
):
    """Builder emits expected commands on build."""

    # Gather all emitted commands
    commands = []
    monkeypatch.setattr(
        'rpmlb.builder.koji.run_cmd',
        lambda cmd, **__: commands.append(cmd),
    )

    # Skip make_srpm, as it requires the run_cmd to actually do something
    monkeypatch.setattr(
        KojiBuilder, '_make_srpm',
        lambda *_, **__: Path('test.src.rpm'),
    )

    builder.scratch_build = scratch
    builder.build({'name': 'test'})

    command_pairs = zip_longest(commands, expected_commands)
    assert all(cmd.startswith(exp) for cmd, exp in command_pairs), commands
