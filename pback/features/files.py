from io import BytesIO
from typing import Literal, Optional

from fastapi import Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session  # type: ignore

import crud
import db
import models
from features import users


def get_file(
    file_name: str,
    s: Session = Depends(db.get_session),
    # current_user: Optional[models.User] = Depends(users.get_current_user_or_none),
) -> StreamingResponse:
    f = crud.read_file(s, int(file_name))
    assert f is not None
    # print("File id:", f.file_id)
    b = f.file
    bytes_io = BytesIO()
    bytes_io.write(b)
    bytes_io.seek(0)
    r = StreamingResponse(bytes_io, media_type=f.content_type)
    return r


def create_file(
    file: UploadFile = File(...),
    s: Session = Depends(db.get_session),
    current_user: Optional[models.User] = Depends(users.get_current_user_or_none),
) -> dict[Literal["file_id"], int]:
    # TODO check user
    db_file_id = crud.load_file(s, file, 5)
    return {"file_id": db_file_id}
