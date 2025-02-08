# This file was auto-generated by Fern from our API Definition.

from .payment_method_base_request import PaymentMethodBaseRequest
from .card_type import CardType
import pydantic
from .card_brand import CardBrand
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class CardRequest(PaymentMethodBaseRequest):
    card_type: CardType = pydantic.Field(alias="cardType")
    card_brand: CardBrand = pydantic.Field(alias="cardBrand")
    last_four: str = pydantic.Field(alias="lastFour")
    exp_month: str = pydantic.Field(alias="expMonth")
    exp_year: str = pydantic.Field(alias="expYear")
    token: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
