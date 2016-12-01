from app.services.extension import sqlalchemy as db

departments = db.Table('departments', 
                       db.Column('department_id', db.Integer, db.ForeignKey('department.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                      )


class Department(db.Model):
    __tablename__ = 'department'
    
    id = db.Column(db.Integer, primary_key=True)
    department_code = db.Column(db.String(64), unique=True)
    department_name = db.Column(db.String(64), unique=True)
    department_description = db.Column(db.Text)
    