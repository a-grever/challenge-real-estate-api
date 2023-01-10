import pydantic


class Address(pydantic.BaseModel):
    street: str
    house: str
