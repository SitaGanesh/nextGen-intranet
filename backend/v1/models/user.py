from . import db, BaseModel, bcrypt
import re



class User(BaseModel):
    __tablename__ = "users"

    firstname = db.Column(db.String(36), nullable=False)
    lastname = db.Column(db.String(36), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    course = db.Column(db.Integer, db.ForeignKey('courses.id'))
    permission = db.Column(db.String(36))
    isVerified = db.Column(db.Boolean, default=False)

    # not neccessary
    phone = db.Column(db.String(15))
    start_date = db.Column(db.String(15))
    group = db.Column(db.Integer)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    isMaleGender = db.Column(db.Boolean)
    nin = db.Column(db.String(15))


    @staticmethod
    def validate_fields(required_fields, data):
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}
            elif type(data[field]) is str:
                if len(data[field]) < 1:
                    return {"error": f"field `{field}` cannot be empty"}
            
        return None

    def validate_password(self, pswd):
        errors = []

        # Check length
        if len(pswd) < 8:
            errors.append("Password must be at least 8 characters long.")

        # Check for at least one letter
        if not re.search(r"[A-Za-z]", pswd):
            errors.append("Password must contain at least one letter.")
        
        if not re.search(r"[A-Z]", pswd):
            errors.append("Password must contain at least Capital letter.")

        # Check for at least one digit
        if not re.search(r"\d", pswd):
            errors.append("Password must contain at least one number.")

        # Check for at least one special character
        if not re.search(r"[@$!%*#?&]", pswd):
            errors.append("Password must contain at least one special character.")

        if errors:
            return {"errors": errors}
        return None

    def hash_password(self, pswd):  
        return bcrypt.generate_password_hash(pswd)
    
    def check_password_hash(self, pswd):
        return bcrypt.check_password_hash(self.password, pswd)
