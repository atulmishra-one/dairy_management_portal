from app.services.extension import sqlalchemy as db

class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    
    def __str__(self):
        return '%s' % self.name