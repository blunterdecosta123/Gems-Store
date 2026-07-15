from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from enum import Enum as Enum_,IntEnum
from models.user_models import User

class Enum(Enum_):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
class GemClarity(IntEnum):
    SI=1
    VS=2
    VVS=3
    FL=4

class GemColor(str, Enum):
    D='D'
    E='E'
    G='G'
    F='F'
    H='H'
    I='I'

class GemType(str, Enum):
    DIAMOND='DIAMOND'
    RUBY='RUBY'
    EMERALD='EMERALD'
    
class GemPropertiesCreate(SQLModel):
    size: float=Field(default=1)
    clarity: GemClarity=Field(default=GemClarity.SI)
    color: GemColor=Field(default=GemColor.D)

class GemCreate(SQLModel):
    availability: bool=Field(default=True)
    gem_type: GemType=Field(default=GemType.DIAMOND)

class GemPatch(SQLModel):
    availability: Optional[bool] = None
    gem_type: Optional[GemType] = None


class GemPropertiesPatch(SQLModel):
    size: Optional[float] = None
    clarity: Optional[GemClarity] = None
    color: Optional[GemColor] = None

class GemProperties(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    size: float = Field(default=1)
    clarity: Optional[GemClarity] = Field(default=GemClarity.SI)
    color: Optional[GemColor] = Field(default=GemColor.D)
    # queotes because Gem is not created till now it comes later
    gem: Optional['Gem'] = Relationship(back_populates="gem_properties")
    
    
class Gem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    price: float = Field(default=1000)
    availability: bool = Field(default=True)
    gem_type: GemType = Field(default=GemType.DIAMOND)
    gem_properties_id: Optional[int] = Field(default=None, foreign_key="gemproperties.id") #In the foreign key we are referencing the table not the Class which is lower case
    #relationship tells that if data changes in the GemProperties table then the data in Gem table should be updated
    gem_properties: Optional[GemProperties] = Relationship(back_populates="gem")
    seller_id: Optional[int] = Field(default=None, foreign_key="user.id")
    seller: Optional[User] = Relationship()