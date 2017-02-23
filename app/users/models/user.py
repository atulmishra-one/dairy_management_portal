
from app.services.extension import db


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    initial_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __str__(self):
        return '%s' % self.username
    
    def fullname(self):
        return '%s %s %s' % (self.initial_name, self.first_name, self.last_name)
    
    def get_id(self):
        return self.id
    
    def is_active(self):
        return self.active
    
    def is_authenticated(self):
        return self.authenticated


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                      )

