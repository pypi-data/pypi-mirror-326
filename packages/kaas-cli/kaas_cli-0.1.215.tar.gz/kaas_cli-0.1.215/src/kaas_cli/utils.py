import os
from typing import Any

import click
import tomlkit

from kaas_cli.types import KaasCliException

from .config import DEFAULT_DIRECTORY


def get_foundry_out_dir() -> str:
    kontrol_toml_path, foundry_toml_path = find_kontrol_configs()
    profile = os.environ.get('FOUNDRY_PROFILE')
    click.echo(f"env FOUNDRY_PROFILE={profile}")
    if profile is None:
        profile = 'default'
    click.echo(f"Using Foundry profile: {profile}")
    try:
        with open(foundry_toml_path, 'r') as file:
            parsed_toml: dict[str, Any] = tomlkit.load(file)
        if 'profile' in parsed_toml and isinstance(parsed_toml['profile'], dict):
            profile_config = parsed_toml['profile'].get(profile)
            if isinstance(profile_config, dict) and 'out' in profile_config:
                click.echo(f"Using Foundry out directory: {profile_config['out']}")
                return profile_config['out']
        click.echo("Falling back to default 'out' value")
        return DEFAULT_DIRECTORY
    except Exception as e:
        click.echo(f"Error parsing Foundry profile: {e}")
        raise KaasCliException(f"Error reading foundry.toml: {e}") from e


def find_kontrol_configs() -> tuple[str, str]:
    """
    Check if kontrol.toml and foundry.toml or just 'foundry.toml' exist below the current directory.
    Use chdir to change to the directory containing the kontrol.toml and foundry.toml files
    then if they do exist, return the path, otherwise return None

    Returns:
        str: Path to the directory containing the kontrol.toml and foundry.toml files
    """
    # Check if kontrol.toml and foundry.toml or just 'foundry.toml' exist below the current directory
    kontrol_toml = find_file('kontrol.toml')
    foundry_toml = find_file('foundry.toml')
    kontrol_exists = os.path.exists(kontrol_toml)
    foundry_exists = os.path.exists(foundry_toml)

    if not foundry_exists:
        click.echo("No foundry.toml file found...")
        raise KaasCliException(
            "Missing foundry.toml file or found the wrong one.\n"
            "If there are more than one foundry config in your project please specify the kontrol test root.\n"
            "OR create test configs using 'kontrol init --help' for more information."
        )
    else:
        click.echo("Found foundry.toml file.")
    return kontrol_toml if kontrol_exists else "", foundry_toml if foundry_exists else ""


def find_file(file_name: str) -> str:
    """
    Check if the file exists below the current directory
    if it does, return the path to the file, otherwise return None

    Returns:
        str: Path to the file
    """
    for root, _dirs, files in os.walk("."):
        if file_name in files:
            return os.path.relpath(root) + '/' + file_name
    return ""


def validate_config_location(test_root: str, kontrol_toml: str, foundry_toml: str) -> None:
    if test_root:
        if os.path.exists(os.path.join(test_root, 'foundry.toml')):
            foundry_toml = os.path.join(test_root, 'foundry.toml')
        else:
            raise KaasCliException("No foundry.toml file found in the defined test-root: " + test_root)
    elif not foundry_toml:
        raise KaasCliException("No foundry.toml file found in the current directory or subdirectories.")
    if not kontrol_toml:
        click.echo(
            click.style(
                "Warning: No kontrol.toml file found in the current directory or subdirectories. Refine Kontrol execution using 'kontrol.toml'.",
                fg='yellow',
            )
        )
