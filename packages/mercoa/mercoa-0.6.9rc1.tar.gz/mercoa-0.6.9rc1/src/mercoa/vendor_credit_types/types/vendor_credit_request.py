# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
from ...payment_method_types.types.currency_code import CurrencyCode
import typing
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class VendorCreditRequest(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.vendor_credit_types import VendorCreditRequest

    VendorCreditRequest(
        total_amount=100.0,
        currency="USD",
        note="This is a note",
    )
    """

    total_amount: float = pydantic.Field(alias="totalAmount")
    """
    Total amount of the vendor credit in major units
    """

    currency: CurrencyCode = pydantic.Field()
    """
    Currency code for the amount. Defaults to USD.
    """

    note: typing.Optional[str] = pydantic.Field(default=None)
    """
    An optional note to attach to the vendor credit
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
