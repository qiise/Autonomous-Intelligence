
---

## 5. `api-overview/tools.md`

```markdown
# Tools

**Tools** give Agents extended capabilities, such as searching the web, scraping websites, or retrieving financial data. They act as plugins or external functions the Agent can call.

## 1. Examples

### 1.1 SerperDevTool (Search)
```python
from anote_agents.tools import SerperDevTool

search_tool = SerperDevTool()
Provides web search functionality
Typically requires an API key or developer token
1.2 ScrapeWebsiteTool
python
Copy code
from anote_agents.tools import ScrapeWebsiteTool

scrape_tool = ScrapeWebsiteTool()
Allows Agents to fetch and parse HTML from websites
2. Assigning Tools to Agents
python
Copy code
venue_coordinator.tools = [search_tool, scrape_tool]
```
3. Building Custom Tools
You can implement custom Tools (e.g., database queries, Slack bot actions) by extending a base Tool class and overriding a run() method. This approach unifies external integrations under a single interface.