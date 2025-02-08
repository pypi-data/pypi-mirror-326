# This file was auto-generated by Fern from our API Definition.

from .generic_payment_rail_response import GenericPaymentRailResponse
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class CustomPaymentRailResponse(GenericPaymentRailResponse):
    schema_id: str = pydantic.Field(alias="schemaId")

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
