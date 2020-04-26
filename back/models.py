from app import db


class Repo(db.Model):
    __tablename__ = 'repos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lang = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('repos', lazy=True))

    def __init__(self, name, lang, description, user_id):
        self.name = name
        self.lang = lang
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return f'<repo: {self.id}>'

    def serialize(self):
        return {
            'name': self.name,
            'lang': self.lang,
            'description': self.description,
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    link = db.Column(db.String(), unique=True, nullable=False)

    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return f'<user: {self.id}>'

    def serialize(self):
        return {'name': self.name, 'link': self.link}
