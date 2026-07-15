from db.db import engine
from sqlmodel import Session,select,or_
from models.gem_models import *
#or_ is used to combine the conditions as OR
def select_all_gems():
    with Session(engine) as session:
        statements=select(Gem,GemProperties).join(GemProperties)
        # statements=statements.where(or_(Gem.id==1,Gem.id==2,Gem.id==3))
        result=session.exec(statements)
        return [{"gem": gem, "properties": properties}for gem, properties in result.all()]
    
def select_gems(id):
    with Session(engine) as session:
        #statements=select(Gem,GemProperties).where(Gem.gem_properties_id==GemProperties.id)
        statements=select(Gem,GemProperties).join(GemProperties)
        statements=statements.where(Gem.id==id)
        result=session.exec(statements)
        row=result.first()
        gem,properties=row
        if len(row)==0:
            return None
        return [{"gem": gem, "properties": properties}]
    