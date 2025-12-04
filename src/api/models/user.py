from msgspec import Struct

class UserCreate(Struct, kw_only=True):
    name: str
    surname: str | None = None
    password: str

class UserPatch(Struct, kw_only=True, omit_defaults=True):
    name: str | None = None
    surname: str | None = None
    password: str | None = None