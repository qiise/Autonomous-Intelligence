
---

## 6. `api-overview/workflows.md`

```markdown
# Workflows

Workflows dictate how Tasks are executed within a Crew. They define the order, logic, and decision-making structure.

## 1. Common Process Types

1. **Sequential**
   - Tasks run one after another in a predefined order.
   - Good for simple, linear processes.

2. **Hierarchical**
   - Involves a "manager" agent that oversees or delegates Tasks to subordinate agents.
   - Useful when tasks must be dynamically created or delegated.

3. **Consensual** (Planned)
   - Focuses on collaborative decision-making among agents.
   - Agents vote or debate to reach a consensus.

## 2. Implementation in Code
```python
crew = Crew(
    agents=[manager_agent, worker_agent],
    tasks=[task1, task2],
    verbose=True
)

# For hierarchical, specify a manager agent with special logic
crew.workflow_type = "hierarchical"
```

(Note: The actual implementation of these workflow types may vary. Some are planned features, while others might already exist.)

3. Choosing a Workflow
Sequential is easiest to implement but less flexible.
Hierarchical suits large projects with many sub-tasks.
Consensual may improve decision quality but can be more complex to set up.