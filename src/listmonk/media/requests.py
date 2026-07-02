from __future__ import annotations

from pathlib import Path
from typing import Self

from klarient import (
    HTTPRequestOptions,
    MultipartBuilder,
    MultipartValue,
    RequestField,
    RequestFields,
    RequestOptionsProvider,
)


class MediaUpload(RequestFields, RequestOptionsProvider):
    """Multipart request for uploading media."""

    def __init__(
            self,
            *,
            file: bytes | MultipartValue | None = None,
            filename: str = "upload",
            content_type: str | None = None,
    ) -> None:
        super().__init__()
        if file is not None:
            self.file = (
                MultipartValue(file, filename=filename, content_type=content_type)
                if isinstance(file, bytes)
                else file
            )

    file = RequestField[MultipartValue](value_type=MultipartValue)

    @classmethod
    def from_file(
            cls,
            path: str | Path,
            *,
            content_type: str | None = None,
    ) -> MediaUpload:
        file_path = Path(path)
        return cls(
            file=file_path.read_bytes(),
            filename=file_path.name,
            content_type=content_type,
        )

    def with_file(
            self,
            data: bytes,
            *,
            filename: str = "upload",
            content_type: str | None = None,
    ) -> Self:
        """Set the media file from bytes."""
        self.file = MultipartValue(
            data,
            filename=filename,
            content_type=content_type,
        )
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        if self.file is None:
            raise ValueError("file is required")
        body = (
            MultipartBuilder()
            .file("file", self.file)
            .to_body()
        )
        return HTTPRequestOptions(body=body)
