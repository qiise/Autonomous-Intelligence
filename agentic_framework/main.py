# # main.py
# import asyncio
# import yaml
# from agents.registry import agent_registry
# from tools.search_api import SearchAPI
# from lm.llm_service import LLMService
# from orchestrator.orchestrator import Orchestrator
# from utils.logger import logger
# from memory.memory_manager import MemoryManager
# from utils.rbac_manager import RBACManager
# from utils.workflow_engine import load_workflow, WorkflowEngine

# def load_config(config_path):
#     with open(config_path, 'r') as file:
#         return yaml.safe_load(file)

# async def main():
#     # Load configuration
#     config = load_config('config/config.yaml')
#     rbac_config = load_config('config/rbac.yaml')

#     # Initialize tools
#     tools = {}
#     for tool_name, tool_class_path in config['tools'].items():
#         module_name, class_name = tool_class_path.rsplit('.', 1)
#         module = __import__(module_name, fromlist=[class_name])
#         tool_class = getattr(module, class_name)
#         tools[tool_name] = tool_class()

#     # Initialize agents with tools
#     for agent_config in config['agents']:
#         agent_name = agent_config['name']
#         agent_class_path = agent_config['class']
#         module_name, class_name = agent_class_path.rsplit('.', 1)
#         module = __import__(module_name, fromlist=[class_name])
#         agent_class = getattr(module, class_name)
#         agent_registry.register_agent(agent_name, agent_class)

#     # Initialize memory manager and RBAC manager
#     memory_manager = MemoryManager()
#     await memory_manager.connect()
#     rbac_manager = RBACManager('config/rbac.yaml')

#     # Initialize orchestrator with tools, memory manager, and RBAC
#     orchestrator = Orchestrator(agent_registry, tools, memory_manager, rbac_manager)

#     # Example queries
#     queries = [
#         {"query": "Get the latest AI news and summarize it", "user_role": "user"},
#         {"query": "Summarize recent AI breakthroughs and reach out to experts", "user_role": "admin"}
#     ]

#     for q in queries:
#         logger.info(f"Processing query: '{q['query']}' with role '{q['user_role']}'")
#         response = await orchestrator.process_query(q['query'], user_role=q['user_role'])
#         logger.info(f"Response: {response}")
#         print(f"Query: {q['query']}\nResponse:\n{response}\n{'-'*50}")

#     # Example of executing a predefined workflow
#     workflow = load_workflow('workflows/example_workflow.yaml')
#     workflow_engine = WorkflowEngine(workflow)
#     await workflow_engine.execute(orchestrator)

#     # Retrieve and print workflow results from memory
#     for step in workflow:
#         step_key = f"step_{step['step']}"
#         result = await memory_manager.retrieve(step_key)
#         print(f"Result for {step_key}: {result}")

#     # Close memory manager connection
#     await memory_manager.close()

# if __name__ == "__main__":
#     asyncio.run(main())
# main.py

import click
import pkg_resources

from panacea_ai_framework.agents.base_agent import Agent
from panacea_ai_framework.agents.crews.research_crew import ResearchCrew
from panacea_ai_framework.agents.crews.poem_crew import PoemCrew
from panacea_ai_framework.orchestrator.orchestrator import Orchestrator

from panacea_ai_framework.cli.add_panacea_to_flow import add_panacea_to_flow
from panacea_ai_framework.cli.create_panacea import create_panacea
from panacea_ai_framework.cli.create_pipeline import create_pipeline
from panacea_ai_framework.cli.create_flow import create_flow
from panacea_ai_framework.cli.constants import ENV_VARS
from panacea_ai_framework.cli.utils import copy_template

from panacea_ai_framework.deploy_commands import DeployCommand
from panacea_ai_framework.tool_commands import ToolCommand
from panacea_ai_framework.training_commands import train_panacea
from panacea_ai_framework.evaluation_commands import evaluate_panacea
from panacea_ai_framework.installation_commands import install_panacea

from rich.console import Console
console = Console()

@click.group()
def panacea():
    """Top-level command group for Panacea."""
    pass

@panacea.command()
@click.argument("type", type=click.Choice(["panacea", "pipeline", "flow"]))
@click.argument("name")
@click.option("--provider", type=str, help="The provider to use for the Panacea")
@click.option("--skip_provider", is_flag=True, help="Skip provider validation")
def create(type, name, provider, skip_provider=False):
    """Create a new panacea, pipeline, or flow."""
    if type == "panacea":
        create_panacea(name, provider, skip_provider)
    elif type == "pipeline":
        create_pipeline(name)
    elif type == "flow":
        create_flow(name)
    else:
        click.secho(
            "Error: Invalid type. Must be 'panacea', 'pipeline', or 'flow'.", fg="red"
        )

