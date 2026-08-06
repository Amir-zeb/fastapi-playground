from fastapi import status


class AppException(Exception):
    status_code: int
    detail: str

    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class EmailAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            detail="Email already registered",
            status_code=status.HTTP_409_CONFLICT,
        )


class PasswordDoesNotMatchError(AppException):
    def __init__(self):
        super().__init__(
            detail="Password does not match",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class InvalidCredentialsError(AppException):
    def __init__(self):
        super().__init__(
            detail="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )