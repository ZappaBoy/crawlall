class PatternNotFoundError(Exception):
    def __init__(self, pattern: str):
        super().__init__(f"Pattern not found: {pattern}")