@panacea.command()
@click.option("--tools", is_flag=True, help="Show the installed version of panacea tools")
def version(tools):
    """Show the installed version of Panacea."""
    panacea_version = pkg_resources.get_distribution("panacea_ai_framework").version
    click.echo(f"Panacea version: {panacea_version}")

    if tools:
        try:
            tools_version = pkg_resources.get_distribution("panacea_tools").version
            click.echo(f"Panacea tools version: {tools_version}")
        except pkg_resources.DistributionNotFound:
            click.echo("Panacea tools not installed")

@panacea.command()
@click.option(
    "-n",
    "--n_iterations",
    type=int,
    default=5,
    help="Number of iterations to train the panacea",
)
@click.option(
    "-f",
    "--filename",
    type=str,
    default="trained_agents_data.pkl",
    help="Path to a custom file for training",
)
def train(n_iterations: int, filename: str):
    """Train the panacea."""
    click.echo(f"Training the Panacea for {n_iterations} iterations")
    train_panacea(n_iterations, filename)

@panacea.command()
@click.option(
    "-t",
    "--task_id",
    type=str,
    help="Replay the panacea from this task ID, including all subsequent tasks.",
)
def replay(task_id: str) -> None:
    """
    Replay the panacea execution from a specific task.

    Args:
        task_id (str): The ID of the task to replay from.
    """
    try:
        click.echo(f"Replaying the Panacea from task {task_id}")
        # Implement the replay logic or call the appropriate function
    except Exception as e:
        click.echo(f"An error occurred while replaying: {e}", err=True)

# Define other commands similarly...

# DEPLOY PANACEA+ COMMANDS
@panacea.group()
def deploy():
    """Deploy the Panacea CLI group."""
    pass

@deploy.command(name="create")
@click.option("-y", "--yes", is_flag=True, help="Skip the confirmation prompt")
def deploy_create(yes: bool):
    """Create a Panacea deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.create_panacea(yes)

@deploy.command(name="list")
def deploy_list():
    """List all deployments."""
    deploy_cmd = DeployCommand()
    deploy_cmd.list_panaceas()

@deploy.command(name="push")
@click.option("-u", "--uuid", type=str, help="Panacea UUID parameter")
def deploy_push(uuid: str):
    """Deploy the Panacea."""
    deploy_cmd = DeployCommand()
    deploy_cmd.deploy(uuid=uuid)

@deploy.command(name="status")
@click.option("-u", "--uuid", type=str, help="Panacea UUID parameter")
def deploy_status(uuid: str):
    """Get the status of a deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.get_panacea_status(uuid=uuid)

@deploy.command(name="logs")
@click.option("-u", "--uuid", type=str, help="Panacea UUID parameter")
def deploy_logs(uuid: str):
    """Get the logs of a deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.get_panacea_logs(uuid=uuid)

# TOOL COMMANDS
@panacea.group()
def tool():
    """Tool Repository related commands."""
    pass

@tool.command(name="create")
@click.argument("handle")
def tool_create(handle: str):
    tool_cmd = ToolCommand()
    tool_cmd.create(handle)

@tool.command(name="install")
@click.argument("handle")
def tool_install(handle: str):
    tool_cmd = ToolCommand()
    tool_cmd.login()
    tool_cmd.install(handle)

@tool.command(name="publish")
@click.option(
    "--force",
    is_flag=True,
    show_default=True,
    default=False,
    help="Bypasses Git remote validations",
)
@click.option("--public", "is_public", flag_value=True, default=False)
@click.option("--private", "is_public", flag_value=False)
def tool_publish(is_public: bool, force: bool):
    tool_cmd = ToolCommand()
    tool_cmd.login()
    tool_cmd.publish(is_public, force)

# FLOW COMMANDS
@panacea.group()
def flow():
    """Flow related commands."""
    pass

@flow.command(name="kickoff")
def flow_run():
    """Kickoff the Flow."""
    click.echo("Running the Flow")
    # Implement the kickoff_flow function or call it here

@flow.command(name="plot")
def flow_plot():
    """Plot the Flow."""
    click.echo("Plotting the Flow")
    # Implement the plot_flow function or call it here

@flow.command(name="add-panacea")
@click.argument("panacea_name")
def flow_add_panacea(panacea_name):
    """Add a panacea to an existing flow."""
    click.echo(f"Adding panacea {panacea_name} to the flow")
    add_panacea_to_flow(panacea_name)

if __name__ == "__main__":
    panacea()
