from app import db


class Repo(db.Model):
    __tablename__ = 'repos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    lang = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, name, lang, description):
        self.name = name
        self.lang = lang
        self.description = description

    def __repr__(self):
        return f'<id: {self.id}>'

    def serialize(self):
        return {
            'name': self.name,
            'lang': self.lang,
            'description': self.description,
        }
