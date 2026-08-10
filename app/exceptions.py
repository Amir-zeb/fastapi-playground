from fastapi import status

class AppException(Exception):
    def __init__(self, detail: str, code: str, status: int)-> None :
        self.detail = detail
        self.code = code
        self.status = status
        super().__init__(detail)


class EmailAlreadyExistsError(AppException):
    def __init__(self)-> None   :
        super().__init__(
            detail="Email already registered",
            status=status.HTTP_409_CONFLICT,
            code="EMAIL_ALREADY_EXISTS",
        )


class PasswordDoesNotMatchError(AppException):
    def __init__(self)-> None :
        super().__init__(
            detail="Password does not match",
            status=status.HTTP_401_UNAUTHORIZED,
            code="PASSWORD_DOES_NOT_MATCH",
        )


class InvalidCredentialsError(AppException):
    def __init__(self)-> None :
        super().__init__(
            detail="Invalid email or password",
            status=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_CREDENTIALS",
        )


class InvalidTokenError(AppException):
    def __init__(self)-> None :
        super().__init__(
            detail="Invalid token",
            status=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_TOKEN",
        )


class TokenExpiredError(AppException):
    def __init__(self)-> None :
        super().__init__(
            detail="Token has expired",
            status=status.HTTP_401_UNAUTHORIZED,
            code="TOKEN_EXPIRED",
        )


class AuthRequired(AppException):
    def __init__(self)-> None :
        super().__init__(
            detail="Authentication required",
            status=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_REQUIRED",
        )

class UserNotFound(AppException):
    def __init__(self)-> None :
        super().__init__(
            detail="User not found",
            status=status.HTTP_404_NOT_FOUND,
            code="USER_NOT_FOUND",
        )