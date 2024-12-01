# Workflow Name

Sample_Workflow

---

## Agents

- **Researcher**
  - Config Path: examples/agents/researcher.md
- **Writer**
  - Config Path: examples/agents/writer.md

---

## Execution Flow

### Step 1: Researching

- Agent: Researcher
- Inputs:
  - user_input
- Outputs:
  - Researcher_Output

### Step 2: Writing

- Agent: Writer
- Inputs:
  - Researcher_Output
  - user_input
- Outputs:
  - Final_Output
