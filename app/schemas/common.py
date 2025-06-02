from pydantic import BaseModel, Field, field_validator, ConfigDict

class PaginationParams(BaseModel):
    skip: int = Field(default=0, description="Number of items to skip for pagination", ge=0)
    limit: int = Field(default=10, description="Number of items to return for pagination", gt=0)

    @field_validator('skip', 'limit')
    @classmethod
    def validate_positive(cls, v, info):
        if v < 0:
            raise ValueError(f"{info.field_name} must be positive")
        return v

    model_config = ConfigDict(from_attributes=True)