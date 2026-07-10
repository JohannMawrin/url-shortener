class ApplicationError(Exception):
    pass


class ShortURLNotFoundError(ApplicationError):
    def __init__(self, short_code: str) -> None:
        self.short_code = short_code
        self.message = f"Short URL with code '{short_code}' not found"
        super().__init__(self.message)
