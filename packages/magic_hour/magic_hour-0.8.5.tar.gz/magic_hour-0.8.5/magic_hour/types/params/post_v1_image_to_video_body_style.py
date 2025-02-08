import typing
import typing_extensions
import pydantic


class PostV1ImageToVideoBodyStyle(typing_extensions.TypedDict):
    """
    PostV1ImageToVideoBodyStyle
    """

    prompt: typing_extensions.Required[typing.Optional[str]]
    """
    The prompt used for the video.
    """


class _SerializerPostV1ImageToVideoBodyStyle(pydantic.BaseModel):
    """
    Serializer for PostV1ImageToVideoBodyStyle handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    prompt: typing.Optional[str] = pydantic.Field(
        alias="prompt",
    )
