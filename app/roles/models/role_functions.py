from app.services.extension import db


class RoleFunctions(db.Model):
    __tablename__ = 'role_functions'
    
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    roles = db.Column(db.Text)
