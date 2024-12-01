import json
import re

def parse_agent_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = re.split(r'^# (.+)$', content, flags=re.MULTILINE)
    agent_data = {}
    for i in range(1, len(sections), 2):
        header = sections[i].strip()
        body = sections[i + 1].strip()
        agent_data[header] = parse_subsections(body)
    return agent_data

def parse_subsections(text):
    subsections = re.split(r'^## (.+)$', text, flags=re.MULTILINE)
    data = {}
    for i in range(1, len(subsections), 2):
        header = subsections[i].strip()
        body = subsections[i + 1].strip()
        if header in ['Subtasks', 'Examples', 'Files Uploaded', 'Tools', 'Content']:
            items = re.findall(r'- (.+)', body)
            data[header] = items
        else:
            data[header] = body
    return data

def parse_workflow_markdown(file_path):
    import os
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Parsing workflow markdown content:\n", content)  # Debugging

    # Split the content by top-level sections using regex for markdown headers
    sections = re.split(r'^## (.+)$', content, flags=re.MULTILINE)
    workflow_data = {}
    for i in range(1, len(sections), 2):
        header = sections[i].strip()
        body = sections[i + 1].strip()
        print(f"Parsing section: {header}")  # Debugging

        if header == "Agents":
            agents = []
            agent_entries = re.findall(r'- \*\*(.+)\*\*\n\s*- Config Path: (.+)', body)
            print(f"Found agents: {agent_entries}")  # Debugging
            for name, path in agent_entries:
                agents.append({'agent_name': name.strip(), 'config_path': path.strip()})
            workflow_data['agents'] = agents

        elif header == "Execution Flow":
            execution_flow = []
            steps = re.findall(r'### (.+?)\n(.+?)(?=\n### |\Z)', body, flags=re.DOTALL)
            for step_name, step_body in steps:
                step_data = {'step_name': step_name.strip()}
                agent_match = re.search(r'- Agent: (.+)', step_body)
                if agent_match:
                    step_data['agent'] = agent_match.group(1).strip()
                inputs_match = re.search(r'- Inputs:\n(.+?)(?=\n- |\Z)', step_body, flags=re.DOTALL)
                if inputs_match:
                    inputs = re.findall(r'  - (.+)', inputs_match.group(1))
                    step_data['inputs'] = inputs
                outputs_match = re.search(r'- Outputs:\n(.+?)(?=\n- |\Z)', step_body, flags=re.DOTALL)
                if outputs_match:
                    outputs = re.findall(r'  - (.+)', outputs_match.group(1))
                    step_data['outputs'] = outputs
                execution_flow.append(step_data)
            workflow_data['execution_flow'] = execution_flow

        elif header == "Workflow Name":
            workflow_data['workflow_name'] = body.strip()

        else:
            workflow_data[header.lower()] = body.strip()

    print("Parsed workflow data:", workflow_data)  # Debugging
    return workflow_data

def agent_config_to_markdown(agent_config):
    md = f"# Agent Name\n\n{agent_config['Agent Name']}\n\n---\n\n"
    md += f"## Model\n\n{agent_config['Model']}\n\n---\n\n"
    md += f"## System Prompt\n\n{agent_config['System Prompt']}\n\n---\n\n"
    md += "## Task\n\n"
    md += "### Task Description\n\n"
    md += f"{agent_config['Task']['Task Description']}\n\n"
    md += "### Subtasks\n\n"
    for subtask in agent_config['Task'].get('Subtasks', []):
        md += f"- {subtask}\n"
    md += "\n---\n\n"
    md += "## Tools\n\n"
    for tool in agent_config.get('Tools', []):
        md += f"- {tool}\n"
    md += "\n---\n\n"
    md += "## Output\n\n"
    md += "### Format\n\n"
    md += f"{agent_config['Output']['Format']}\n\n"
    return md

def workflow_config_to_markdown(workflow_config):
    md = f"# Workflow Name\n\n{workflow_config['workflow_name']}\n\n---\n\n"
    md += "## Agents\n\n"
    for agent in workflow_config['agents']:
        md += f"- **{agent['agent_name']}**\n"
        md += f"  - Config Path: {agent['config_path']}\n"
    md += "\n---\n\n"
    md += "## Execution Flow\n\n"
    for step in workflow_config['execution_flow']:
        md += f"### {step['step_name']}\n\n"
        md += f"- Agent: {step['agent']}\n"
        md += "- Inputs:\n"
        for inp in step['inputs']:
            md += f"  - {inp}\n"
        md += "- Outputs:\n"
        for outp in step['outputs']:
            md += f"  - {outp}\n"
        md += "\n"
    return md

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON file {file_path}: {e}")
