# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from .metadata_type import MetadataType
from .metadata_validation_rule import MetadataValidationRule
from .metadata_show_conditions import MetadataShowConditions
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class MetadataSchema(UniversalBaseModel):
    key: str
    display_name: str = pydantic.Field(alias="displayName")
    description: typing.Optional[str] = None
    line_item: typing.Optional[bool] = pydantic.Field(alias="lineItem", default=None)
    """
    Whether or not this field should be shown on line items. If true, this field will be shown on each line item. If false, the field will be shown on the invoice level. Defaults to false.
    """

    type: MetadataType
    allow_multiple: typing.Optional[bool] = pydantic.Field(alias="allowMultiple", default=None)
    """
    Whether or not multiple values are allowed for this field. Defaults to false. If true, the value will be a list of the specified type.
    """

    validation_rules: typing.Optional[MetadataValidationRule] = pydantic.Field(alias="validationRules", default=None)
    """
    Validation rules are currently only supported for STRING types.
    """

    show_conditions: typing.Optional[MetadataShowConditions] = pydantic.Field(alias="showConditions", default=None)
    """
    A list of conditional rules that determine whether or not this field should be shown. The field will only be shown if all of the conditions are met. If no conditions are specified, the field will always be shown.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
