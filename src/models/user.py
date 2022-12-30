from peewee import Model, CharField



def buildUser(db):
    
    class BaseModel(Model):
        
        class Meta:
            database = db
            
    class User(BaseModel):
        
        username = CharField(max_length=100, unique=True)
        password = CharField()   
    
        
    db.create_tables([User])
    return User     