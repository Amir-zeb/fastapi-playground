from fastapi import status


class AppException(Exception):
    status: int
    detail: str

    def __init__(self, detail: str, status: int):
        self.detail = detail
        self.status = status
        super().__init__(detail)


class EmailAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            detail="Email already registered",
            status=status.HTTP_409_CONFLICT,
        )


class PasswordDoesNotMatchError(AppException):
    def __init__(self):
        super().__init__(
            detail="Password does not match",
            status=status.HTTP_401_UNAUTHORIZED,
        )


class InvalidCredentialsError(AppException):
    def __init__(self):
        super().__init__(
            detail="Invalid email or password",
            status=status.HTTP_401_UNAUTHORIZED,
        )