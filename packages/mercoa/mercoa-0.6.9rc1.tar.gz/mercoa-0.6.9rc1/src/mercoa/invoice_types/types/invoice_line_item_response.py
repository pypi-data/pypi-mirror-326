# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from .invoice_line_item_id import InvoiceLineItemId
import typing
import pydantic
from ...payment_method_types.types.currency_code import CurrencyCode
import datetime as dt
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class InvoiceLineItemResponse(UniversalBaseModel):
    """
    Examples
    --------
    import datetime

    from mercoa.invoice_types import InvoiceLineItemResponse

    InvoiceLineItemResponse(
        id="inli_26672f38-eb9a-48f1-a7a0-f1b855e38cd7",
        amount=100.0,
        currency="USD",
        description="Product A",
        name="Product A",
        quantity=1.0,
        unit_price=100.0,
        category="EXPENSE",
        service_start_date=datetime.datetime.fromisoformat(
            "2021-01-01 00:00:00+00:00",
        ),
        service_end_date=datetime.datetime.fromisoformat(
            "2021-01-31 00:00:00+00:00",
        ),
        metadata={"key1": "value1", "key2": "value2"},
        gl_account_id="600394",
        created_at=datetime.datetime.fromisoformat(
            "2021-01-01 00:00:00+00:00",
        ),
        updated_at=datetime.datetime.fromisoformat(
            "2021-01-01 00:00:00+00:00",
        ),
    )
    """

    id: InvoiceLineItemId
    amount: typing.Optional[float] = pydantic.Field(default=None)
    """
    Total amount of line item in major units.
    """

    currency: CurrencyCode
    description: typing.Optional[str] = None
    name: typing.Optional[str] = None
    quantity: typing.Optional[float] = None
    unit_price: typing.Optional[float] = pydantic.Field(alias="unitPrice", default=None)
    """
    Unit price of line item in major units.
    """

    category: str = pydantic.Field()
    """
    Category of the line item. Defaults to 'EXPENSE'.
    """

    service_start_date: typing.Optional[dt.datetime] = pydantic.Field(alias="serviceStartDate", default=None)
    service_end_date: typing.Optional[dt.datetime] = pydantic.Field(alias="serviceEndDate", default=None)
    metadata: typing.Optional[typing.Dict[str, str]] = None
    gl_account_id: typing.Optional[str] = pydantic.Field(alias="glAccountId", default=None)
    """
    ID of general ledger account associated with this line item.
    """

    created_at: dt.datetime = pydantic.Field(alias="createdAt")
    updated_at: dt.datetime = pydantic.Field(alias="updatedAt")

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
