# This file was auto-generated by Fern from our API Definition.

from .invoice_notification_configuration_request import InvoiceNotificationConfigurationRequest
from ...entity_types.types.notification_type import NotificationType
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class InvoiceNotificationConfigurationResponse(InvoiceNotificationConfigurationRequest):
    type: NotificationType

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
