# This file was auto-generated by Fern from our API Definition.

import typing

NotificationType = typing.Union[
    typing.Literal[
        "INVOICE_APPROVAL_NEEDED",
        "INVOICE_APPROVED",
        "INVOICE_REJECTED",
        "INVOICE_SCHEDULED",
        "INVOICE_PENDING",
        "INVOICE_PAID",
        "INVOICE_CANCELED",
        "INVOICE_CREATED",
        "INVOICE_EMAILED",
        "INVOICE_FAILED",
        "COUNTERPARTY_ONBOARDING_COMPLETED",
    ],
    typing.Any,
]
