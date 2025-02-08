# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
from .notification_type import NotificationType
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class UserNotificationPolicyResponse(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.entity_types import UserNotificationPolicyResponse

    UserNotificationPolicyResponse(
        disabled=True,
        digest=False,
        immediate=True,
        type="INVOICE_APPROVED",
    )
    """

    disabled: bool = pydantic.Field()
    """
    True if the selected notification type is disabled for this user
    """

    digest: bool = pydantic.Field()
    """
    True if the selected notification type is sent as a digest.
    """

    immediate: bool = pydantic.Field()
    """
    True if the selected notification type is sent immediately.
    """

    type: NotificationType

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
