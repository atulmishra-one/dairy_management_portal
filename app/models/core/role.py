from app.services.extension import sqlalchemy as db

class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    allowed_funcs = db.Column(db.Text)
    disallowed_funcs = db.Column(db.Text)
    
    def __str__(self):
        return '%s' % self.name
    
    @staticmethod
    def create_or_update(name, allowed_funcs, disallowed_funcs):
        try:
            role_exists = Role.query.filter(Role.name==name).first()
            if role_exists:
                role_exists.name = name
                role_exists.allowed_funcs = allowed_funcs
                role_exists.disallowed_funcs = disallowed_funcs
                db.session.add(role_exists)
            else:
                db.session.add_all([
                    Role(
                        name=name,
                        allowed_funcs=allowed_funcs,
                        disallowed_funcs=disallowed_funcs
                    )
                ])
            db.session.commit()
            return True
        except TypeError:
            return False