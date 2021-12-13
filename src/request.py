from typing import Optional

from pydantic import BaseModel


class KeyGenerationRequest(BaseModel):
    with_private_key: Optional[bool] = False
