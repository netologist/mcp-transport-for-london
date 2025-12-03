from __future__ import annotations

import os
from dataclasses import dataclass
from functools import cached_property
from typing import Annotated, Any

import yaml
from client import agent
from pydantic import Field
from pydantic_ai import Agent, PromptedOutput
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EqualsExpected
from typing_extensions import override
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.otel.span_tree import SpanQuery

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
            evaluators=(AgentCalledTool(agent_name="tfl_agent", tool_name="search_bus_stops"),),
        ),
        # EvalCase(
        #         id="basic_001",
        #         name="Find stops by location name",
        #         user_query="Find bus stops near Piccadilly Circus",
        #         expected_tools=["search_bus_stops"],
        #         success_criteria=[
        #             "Uses search_bus_stops tool",
        #             "Returns stop names and IDs",
        #             "Mentions multiple stops"
        #         ],
        #         category="basic_search"
        #     ),
        
        # Case(
        #     name="clause_commas_and_split",
        #     inputs="when i went to the store it was closed so i came back home",
        #     expected_output="When I went to the store, it was closed so I came back home.",
        #     metadata={"difficulty": "medium"},
        #     evaluators=(EqualsExpected(),),
        # ),
        # Case(
        #     name="multiple_questions",
        #     inputs="you paid the invoice right when is the next one due",
        #     expected_output="You paid the invoice, right? When is the next one due?",
        #     metadata={"difficulty": "easy"},
        #     evaluators=(EqualsExpected(),),
        # ),
        # Case(
        #     name="capitalization_only_plus_period",
        #     inputs="this should end with a period",
        #     expected_output="This should end with a period.",
        #     metadata={"difficulty": "easy"},
        #     evaluators=(EqualsExpected(),),
        # ),
        # Case(
        #     name="short_ack_exchange",
        #     inputs="this is fine right yes of course",
        #     expected_output="This is fine, right? Yes, of course.",
        #     metadata={"difficulty": "easy"},
        #     evaluators=(EqualsExpected(),),
        # ),
        # Case(
        #     name="acronym_caps",
        #     inputs="cia operative said go now do you agree",
        #     expected_output="CIA operative said go now. Do you agree?",
        #     metadata={"difficulty": "medium"},
        #     evaluators=(EqualsExpected(),),
        # ),
        # Case(
        #     name="long_run_on_to_sentences",
        #     inputs="we met in berlin in june we walked the river we talked about work and travel is that okay with you",
        #     expected_output="We met in Berlin in June. We walked the river. We talked about work and travel. Is that okay with you?",
        #     metadata={"difficulty": "hard"},
        #     evaluators=(EqualsExpected(),),
        # ),
    ],
    evaluators=[],
)

def main(text: str) -> str:
    result = agent.run_sync(text)
    return result.output

if __name__ == "__main__":
    report = tfl_dataset.evaluate_sync(main)
    report.print()
