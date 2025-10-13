# type annotation for list
from typing import List

# automatic validation and serialisation with Pydantic BaseModel
# field - function extra metadata and constraints
from pydantic import BaseModel, Field


# metadata we put here we will propagate leter to be used by the agent
class Source(BaseModel):
    """Schema for source used by the agent"""

    url: str = Field(description="The URL of the source")
    description: str = Field(description="description of the job requirments")
    salary: str = Field(
        default_factory=None,
        description="salary, if there is any, or information on any money that could be earned. Can be empty",
    )


# now LLMs can handle composable interfaces litke this
class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer: List[Source] = Field(
        default_factory=list,  # used by pydantic to generate when nothing is there
        description="List of sources used to generate the answer",
    )
