from peewee import Model, CharField


def buildItem(self, db):

    class BaseModel(Model):
        class Meta:
            database = db

    class Item(BaseModel):

        name = CharField(max_length=100, unique=True)

    db.create_tables([Item])
    return Item
