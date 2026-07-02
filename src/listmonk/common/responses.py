from klarient import ResponseMap


class BooleanResponse(ResponseMap):
    """Response wrapper for listmonk boolean result payloads."""

    @property
    def data(self) -> bool:
        """Boolean value returned by the endpoint."""
        return bool(self["data"])
