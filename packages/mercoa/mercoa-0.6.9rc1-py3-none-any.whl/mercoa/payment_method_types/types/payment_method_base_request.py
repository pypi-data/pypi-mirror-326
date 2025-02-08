# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class PaymentMethodBaseRequest(UniversalBaseModel):
    default_source: typing.Optional[bool] = pydantic.Field(alias="defaultSource", default=None)
    """
    If true, this payment method will be set as the default source. Only one payment method can be set as the default source. If another payment method is already set as the default source, it will be unset.
    """

    default_destination: typing.Optional[bool] = pydantic.Field(alias="defaultDestination", default=None)
    """
    If true, this payment method will be set as the default destination. Only one payment method can be set as the default destination. If another payment method is already set as the default destination, it will be unset.
    """

    external_accounting_system_id: typing.Optional[str] = pydantic.Field(
        alias="externalAccountingSystemId", default=None
    )
    """
    ID for this payment method in the external accounting system (e.g Rutter or Codat)
    """

    frozen: typing.Optional[bool] = pydantic.Field(default=None)
    """
    If true, this payment method will be frozen. Frozen payment methods cannot be used for payments, but will still be returned in API responses.
    """

    metadata: typing.Optional[typing.Dict[str, str]] = pydantic.Field(default=None)
    """
    Metadata associated with this payment method.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
