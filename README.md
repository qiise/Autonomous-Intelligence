# Panacea

agentic_ai_framework/
├── README.md
├── main.py
├── config/
│   ├── config.yaml
│   └── rbac.yaml
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── registry.py
│   ├── search_agent.py
│   ├── analysis_agent.py
│   └── communication_agent.py
├── orchestrator/
│   ├── __init__.py
│   └── orchestrator.py
├── lm/
│   ├── __init__.py
│   └── llm_service.py
├── tools/
│   ├── __init__.py
│   └── search_api.py
├── utils/
│   ├── __init__.py
│   ├── response_synthesizer.py
│   ├── logger.py
│   ├── cache_manager.py
│   ├── workflow_engine.py
│   └── rbac_manager.py
├── memory/
│   ├── __init__.py
│   └── memory_manager.py
├── api/
│   ├── __init__.py
│   └── api_server.py
├── workflows/
│   └── example_workflow.yaml
├── docs/
│   └── setup_guide.md
├── tests/
│   ├── __init__.py
│   └── test_framework.py
└── requirements.txt
