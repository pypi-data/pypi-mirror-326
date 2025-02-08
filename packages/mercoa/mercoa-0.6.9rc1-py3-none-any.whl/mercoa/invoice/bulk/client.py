# This file was auto-generated by Fern from our API Definition.

import typing
from ...core.client_wrapper import SyncClientWrapper
from ...invoice_types.types.bulk_invoice_creation_request import BulkInvoiceCreationRequest
from ...core.request_options import RequestOptions
from ...invoice_types.types.bulk_invoice_creation_response import BulkInvoiceCreationResponse
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ...core.pydantic_utilities import parse_obj_as
from ...commons.errors.bad_request import BadRequest
from ...commons.errors.unauthorized import Unauthorized
from ...commons.errors.forbidden import Forbidden
from ...commons.errors.not_found import NotFound
from ...commons.errors.conflict import Conflict
from ...commons.errors.internal_server_error import InternalServerError
from ...commons.errors.unimplemented import Unimplemented
from ...core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class BulkClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def create(
        self,
        *,
        request: BulkInvoiceCreationRequest,
        emit_webhooks: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BulkInvoiceCreationResponse:
        """
        Create multiple invoices in bulk. This endpoint will process synchronously and return a list of invoices that were created or failed to create.

        Parameters
        ----------
        request : BulkInvoiceCreationRequest

        emit_webhooks : typing.Optional[bool]
            If true, webhooks will be emitted for each invoice that is created. By default, webhooks are not emitted.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BulkInvoiceCreationResponse

        Examples
        --------
        import datetime

        from mercoa import Mercoa
        from mercoa.invoice_types import (
            BulkInvoiceCreationRequest,
            InvoiceCreationWithEntityRequest,
            InvoiceLineItemCreationRequest,
            PaymentDestinationOptions_Check,
        )

        client = Mercoa(
            token="YOUR_TOKEN",
        )
        client.invoice.bulk.create(
            request=BulkInvoiceCreationRequest(
                invoices=[
                    InvoiceCreationWithEntityRequest(
                        status="NEW",
                        amount=100.0,
                        currency="USD",
                        invoice_date=datetime.datetime.fromisoformat(
                            "2021-01-01 00:00:00+00:00",
                        ),
                        due_date=datetime.datetime.fromisoformat(
                            "2021-01-31 00:00:00+00:00",
                        ),
                        invoice_number="INV-123",
                        note_to_self="For the month of January",
                        payer_id="ent_8545a84e-a45f-41bf-bdf1-33b42a55812c",
                        payment_source_id="pm_4794d597-70dc-4fec-b6ec-c5988e759769",
                        vendor_id="ent_21661ac1-a2a8-4465-a6c0-64474ba8181d",
                        payment_destination_id="pm_5fde2f4a-facc-48ef-8f0d-6b7d087c7b18",
                        payment_destination_options=PaymentDestinationOptions_Check(
                            delivery="MAIL",
                            print_description=True,
                        ),
                        line_items=[
                            InvoiceLineItemCreationRequest(
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
                            )
                        ],
                        creator_entity_id="ent_8545a84e-a45f-41bf-bdf1-33b42a55812c",
                        creator_user_id="user_e24fc81c-c5ee-47e8-af42-4fe29d895506",
                    )
                ],
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "invoices",
            method="POST",
            params={
                "emitWebhooks": emit_webhooks,
            },
            json=request,
            request_options=request_options,
            omit=OMIT,
        )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        if 200 <= _response.status_code < 300:
            return typing.cast(
                BulkInvoiceCreationResponse,
                parse_obj_as(
                    type_=BulkInvoiceCreationResponse,  # type: ignore
                    object_=_response_json,
                ),
            )
        if "errorName" in _response_json:
            if _response_json["errorName"] == "BadRequest":
                raise BadRequest(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "Unauthorized":
                raise Unauthorized(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "Forbidden":
                raise Forbidden(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "NotFound":
                raise NotFound(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "Conflict":
                raise Conflict(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "InternalServerError":
                raise InternalServerError(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "Unimplemented":
                raise Unimplemented(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncBulkClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def create(
        self,
        *,
        request: BulkInvoiceCreationRequest,
        emit_webhooks: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BulkInvoiceCreationResponse:
        """
        Create multiple invoices in bulk. This endpoint will process synchronously and return a list of invoices that were created or failed to create.

        Parameters
        ----------
        request : BulkInvoiceCreationRequest

        emit_webhooks : typing.Optional[bool]
            If true, webhooks will be emitted for each invoice that is created. By default, webhooks are not emitted.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BulkInvoiceCreationResponse

        Examples
        --------
        import asyncio
        import datetime

        from mercoa import AsyncMercoa
        from mercoa.invoice_types import (
            BulkInvoiceCreationRequest,
            InvoiceCreationWithEntityRequest,
            InvoiceLineItemCreationRequest,
            PaymentDestinationOptions_Check,
        )

        client = AsyncMercoa(
            token="YOUR_TOKEN",
        )


        async def main() -> None:
            await client.invoice.bulk.create(
                request=BulkInvoiceCreationRequest(
                    invoices=[
                        InvoiceCreationWithEntityRequest(
                            status="NEW",
                            amount=100.0,
                            currency="USD",
                            invoice_date=datetime.datetime.fromisoformat(
                                "2021-01-01 00:00:00+00:00",
                            ),
                            due_date=datetime.datetime.fromisoformat(
                                "2021-01-31 00:00:00+00:00",
                            ),
                            invoice_number="INV-123",
                            note_to_self="For the month of January",
                            payer_id="ent_8545a84e-a45f-41bf-bdf1-33b42a55812c",
                            payment_source_id="pm_4794d597-70dc-4fec-b6ec-c5988e759769",
                            vendor_id="ent_21661ac1-a2a8-4465-a6c0-64474ba8181d",
                            payment_destination_id="pm_5fde2f4a-facc-48ef-8f0d-6b7d087c7b18",
                            payment_destination_options=PaymentDestinationOptions_Check(
                                delivery="MAIL",
                                print_description=True,
                            ),
                            line_items=[
                                InvoiceLineItemCreationRequest(
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
                                )
                            ],
                            creator_entity_id="ent_8545a84e-a45f-41bf-bdf1-33b42a55812c",
                            creator_user_id="user_e24fc81c-c5ee-47e8-af42-4fe29d895506",
                        )
                    ],
                ),
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "invoices",
            method="POST",
            params={
                "emitWebhooks": emit_webhooks,
            },
            json=request,
            request_options=request_options,
            omit=OMIT,
        )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        if 200 <= _response.status_code < 300:
            return typing.cast(
                BulkInvoiceCreationResponse,
                parse_obj_as(
                    type_=BulkInvoiceCreationResponse,  # type: ignore
                    object_=_response_json,
                ),
            )
        if "errorName" in _response_json:
            if _response_json["errorName"] == "BadRequest":
                raise BadRequest(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "Unauthorized":
                raise Unauthorized(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "Forbidden":
                raise Forbidden(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "NotFound":
                raise NotFound(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "Conflict":
                raise Conflict(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "InternalServerError":
                raise InternalServerError(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
            if _response_json["errorName"] == "Unimplemented":
                raise Unimplemented(
                    typing.cast(
                        str,
                        parse_obj_as(
                            type_=str,  # type: ignore
                            object_=_response_json["content"],
                        ),
                    )
                )
        raise ApiError(status_code=_response.status_code, body=_response_json)
