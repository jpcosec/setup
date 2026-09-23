"""SLDB models for the setup repo's external-resources surface."""

from typing import Annotated, Optional

from pydantic import Field

from sldb import StructuredNLDoc


ExternalResourceTag = Annotated[
    str,
    Field(
        pattern=r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$",
        description="Namespaced tag in the form namespace:value, using the namespaces defined in desk/atoms/tag-namespaces.yaml (domain, layer, system, topic).",
    ),
]


class ExternalResourceDoc(StructuredNLDoc):
    """Model for one external resource (tool, skill, service) used or evaluated by the setup."""

    __semantics__ = {
        "type": ["external", "resource"],
        "workspace": ["external-resources"],
    }
    __template__ = """---
# Human-readable name of the resource
name: ⸢rev•name⸥
# Official docs or repository URL
page: ⸢rev•page⸥
# true | false — whether the resource is installed locally
installed: ⸢rev•installed⸥
# Local install path or install command; set when installed is true
install_path: ⸢optrev•install_path⸥
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags: ⸢rev•tags⸥
---

# ⸢render•name⸥

## Summary

_One paragraph: what this resource is and why it matters to this setup._

⸢rev•summary⸥

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

⸢rev•usage⸥

## Status

_How it is currently working; keep empty when not installed._

⸢optrev•status_notes⸥

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

⸢optrev•issues_log⸥
""".strip()

    name: str = Field(
        description="Human-readable name of the external resource."
    )
    summary: str = Field(
        description=(
            "One-paragraph description of what the resource is and why it "
            "matters to this setup."
        )
    )
    page: str = Field(
        description="Official documentation or repository URL for the resource."
    )
    usage: str = Field(
        description=(
            "How the resource is used in this setup: entry commands, hook "
            "wiring, workflows, and integration points."
        )
    )
    tags: list[ExternalResourceTag] = Field(
        default_factory=list,
        description=(
            "Namespaced tags in namespace:value form using the namespaces "
            "defined in desk/atoms/tag-namespaces.yaml (domain, layer, "
            "system, topic). Repeated tags across fichas reveal groups, "
            "such as two IDEs sharing one tag."
        ),
    )
    installed: bool = Field(
        default=False,
        description="Whether the resource is installed locally right now.",
    )
    install_path: Optional[str] = Field(
        default=None,
        description=(
            "Local install location (binary path, directory, or install "
            "command). Set when installed is true."
        ),
    )
    status_notes: Optional[str] = Field(
        default=None,
        description=(
            "How the resource is currently working: state, usage evidence, "
            "and observed behavior. Only meaningful when installed is true."
        ),
    )
    issues_log: Optional[str] = Field(
        default=None,
        description=(
            "Dated log of problems, quirks, and their resolutions. Only "
            "meaningful when installed is true."
        ),
    )