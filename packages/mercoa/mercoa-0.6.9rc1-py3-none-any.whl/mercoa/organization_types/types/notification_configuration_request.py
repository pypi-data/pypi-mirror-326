# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class NotificationConfigurationRequest_Invoice(UniversalBaseModel):
    notification_type: typing.Literal["invoice"] = pydantic.Field(alias="notificationType", default="invoice")
    url: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


NotificationConfigurationRequest = NotificationConfigurationRequest_Invoice
