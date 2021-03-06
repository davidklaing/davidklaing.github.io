class SiteBuilderException(BaseException):
    """Generic exception."""


class MissingAuthorException(SiteBuilderException):
    """Author listed in books or readings but missing from authors table."""


class MissingBookException(SiteBuilderException):
    """Book listed in readings but missing from books table."""