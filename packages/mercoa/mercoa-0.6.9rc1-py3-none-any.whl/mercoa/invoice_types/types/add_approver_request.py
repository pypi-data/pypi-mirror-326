# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .approval_slot_id import ApprovalSlotId
import pydantic
from ...entity_types.types.entity_user_id import EntityUserId
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class AddApproverRequest(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.invoice_types import AddApproverRequest

    AddApproverRequest(
        approval_slot_id="inap_9bb311c9-7c15-4c9e-8148-63814e0abec6",
        user_id="user_e24fc81c-c5ee-47e8-af42-4fe29d895506",
    )
    """

    approval_slot_id: typing.Optional[ApprovalSlotId] = pydantic.Field(alias="approvalSlotId", default=None)
    """
    The identifier for the approval slot this user is assigned to.
    """

    user_id: EntityUserId = pydantic.Field(alias="userId")
    """
    The ID or the Foreign ID of the user to add to the approval slot.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
