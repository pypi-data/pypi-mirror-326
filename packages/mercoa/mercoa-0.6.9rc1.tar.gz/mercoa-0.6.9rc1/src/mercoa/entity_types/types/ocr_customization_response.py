# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class OcrCustomizationResponse(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.entity_types import OcrCustomizationResponse

    OcrCustomizationResponse(
        line_items=True,
        collapse_line_items=True,
        invoice_metadata=True,
        line_item_metadata=True,
        line_item_gl_account_id=True,
        predict_metadata=True,
        tax_and_shipping_as_line_items=True,
    )
    """

    line_items: bool = pydantic.Field(alias="lineItems")
    """
    Extract line items from the invoice. Defaults to true.
    """

    collapse_line_items: bool = pydantic.Field(alias="collapseLineItems")
    """
    If true, the line items will be collapsed into a single line item. Defaults to false.
    """

    invoice_metadata: bool = pydantic.Field(alias="invoiceMetadata")
    """
    Pull custom metadata at the invoice level. Defaults to true.
    """

    line_item_metadata: bool = pydantic.Field(alias="lineItemMetadata")
    """
    Pull custom metadata at the line item level. Defaults to true.
    """

    line_item_gl_account_id: bool = pydantic.Field(alias="lineItemGlAccountId")
    """
    Pull GL Account ID at the line item level. Defaults to true.
    """

    predict_metadata: bool = pydantic.Field(alias="predictMetadata")
    """
    Use AI to predict metadata from historical data. Defaults to true.
    """

    tax_and_shipping_as_line_items: bool = pydantic.Field(alias="taxAndShippingAsLineItems")
    """
    Pull tax and shipping information as line items. Defaults to true. If false, tax and shipping will extracted as invoice level fields.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
