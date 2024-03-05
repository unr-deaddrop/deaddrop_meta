"""
Library adhering to the standard definition of a DeadDrop agent.

Although this can be used at runtime, its intended purpose is to facilitate
exposing various metadata to the server. This defines certain constants
that are intended to be shared across all agents (including those not
written in Python), such that a JSON metadata file can be generated
for the agent.
"""

from enum import Enum
from textwrap import dedent
from typing import Any, Type
import abc
import json

from pydantic import BaseModel


class SupportedOSTypes(str, Enum):
    """
    Enumeration of available operating systems supported by the entire framework.
    """

    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "mac"


class SupportedProtocols(str, Enum):
    """
    Enumeration of supported protocols.

    Naturally, this enumeration will never be "complete" if others without access
    to this library write new protocols. In turn, the names of protocols would
    simply have to be agreed upon in future agents and protocols.

    However, for the sake of this project, we'll list all "reference" protocols
    here.
    """

    DDDB_LOCAL = "dddb_local"
    DDDB_YOUTUBE = "dddb_youtube"
    PLAINTEXT_LOCAL = "plaintext_local"


class AgentBase(abc.ABC):
    """
    The generic agent definition class. This specifies the static metadata
    fields that agents are expected to define.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        The global name used for this agent.
        """
        pass

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """
        A brief description of this agent.

        The "source" should redirect the user to documentation if needed.
        """
        pass

    @property
    @abc.abstractmethod
    def version(self) -> str:
        """
        The version string for this agent.
        """
        pass

    @property
    @abc.abstractmethod
    def author(self) -> str:
        """
        The agent's author(s).
        """
        pass

    @property
    @abc.abstractmethod
    def source(self) -> str:
        """
        A link to the agent's source code.
        """
        pass

    @property
    @abc.abstractmethod
    def supported_operating_systems(self) -> list[SupportedOSTypes]:
        """
        A list of named and recognized operating systems this agent supports.
        """
        pass

    @property
    @abc.abstractmethod
    def supported_protocols(self) -> list[SupportedProtocols]:
        """
        A list of named and recognized protocols this agent supports.
        """
        pass

    @property
    @abc.abstractmethod
    def config_model(self) -> Type[BaseModel]:
        """
        The model representing all available configuration for this agent.
        """
        pass

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        """
        Convert this agent to a dictionary suitable for export.

        The structure is as follows:
        ```json
        {
            "name": str,
            "description": str,
            "version": str,
            "author": str,
            "source": str,
            "operating_systems": list[str],
            "protocols": list[str],
            "config": [
                {
                    // See Argument for what this looks like
                }
            ]
        }
        ```

        As always, ensure that the resulting dictionary is JSON serializable.
        """
        # The type ignores below are all the result of properties.
        return {
            "name": cls.name,
            "description": dedent(cls.description).strip(),  # type: ignore[arg-type]
            "version": cls.version,
            "author": cls.author,
            "source": cls.source,
            "operating_systems": cls.supported_operating_systems,
            "protocols": cls.supported_protocols,
            "config": cls.config_model.model_json_schema(),  # type: ignore[attr-defined]
        }

    @classmethod
    def to_json(cls, **kwargs) -> str:
        return json.dumps(cls.to_dict(), **kwargs)
