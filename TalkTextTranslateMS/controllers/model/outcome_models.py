from typing import Optional
from pydantic import BaseModel

    
class ContextResponseModel(BaseModel):
    content:Optional[str]