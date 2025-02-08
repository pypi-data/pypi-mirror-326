# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...entity_types.types.entity_id import EntityId
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class EntityGroupRemoveEntitiesRequest(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.entity_group_types import EntityGroupRemoveEntitiesRequest

    EntityGroupRemoveEntitiesRequest(
        entity_ids=[
            "ent_8545a84e-a45f-41bf-bdf1-33b42a55812c",
            "ent_21661ac1-a2a8-4465-a6c0-64474ba8181d",
        ],
    )
    """

    entity_ids: typing.List[EntityId] = pydantic.Field(alias="entityIds")
    """
    List of entity IDs or foreign IDs to remove from the group
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
