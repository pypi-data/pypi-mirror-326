# This file was auto-generated by Fern from our API Definition.

from .transaction_response_bank_to_bank_base import TransactionResponseBankToBankBase
import typing
from ...invoice_types.types.invoice_response import InvoiceResponse
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class TransactionResponseBankToBankWithInvoices(TransactionResponseBankToBankBase):
    invoices: typing.List[InvoiceResponse] = pydantic.Field()
    """
    Invoices associated with this transaction
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
