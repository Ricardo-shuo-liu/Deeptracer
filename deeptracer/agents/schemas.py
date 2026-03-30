from pydantic import BaseModel, Field


class StructureAgentResult(BaseModel):
    summary: str = Field(description="One-paragraph structural summary.")
    focus_function: str = Field(description="The function a learner should inspect first.")
    points: list[str] = Field(description="Three concise structure insights.")


class PerformanceAgentResult(BaseModel):
    summary: str = Field(description="Short performance explanation.")
    hottest_function: str = Field(description="Most relevant hotspot.")
    points: list[str] = Field(description="Three concise performance insights.")


class MemoryAgentResult(BaseModel):
    summary: str = Field(description="Short memory explanation.")
    focus_area: str = Field(description="Most relevant memory hotspot.")
    points: list[str] = Field(description="Three concise memory insights.")


class SuggestionItem(BaseModel):
    id: str = Field(description="Stable suggestion id in kebab-case.")
    title: str = Field(description="Short user-facing title.")
    priority: str = Field(description="Priority label.")
    confidence: str = Field(description="Confidence label.")
    impact: str = Field(description="Expected impact.")
    risk: str = Field(description="Risk label.")
    file: str = Field(description="Display file label.")
    note: str = Field(description="One-line note shown in the list.")
    explanation: str = Field(description="Longer explanation for the detail panel.")
    diff: list[list] = Field(description="Diff preview rows as [line, marker, text, kind].")


class RefactorAgentResult(BaseModel):
    suggestions: list[SuggestionItem] = Field(description="One to three concrete suggestions.")


class TeachingAgentResult(BaseModel):
    overview: str = Field(description="Beginner-friendly overall explanation.")
    beginner_tip: str = Field(description="Practical tip for a beginner.")
    next_step: str = Field(description="Best next action for the user.")


class ChatMessage(BaseModel):
    role: str = Field(description="Role of the message sender (user/assistant).")
    content: str = Field(description="Content of the message.")


class ChatAgentResult(BaseModel):
    discussion: str = Field(description="Discussion about the code analysis and suggestions.")
    questions: list[str] = Field(description="Questions to ask the user for clarification.")
    next_steps: list[str] = Field(description="Recommended next steps for code improvement.")
    conversation_history: list[ChatMessage] = Field(description="Conversation history.")
