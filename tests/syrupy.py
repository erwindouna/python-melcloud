"""Syrupy snapshot extension for python-melcloud."""

from dataclasses import asdict, is_dataclass
from typing import TYPE_CHECKING, Any

from syrupy.extensions.amber import AmberDataSerializer, AmberSnapshotExtension

if TYPE_CHECKING:
    from syrupy.types import (
        PropertyFilter,
        PropertyMatcher,
        PropertyPath,
        SerializableData,
    )


class MelCloudSnapshotSerializer(AmberDataSerializer):
    """MELCloud snapshot serializer for Syrupy.

    Converts dataclass instances to dicts before serialization so that
    mashumaro-based models serialize cleanly.
    """

    @classmethod
    def _serialize(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        exclude: "PropertyFilter | None" = None,
        include: "PropertyFilter | None" = None,
        matcher: "PropertyMatcher | None" = None,
        path: "PropertyPath" = (),
        visited: set[Any] | None = None,
    ) -> str:
        """Pre-process data before serializing."""
        serializable_data = data
        if is_dataclass(type(data)):
            serializable_data = asdict(data)

        return super()._serialize(
            serializable_data,
            depth=depth,
            exclude=exclude,
            include=include,
            matcher=matcher,
            path=path,
            visited=visited,
        )


class MelCloudSnapshotExtension(AmberSnapshotExtension):
    """MELCloud extension for Syrupy."""

    VERSION = "1"

    serializer_class: type[AmberDataSerializer] = MelCloudSnapshotSerializer
