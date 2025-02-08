# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from .business_type import BusinessType
from ...commons.types.phone_number import PhoneNumber
from ...commons.types.address import Address
from .tax_id import TaxId
import datetime as dt
from .industry_codes import IndustryCodes
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class BusinessProfileRequest(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.commons import Address, PhoneNumber
    from mercoa.entity_types import BusinessProfileRequest, Ein, TaxId

    BusinessProfileRequest(
        email="customer@acme.com",
        legal_business_name="Acme Inc.",
        website="http://www.acme.com",
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
        tax_id=TaxId(
            ein=Ein(
                number="12-3456789",
            ),
        ),
    )
    """

    email: typing.Optional[str] = pydantic.Field(default=None)
    """
    Email address for the business. Required for KYB.
    """

    legal_business_name: str = pydantic.Field(alias="legalBusinessName")
    business_type: typing.Optional[BusinessType] = pydantic.Field(alias="businessType", default=None)
    phone: typing.Optional[PhoneNumber] = pydantic.Field(default=None)
    """
    Phone number for the business. Required for KYB.
    """

    doing_business_as: typing.Optional[str] = pydantic.Field(alias="doingBusinessAs", default=None)
    website: typing.Optional[str] = pydantic.Field(default=None)
    """
    Website URL for the business. Must be in the format http://www.example.com. Required for KYB if description is not provided.
    """

    description: typing.Optional[str] = pydantic.Field(default=None)
    """
    Description of the business. Required for KYB if website is not provided.
    """

    address: typing.Optional[Address] = pydantic.Field(default=None)
    """
    Address for the business. Required for KYB.
    """

    tax_id: typing.Optional[TaxId] = pydantic.Field(alias="taxId", default=None)
    """
    Tax ID for the business. Currently only EIN is supported. Required for KYB.
    """

    formation_date: typing.Optional[dt.datetime] = pydantic.Field(alias="formationDate", default=None)
    """
    Date of business formation
    """

    industry_codes: typing.Optional[IndustryCodes] = pydantic.Field(alias="industryCodes", default=None)
    """
    Industry code for the business. Required to collect funds.
    """

    average_monthly_transaction_volume: typing.Optional[float] = pydantic.Field(
        alias="averageMonthlyTransactionVolume", default=None
    )
    """
    Average monthly transaction volume for the business. Required to collect funds.
    """

    average_transaction_size: typing.Optional[float] = pydantic.Field(alias="averageTransactionSize", default=None)
    """
    Average transaction size for the business. Required to collect funds.
    """

    max_transaction_size: typing.Optional[float] = pydantic.Field(alias="maxTransactionSize", default=None)
    """
    Maximum transaction size for the business. Required to collect funds.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
