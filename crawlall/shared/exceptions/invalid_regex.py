class InvalidRegexError(Exception):
    def __init__(self, regex: str):
        super().__init__(f"Invalid regex: {regex}")
