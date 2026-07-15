from models.gem_models import *
from sqlmodel import Session
from db.db import engine
import random


color_multiplier = {
    'D': 1.8,
    'E': 1.6,
    'G': 1.4,
    'F': 1.2,
    'H': 1,
    'I': 0.8
}

def calculate_gem_price(gem, gem_pr):
    price = 1000
    if gem.gem_type == 'Ruby':
        price = 400
    elif gem.gem_type == 'Emerald':
        price = 650

    if gem_pr.clarity == 1:
        price *= 0.75
    elif gem_pr.clarity == 3:
        price *= 1.25
    elif gem_pr.clarity == 4:
        price *= 1.5

    price = price * (gem_pr.size**3)

    if gem.gem_type == 'Diamond':
        multiplier = color_multiplier[gem_pr.color]
        price *= multiplier

    return price

def create_gem(gem_p):
    gem_type=random.choice(GemType.list())
    gem=Gem(price=100000,availability=True,gem_type=gem_type,gem_properties_id=gem_p.id)
    price=calculate_gem_price(gem,gem_p)
    price=round(price,2)
    gem.price=price
    return gem

def create_gem_properties():
    sz=random.randint(3,70)/10
    color=random.choice(GemColor.list())
    clarity=random.randint(1,4)
    gem_properties=GemProperties(size=sz,clarity=clarity,color=color)
    return gem_properties

def create_gems_db():
    gem_ps = [create_gem_properties() for x in range(100)]
    print(gem_ps)
    with Session(engine) as session:
        session.add_all(gem_ps)
        session.commit()
        gems = [create_gem(gem_ps[x]) for x in range(100)]
        # g = create_gem(gem_p.id)
        session.add_all(gems)
        session.commit()
        

if __name__ == "__main__":
    create_gems_db()