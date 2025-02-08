# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .integration_type import IntegrationType
import typing
from .connection_status import ConnectionStatus
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class Connection(UniversalBaseModel):
    """
    Schema for connection with config fields.
    """

    name: str
    integration_type: IntegrationType
    integration_credential_id: typing.Optional[str] = None
    status: ConnectionStatus
    short_name: str
    id: str
    organization_id: str
    created_by_email: str
    modified_by_email: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
