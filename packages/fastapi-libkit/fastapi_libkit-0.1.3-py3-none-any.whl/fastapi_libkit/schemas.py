from inspect import signature, Parameter
from types import GenericAlias, UnionType

from fastapi.datastructures import UploadFile
from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from typing import Self, get_args, Type

modelT = Type[BaseModel]



def check_type_in_annotation(_type: type, annotation: type):
    if isinstance(annotation, GenericAlias):
        return _type is get_args(annotation)[0]
    elif isinstance(annotation, UnionType):
        args = get_args(annotation)
        left = args[0]
        right = args[1]
        return check_type_in_annotation(_type, left) or check_type_in_annotation(_type, right)
    else:
        return _type is annotation


class FormBodyMixin:

    @classmethod
    def as_form(cls):
        def wrapper(**kwargs) -> Self:
            return cls(**kwargs)

        _signature = signature(wrapper)

        parameters = []
        for field_name, field in cls.model_fields.items():  # type: ignore
            field: FieldInfo
            if check_type_in_annotation(UploadFile, field.annotation):
                default = field.default if field.default is not PydanticUndefined else Parameter.empty
            else:
                default = Form(default=field.default)
            parameters.append(
                Parameter(
                    field_name,
                    kind=Parameter.KEYWORD_ONLY,
                    default=default,
                    annotation=field.annotation,
                )
            )

        wrapper.__signature__ = _signature.replace(parameters=parameters)
        return wrapper


def as_form(model: modelT):
    def wrapper(**kwargs):
        return model(**kwargs)

    _signature = signature(wrapper)

    parameters = []
    for field_name, field in model.model_fields.items():  # type: ignore
        field: FieldInfo
        if check_type_in_annotation(UploadFile, field.annotation):
            default = field.default if field.default is not PydanticUndefined else Parameter.empty
        else:
            default = Form(default=field.default)
        parameters.append(
            Parameter(
                field_name,
                kind=Parameter.KEYWORD_ONLY,
                default=default,
                annotation=field.annotation,
            )
        )

    wrapper.__signature__ = _signature.replace(parameters=parameters)
    return wrapper