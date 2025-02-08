"""Event sources for LLMling agent."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, SecretStr


if TYPE_CHECKING:
    from llmling_agent.messaging.messages import ChatMessage
    from llmling_agent.talk.talk import Talk

ConnectionEventType = Literal[
    "message_received",
    "message_processed",
    "message_forwarded",
    "queue_filled",
    "queue_triggered",
]

DEFAULT_TEMPLATE = """
{%- if include_timestamp %}at {{ timestamp }}{% endif %}
Event from {{ source }}:
{%- if include_metadata %}
Metadata:
{% for key, value in metadata.items() %}
{{ key }}: {{ value }}
{% endfor %}
{% endif %}
{{ content }}
"""


@dataclass(frozen=True, kw_only=True)
class EventData:
    """Base class for event data."""

    source: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, source: str, **kwargs: Any) -> Self:
        """Create event with current timestamp."""
        return cls(source=source, timestamp=datetime.now(), **kwargs)

    @abstractmethod
    def to_prompt(self) -> str:
        """Convert event to agent prompt."""

    async def format(self, config: EventSourceConfig) -> str:
        """Wraps core message with configurable template."""
        from jinja2 import Environment

        env = Environment(trim_blocks=True, lstrip_blocks=True)
        template = env.from_string(config.template)

        return template.render(
            source=self.source,
            content=self.to_prompt(),  # Use the core message
            metadata=self.metadata,
            timestamp=self.timestamp,
            include_metadata=config.include_metadata,
            include_timestamp=config.include_timestamp,
        )


@dataclass(frozen=True, kw_only=True)
class UIEvent(EventData):
    """Event triggered through UI interaction."""

    type: Literal["command", "message", "agent_command", "agent_message"]
    """Type of UI interaction that triggered this event."""

    content: str
    """The actual content (command string, voice command, etc.)."""

    args: list[str] = field(default_factory=list)
    """Additional arguments for the interaction."""

    kwargs: dict[str, Any] = field(default_factory=dict)
    """Additional options/parameters."""

    agent_name: str | None = None
    """Target agent for @agent messages/commands."""

    def to_prompt(self) -> str:
        """Convert event to agent prompt."""
        match self.type:
            case "command":
                args_str = " ".join(self.args)
                kwargs_str = " ".join(f"--{k}={v}" for k, v in self.kwargs.items())
                return f"UI Command: /{self.content} {args_str} {kwargs_str}"
            case "shortcut" | "gesture":
                return f"UI Action: {self.content}"
            case "voice":
                return f"Voice Command: {self.content}"
            case _:
                raise ValueError(self.type)


@dataclass(frozen=True)
class ConnectionEvent[TTransmittedData](EventData):
    """Event from connection activity."""

    connection_name: str
    """Name of the connection which fired an event."""

    connection: Talk[TTransmittedData]
    """The connection which fired the event."""

    event_type: ConnectionEventType
    """Type of event that occurred."""

    message: ChatMessage[TTransmittedData] | None = None
    """The message at the stage of the event."""

    def to_prompt(self) -> str:
        """Convert event to agent prompt."""
        base = f"Connection '{self.connection_name}' event: {self.event_type}"
        if self.message:
            return f"{base}\nMessage content: {self.message.content}"
        return base


class EventSourceConfig(BaseModel):
    """Base configuration for event sources."""

    type: str = Field(init=False)
    """Discriminator field for event source types."""

    name: str
    """Unique identifier for this event source."""

    enabled: bool = True
    """Whether this event source is active."""

    template: str = DEFAULT_TEMPLATE
    """Jinja2 template for formatting events."""

    include_metadata: bool = True
    """Control metadata visibility in template."""

    include_timestamp: bool = True
    """Control timestamp visibility in template."""

    model_config = ConfigDict(frozen=True, use_attribute_docstrings=True, extra="forbid")


class FileWatchConfig(EventSourceConfig):
    """File watching event source."""

    type: Literal["file"] = Field("file", init=False)
    """File / folder content change events."""

    paths: list[str]
    """Paths or patterns to watch for changes."""

    extensions: list[str] | None = None
    """File extensions to monitor (e.g. ['.py', '.md'])."""

    ignore_paths: list[str] | None = None
    """Paths or patterns to ignore."""

    recursive: bool = True
    """Whether to watch subdirectories."""

    debounce: int = 1600
    """Minimum time (ms) between trigger events."""


class WebhookConfig(EventSourceConfig):
    """Webhook event source."""

    type: Literal["webhook"] = Field("webhook", init=False)
    """webhook-based event."""

    port: int
    """Port to listen on."""

    path: str
    """URL path to handle requests."""

    secret: str | None = None
    """Optional secret for request validation."""


class TimeEventConfig(EventSourceConfig):
    """Time-based event source configuration."""

    type: Literal["time"] = Field("time", init=False)
    """Time event."""

    schedule: str
    """Cron expression for scheduling (e.g. '0 9 * * 1-5' for weekdays at 9am)"""

    prompt: str
    """Prompt to send to the agent when the schedule triggers."""

    timezone: str | None = None
    """Timezone for schedule (defaults to system timezone)"""

    skip_missed: bool = False
    """Whether to skip executions missed while agent was inactive"""


class EmailConfig(EventSourceConfig):
    """Email event source configuration.

    Monitors an email inbox for new messages and converts them to events.
    """

    type: Literal["email"] = Field("email", init=False)
    """Email event."""

    host: str = Field(description="IMAP server hostname")
    """IMAP server hostname (e.g. 'imap.gmail.com')"""

    port: int = Field(default=993)
    """Server port (defaults to 993 for IMAP SSL)"""

    username: str
    """Email account username/address"""

    password: SecretStr
    """Account password or app-specific password"""

    folder: str = Field(default="INBOX")
    """Folder/mailbox to monitor"""

    ssl: bool = Field(default=True)
    """Whether to use SSL/TLS connection"""

    check_interval: int = Field(
        default=60, gt=0, description="Seconds between inbox checks"
    )
    """How often to check for new emails (in seconds)"""

    mark_seen: bool = Field(default=True)
    """Whether to mark processed emails as seen"""

    filters: dict[str, str] = Field(
        default_factory=dict, description="Email filtering criteria"
    )
    """Filtering rules for emails (subject, from, etc)"""

    max_size: int | None = Field(default=None, description="Maximum email size in bytes")
    """Size limit for processed emails"""


class ConnectionTriggerConfig(EventSourceConfig):
    """Trigger config specifically for connection events."""

    type: Literal["connection"] = Field("connection", init=False)
    """Connection event trigger."""

    source: str | None = None
    """Connection source name."""

    target: str | None = None
    """Connection to trigger."""

    event: ConnectionEventType
    """Event type to trigger on."""

    condition: ConnectionEventConditionType | None = None
    """Condition-based filter for the event."""

    async def matches_event(self, event: ConnectionEvent[Any]) -> bool:
        """Check if this trigger matches the event."""
        # First check event type
        if event.event_type != self.event:
            return False

        # Check source/target filters
        if self.source and event.connection.source.name != self.source:
            return False
        if self.target and not any(
            t.name == self.target for t in event.connection.targets
        ):
            return False

        # Check condition if any
        if self.condition:
            return await self.condition.check(event)

        return True


EventConfig = Annotated[
    FileWatchConfig
    | WebhookConfig
    | EmailConfig
    | TimeEventConfig
    | ConnectionTriggerConfig,
    Field(discriminator="type"),
]


class ConnectionEventCondition(BaseModel):
    """Base conditions specifically for connection events."""

    type: str = Field(init=False)

    async def check(self, event: ConnectionEvent[Any]) -> bool:
        raise NotImplementedError


class ConnectionContentCondition(ConnectionEventCondition):
    """Simple content matching for connection events."""

    type: Literal["content"] = Field("content", init=False)
    """Content-based trigger."""

    words: list[str]
    """List of words to match."""

    mode: Literal["any", "all"] = "any"
    """Matching mode."""

    async def check(self, event: ConnectionEvent[Any]) -> bool:
        if not event.message:
            return False
        text = str(event.message.content)
        return any(word in text for word in self.words)


class ConnectionJinja2Condition(ConnectionEventCondition):
    """Flexible Jinja2 condition for connection events."""

    type: Literal["jinja2"] = Field("jinja2", init=False)
    """Jinja2-based trigger configuration."""

    template: str
    """Jinja2-Template (needs to return a "boolean" string)."""

    async def check(self, event: ConnectionEvent[Any]) -> bool:
        from jinja2 import Environment

        env = Environment()
        template = env.from_string(self.template)
        result = template.render(event=event)
        return result.strip().lower() == "true"


ConnectionEventConditionType = Annotated[
    ConnectionContentCondition | ConnectionJinja2Condition,
    Field(discriminator="type"),
]
