from typing import Optional, List
from pydantic import BaseModel

# --- 请求模型定义 ---
class COCOMORequest(BaseModel):
    loc: float
    mode: Optional[str] = "organic"

class FunctionPointRequest(BaseModel):
    external_inputs: int
    external_outputs: int
    external_inquiries: int
    internal_files: int
    external_interfaces: int

class ExpertRequest(BaseModel):
    estimates: List[float]
