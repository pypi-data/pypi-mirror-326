# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .metadata_customization_request import MetadataCustomizationRequest
from .payment_method_customization_request import PaymentMethodCustomizationRequest
import pydantic
from .ocr_customization_response import OcrCustomizationResponse
from .notification_customization_request import NotificationCustomizationRequest
from .workflow_customization_request import WorkflowCustomizationRequest
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class EntityCustomizationResponse(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.entity_types import (
        EntityCustomizationResponse,
        MetadataCustomizationRequest,
        NotificationCustomizationRequest,
        OcrCustomizationResponse,
        PaymentMethodCustomizationRequest_BankAccount,
        PaymentMethodCustomizationRequest_Check,
        PaymentMethodCustomizationRequest_Custom,
        WorkflowCustomizationRequest,
    )

    EntityCustomizationResponse(
        metadata=[
            MetadataCustomizationRequest(
                key="my_custom_field",
                disabled=True,
            ),
            MetadataCustomizationRequest(
                key="my_other_field",
                disabled=False,
            ),
        ],
        payment_source=[
            PaymentMethodCustomizationRequest_BankAccount(
                disabled=True,
                default_delivery_method="ACH_SAME_DAY",
            ),
            PaymentMethodCustomizationRequest_Custom(
                schema_id="cpms_7df2974a-4069-454c-912f-7e58ebe030fb",
                disabled=True,
            ),
        ],
        backup_disbursement=[
            PaymentMethodCustomizationRequest_Check(
                disabled=True,
                default_delivery_method="MAIL",
                print_description=True,
            )
        ],
        payment_destination=[
            PaymentMethodCustomizationRequest_BankAccount(
                disabled=True,
                default_delivery_method="ACH_SAME_DAY",
            ),
            PaymentMethodCustomizationRequest_Check(
                disabled=True,
                default_delivery_method="MAIL",
                print_description=True,
            ),
        ],
        ocr=OcrCustomizationResponse(
            line_items=True,
            collapse_line_items=True,
            invoice_metadata=True,
            line_item_metadata=True,
            line_item_gl_account_id=True,
            predict_metadata=True,
            tax_and_shipping_as_line_items=True,
        ),
        notifications=NotificationCustomizationRequest(
            assume_role="admin",
        ),
        workflow=WorkflowCustomizationRequest(
            auto_advance_invoice_status=True,
        ),
    )
    """

    metadata: typing.List[MetadataCustomizationRequest]
    payment_source: typing.List[PaymentMethodCustomizationRequest] = pydantic.Field(alias="paymentSource")
    backup_disbursement: typing.List[PaymentMethodCustomizationRequest] = pydantic.Field(alias="backupDisbursement")
    payment_destination: typing.List[PaymentMethodCustomizationRequest] = pydantic.Field(alias="paymentDestination")
    ocr: OcrCustomizationResponse
    notifications: NotificationCustomizationRequest
    workflow: WorkflowCustomizationRequest

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
