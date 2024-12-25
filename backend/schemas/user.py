from pydantic import BaseModel, Field, field_validator, EmailStr

class UserModel(BaseModel):
    username: str = Field(..., description="Username of user")
    password: str = Field(..., min_length=8, description="Password of user")
    email: EmailStr = Field(..., description="Email of user")

    @field_validator("password")
    @classmethod
    def check_password(cls,value):
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        
        if not any(char in "!@#$%^&*()-_+=<>?/\\|[]{}~" for char in value):
            raise ValueError("Password must contain at least one special character")
        
        return value
    

class LoginModel(UserModel):
    email: EmailStr = Field(..., description="Email of user")
    password: str = Field(..., min_length=8, description="Password of user")
