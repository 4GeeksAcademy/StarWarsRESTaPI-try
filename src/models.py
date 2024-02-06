from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(35), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    favorite = db.relationship("Favorites") # uniendo las dos tablas
    
    def __repr__(self):
                # nombre de la clase
        return '<Character %r>' % self.name

    def serialize(self): #serialize todos los datos de la tabla menos el passowrd, datos que quiero mostrar
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    favorite = db.relationship("Favorites") #estamos uniendo las 2 tablas 

    def __repr__(self):
                # nombre de la clase
        return '<Character %r>' % self.name

    def serialize(self): #serialize todos los datos de la tabla menos el passowrd
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String)
    favorite = db.relationship('Favorites')

    def __repr__(self):
        return'<Character %r>' % self.name
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
class Favorites(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    def __repr__(self):
                # nombre de la clase
        return '<Favorites %r>' % self.id
    
    def serialize(self): #serialize todos los datos de la tabla menos el passowrd
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }