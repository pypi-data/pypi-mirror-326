# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
from ...entity_types.types.entity_response import EntityResponse
import typing
from ...entity_types.types.entity_user_response import EntityUserResponse
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class EntityWebhook(UniversalBaseModel):
    """
    Examples
    --------
    import datetime

    from mercoa.commons import Address, PhoneNumber
    from mercoa.entity_types import (
        BusinessProfileResponse,
        Ein,
        EntityResponse,
        EntityUserResponse,
        ProfileResponse,
        TaxId,
    )
    from mercoa.webhooks import EntityWebhook

    EntityWebhook(
        event_type="entity.created",
        entity=EntityResponse(
            id="ent_8545a84e-a45f-41bf-bdf1-33b42a55812c",
            foreign_id="MY-DB-ID-12345",
            name="Acme Inc.",
            email="customer@acme.com",
            accepted_tos=True,
            status="verified",
            is_customer=True,
            is_payor=True,
            is_payee=False,
            is_network_payor=False,
            is_network_payee=False,
            account_type="business",
            updated_at=datetime.datetime.fromisoformat(
                "2024-01-02 00:00:00+00:00",
            ),
            created_at=datetime.datetime.fromisoformat(
                "2024-01-01 00:00:00+00:00",
            ),
            profile=ProfileResponse(
                business=BusinessProfileResponse(
                    email="customer@acme.com",
                    legal_business_name="Acme Inc.",
                    business_type="llc",
                    phone=PhoneNumber(
                        country_code="1",
                        number="4155551234",
                    ),
                    address=Address(
                        address_line_1="123 Main St",
                        address_line_2="Unit 1",
                        city="San Francisco",
                        state_or_province="CA",
                        postal_code="94105",
                        country="US",
                    ),
                    tax_id_provided=True,
                    tax_id=TaxId(
                        ein=Ein(
                            number="12-3456789",
                        ),
                    ),
                    owners_provided=True,
                ),
            ),
        ),
        user=EntityUserResponse(
            id="user_ec3aafc8-ea86-408a-a6c1-545497badbbb",
            foreign_id="MY-DB-ID-12345",
            email="john.doe@acme.com",
            name="John Doe",
            roles=["admin", "approver"],
            created_at=datetime.datetime.fromisoformat(
                "2024-01-01 00:00:00+00:00",
            ),
            updated_at=datetime.datetime.fromisoformat(
                "2024-01-01 00:00:00+00:00",
            ),
        ),
    )
    """

    event_type: str = pydantic.Field(alias="eventType")
    entity: EntityResponse
    user: typing.Optional[EntityUserResponse] = pydantic.Field(default=None)
    """
    User who initiated the change.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
