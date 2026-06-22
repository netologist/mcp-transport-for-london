from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import (Evaluator,
                                       EvaluatorContext)
from pydantic_evals.otel.span_tree import SpanQuery

from agent import create_agent
from otel import enable_tracing

@dataclass
class AgentCalledTool(Evaluator[object, object, object]):
    agent_name: str
    tool_name: str

    def evaluate(self, ctx: EvaluatorContext[object, object, object]) -> bool:
        # Returns True if the given agent ran the given tool at least once
        return ctx.span_tree.any(
            SpanQuery(
                name_equals="agent run",
                has_attributes={"agent_name": self.agent_name},
                stop_recursing_when=SpanQuery(name_equals="agent run"),
                some_descendant_has=SpanQuery(
                    name_equals="running tool",
                    has_attributes={"gen_ai.tool.name": self.tool_name},
                ),
            )
        )


tfl_dataset = Dataset[str, str, Any](
    cases=[
        Case(
            name="Find stops by location name",
            inputs="Find bus stops near Piccadilly Circus",
            expected_output=None,
            evaluators=(
                AgentCalledTool(agent_name="tfl_agent", tool_name="search_bus_stops"),
            ),
        ),
        Case(
            name="Get route details",
            inputs="Tell me about bus route 190",
            expected_output=None,
            evaluators=(
                AgentCalledTool(agent_name="tfl_agent", tool_name="get_route_info"),
            ),
        ),
    ],
    evaluators=[],
)

def main(text: str) -> str:
    agent = create_agent()
    result = agent.run_sync(text)
    return result.output

if __name__ == "__main__":
    enable_tracing()
    report = tfl_dataset.evaluate_sync(main)
    report.print()
