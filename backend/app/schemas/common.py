from pydantic import BaseModel


class ModuleStatus(BaseModel):
    module: str
    implementation_status: str = "placeholder"
