# cli/add_panacea_to_flow.py

from pathlib import Path
import click

from panacea_ai_framework.cli.utils import copy_template

def add_panacea_to_flow(panacea_name: str) -> None:
    """Add a new panacea to the current flow."""
    # Check if pyproject.toml exists in the current directory
    if not Path("pyproject.toml").exists():
        print("This command must be run from the root of a flow project.")
        raise click.ClickException(
            "This command must be run from the root of a flow project."
        )

    # Determine the flow folder based on the current directory
    flow_folder = Path.cwd()
    panaceas_folder = flow_folder / "src" / flow_folder.name / "panaceas"

    if not panaceas_folder.exists():
        print("Panaceas folder does not exist in the current flow.")
        raise click.ClickException("Panaceas folder does not exist in the current flow.")

    # Create the panacea within the flow's panaceas directory
    create_embedded_panacea(panacea_name, parent_folder=panaceas_folder)

    click.echo(
        f"Panacea {panacea_name} added to the current flow successfully!",
    )

def create_embedded_panacea(panacea_name: str, parent_folder: Path) -> None:
    """Create a new panacea within an existing flow project."""
    folder_name = panacea_name.replace(" ", "_").replace("-", "_").lower()
    class_name = panacea_name.replace("_", " ").replace("-", " ").title().replace(" ", "")

    panacea_folder = parent_folder / folder_name

    if panacea_folder.exists():
        if not click.confirm(
            f"Panacea {folder_name} already exists. Do you want to override it?"
        ):
            click.secho("Operation cancelled.", fg="yellow")
            return
        click.secho(f"Overriding panacea {folder_name}...", fg="green", bold=True)
    else:
        click.secho(f"Creating panacea {folder_name}...", fg="green", bold=True)
        panacea_folder.mkdir(parents=True)

    # Create config and panacea.py files
    config_folder = panacea_folder / "config"
    config_folder.mkdir(exist_ok=True)

    templates_dir = Path(__file__).parent / "templates" / "panacea"
    config_template_files = ["agents.yaml", "tasks.yaml"]
    panacea_template_file = f"{folder_name}.py"  # Updated file name

    for file_name in config_template_files:
        src_file = templates_dir / "config" / file_name
        dst_file = config_folder / file_name
        copy_template(src_file, dst_file, panacea_name, class_name, folder_name)

    src_file = templates_dir / "panacea.py"
    dst_file = panacea_folder / panacea_template_file
    copy_template(src_file, dst_file, panacea_name, class_name, folder_name)

    click.secho(
        f"Panacea {panacea_name} added to the flow successfully!", fg="green", bold=True
    )
