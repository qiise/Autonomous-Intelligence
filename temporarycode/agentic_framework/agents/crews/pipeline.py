# crews/pipeline.py

from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from panacea_ai_framework.crews.panacea import Crew
from panacea_ai_framework.agents.crews.research_panacea import ResearchPanacea
from panacea_ai_framework.agents.crews.poem_panacea import PoemPanacea

class Pipeline(BaseModel):
    """Orchestrates the execution of multiple panaceas."""

    stages: List[Crew]

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initiates the execution of all stages in the pipeline."""
        results = {}
        for stage in self.stages:
            stage_result = stage.kickoff(inputs=inputs)
            results[stage.id] = stage_result
        return results

class ExamplePipeline(BaseModel):
    """Example Pipeline integrating Research and Poem Panaceas."""

    def __init__(self):
        super().__init__()
        self.research_panacea = ResearchPanacea().panacea()
        self.poem_panacea = PoemPanacea().panacea()

    def create_pipeline(self) -> Pipeline:
        return Pipeline(
            stages=[
                self.research_panacea,
                self.poem_panacea
            ]
        )

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pipeline = self.create_pipeline()
        results = pipeline.kickoff(inputs)
        return results
