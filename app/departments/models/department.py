from app.services.extension import db


class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(255))


department_roles = db.Table('department_roles',
                            db.Column('department_id', db.Integer, db.ForeignKey('department.id')),
                            db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                            )
