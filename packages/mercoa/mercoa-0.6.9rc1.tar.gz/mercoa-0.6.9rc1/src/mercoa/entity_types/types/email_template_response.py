# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from .email_template_id import EmailTemplateId
from .entity_id import EntityId
import pydantic
from .email_template_type import EmailTemplateType
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class EmailTemplateResponse(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.entity_types import EmailTemplateResponse

    EmailTemplateResponse(
        id="emt_8545a84e-a45f-41bf-bdf1-33b42a55812c",
        entity_id="ent_21661ac1-a2a8-4465-a6c0-64474ba8181d",
        template_type="PAYMENT",
        name="Generic Payment Email",
        subject="Action Required - Your payment is due",
        content="<h1>Your invoice has been sent.</h1>",
        is_default=True,
    )
    """

    id: EmailTemplateId
    entity_id: EntityId = pydantic.Field(alias="entityId")
    """
    The ID of the entity that this email template is associated with.
    """

    template_type: EmailTemplateType = pydantic.Field(alias="templateType")
    name: str = pydantic.Field()
    """
    The name of the email template.
    """

    subject: str = pydantic.Field()
    """
    The subject of the email template.
    """

    content: str = pydantic.Field()
    """
    The HTML content of the email template.
    """

    is_default: bool = pydantic.Field(alias="isDefault")
    """
    True if this email template is the default template for new invoices.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
