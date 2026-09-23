"""SLDB models for the setup repo's herdr command-reference surface."""

from typing import Annotated, Optional

from pydantic import Field

from sldb import StructuredNLDoc


HerdrCommandTag = Annotated[
    str,
    Field(
        pattern=r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$",
        description="Namespaced tag in the form namespace:value, using the namespaces defined in desk/atoms/tag-namespaces.yaml (domain, layer, system, topic).",
    ),
]


class HerdrCommandDoc(StructuredNLDoc):
    """Model for one herdr command reference atom (command, option semantics, jq returns, known errors)."""

    __semantics__ = {
        "type": ["command", "reference"],
        "workspace": ["desk", "atoms", "herdr"],
    }
    __template__ = """---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: ⸢rev•id⸥
# Full command as typed, e.g. 'herdr agent start'
command_path: ⸢rev•command_path⸥
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: ⸢rev•command_group⸥
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags: ⸢rev•tags⸥
---

# ⸢render•command_path⸥

## Synopsis

_What the command does, in one or two sentences._

⸢rev•synopsis⸥

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

⸢rev•syntax⸥

## Arguments

_Table of options: option, type, required, and what it does._

⸢rev•arguments⸥

## Returns

_What the command returns on success: JSON shape and location of the payload._

⸢optrev•returns⸥

## Returns jq

_jq paths to extract the returned payload into shell variables._

⸢optrev•returns_jq⸥

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

⸢optrev•example⸥

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

⸢optrev•errors⸥

## Notes

_Quirks, gotchas, and operational observations not covered above._

⸢optrev•notes⸥

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

⸢optrev•provenance⸥""".strip()

    id: str = Field(
        description="Stable, unique atom identifier, conventionally 'atom-herdr-<command>-<verb>'."
    )
    command_path: str = Field(
        description="Full command as typed, in the form 'herdr <group> <verb>' (e.g. 'herdr agent start')."
    )
    command_group: str = Field(
        description="Command family grouping used by the reference (e.g. 'agent', 'pane', 'machine')."
    )
    synopsis: str = Field(
        description=(
            "One or two sentences describing what the command does and when "
            "to use it."
        )
    )
    syntax: str = Field(
        description=(
            "Usage line(s) as shown by the command help, with '<>' for "
            "positionals, '--flags', and '[OPTIONS]'/'[...]' for optional parts."
        )
    )
    arguments: str = Field(
        description=(
            "Markdown table of options and arguments: option, type, whether "
            "it is required, and what it does."
        )
    )
    tags: list[HerdrCommandTag] = Field(
        default_factory=list,
        description=(
            "Namespaced tags in namespace:value form using the namespaces "
            "defined in desk/atoms/tag-namespaces.yaml (domain, layer, "
            "system, topic). Repeated tags across fichas reveal groups."
        ),
    )
    returns: str | None = Field(default=None, description="What the command returns on success: the JSON shape and where the payload lives (e.g. '.result.agent').")
    returns_jq: str | None = Field(default=None, description='jq paths to extract the returned payload into shell variables, with the exact jq invocation to capture them. None when the command returns no JSON payload worth capturing.')
    example: str | None = Field(default=None, description='Real end-to-end usage example, verified when possible, showing output captured with jq into shell variables.')
    errors: str | None = Field(default=None, description='Known error codes or symptoms, their meaning, and recovery steps, as a markdown table or list.')
    notes: str | None = Field(default=None, description='Quirks, gotchas, and operational observations not covered by the other sections.')
    provenance: Optional[str] = Field(default=None, description='Source of the documented behavior: help output, official docs, or live verification, with date and herdr version when relevant.')
