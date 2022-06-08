from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RegisterResponse:
    response: str


@dataclass(slots=True, frozen=True)
class LoginResponse:
    access: str | None
    refresh: str | None
    error: str | None
    status: int


@dataclass(slots=True, frozen=True)
class ChangePasswordResponse:
    error: str | None
    status: int
