from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, user_data):
        self.id = user_data.get("id")
        self.username = user_data.get("username")
        self.password = user_data.get("password")
        self.email = user_data.get("email")

    
    def is_active(self) -> bool:
        return True
    def is_authenticated(self) -> bool:
        return True
    def is_anonymous(self)->bool:
        return False
    def get_id(self)->str:
        return f"{self.id}"