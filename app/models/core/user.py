from collections import defaultdict
from app.services.extension import sqlalchemy as db
from .role import Role

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
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    
    
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
    
    def create(self, context):
        db.session.add_all([
                User(
                    initial_name=row.get('initial_name', ''), 
                    first_name=row.get('first_name', ''),
                    last_name=row.get('last_name', ''),
                    username=row['username'],
                    password=row['password'],
                    email=row['email'],
                    active=row.get('active', 0),
                    role_id=row.get('role_id', 2)
                ) 
                for row in context
            ])
        db.session.commit()
        return 
    
    def create_or_update(self, context):
        
        users = defaultdict(list)
        for row in context:
            users[row['username']].append(row)
        
        users_that_exists = [user.username for user in User.query.filter(User.username.in_(users.keys())).all()]
        
        users_that_does_not_exists = set(users.keys()) - set(users_that_exists)
        
        if users_that_exists:
            exists_context = []
            for row in users_that_exists:
                exists_context.append(users[row][0])
            
            for ec in exists_context:
                user = User.query.filter_by(username=ec['username']).first()
                user.initial_name = ec.get('initial_name', '')
                user.first_name = ec.get('first_name', '')
                user.last_name = ec.get('last_name', '')
                user.password = ec.get('password', '')
                user.active = ec.get('active', 0)
                user.role_id= ec.get('role_id', 2)
                db.session.add(user)
            db.session.commit()
        if users_that_does_not_exists:
            new_context = []
            for _user in users_that_does_not_exists:
                new_context.append(users[_user][0])
                
            db.session.add_all([
                User(
                    initial_name=row.get('initial_name', ''), 
                    first_name=row.get('first_name', ''),
                    last_name=row.get('last_name', ''),
                    username=row['username'],
                    password=row['password'],
                    email=row['email'],
                    active=row.get('active', 0),
                    role_id=row.get('role_id', 2)
                ) 
                for row in new_context
            ])
            db.session.commit()
        return
    
    def delete_user(self, username):
        deleted = User.query.filter(User.username==username, User.username!='admin').delete()
        if deleted:
            db.session.commit()
            return True
        return False

        
