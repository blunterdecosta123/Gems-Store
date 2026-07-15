from sqlalchemy import create_engine
from fastapi import APIRouter,HTTPException,Depends, Query
from populate import calculate_gem_price
from models.gem_models import *
from repos import gem_repository
from db.db import session
from auth.auth import AuthHandler
from fastapi.responses import JSONResponse
from sqlmodel import select
from typing import List,Dict,Union
auth_handler=AuthHandler()
# gem_router=APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)]) if we want to restrict everything

gem_router=APIRouter()
@gem_router.get("/gems",tags=["Gems"])
def gems(lte:Optional[int]=None,gte:Optional[int]=None,type:List[GemType]=Query(default=None)):
    gems=select(Gem,GemProperties).join(GemProperties)
    if gems is None:
        raise HTTPException(status_code=404, detail="Gems not found")
    if lte is not None:
        gems=gems.where(Gem.price<=lte)
    if gte is not None:
        gems=gems.where(Gem.price>=gte)
    if type:
        gems=gems.where(Gem.gem_type.in_(type)).order_by(Gem.gem_type).order_by(-Gem.price)
    gems=session.exec(gems).all()
    return {"gems":[{"gem": gem, "properties": properties}for gem, properties in gems]}

@gem_router.get('/gem/{id}',tags=["Gems"])
def gem(id:int):
    gem=session.get(Gem,id)
    if gem is None:
        raise HTTPException(status_code=404, detail="Gem not found")
    properties = session.get(GemProperties, gem.gem_properties_id)
    return {"gem": gem, "properties": properties}

@gem_router.post("/gems",tags=["Gems"])
def create_gem(gem_pr: GemPropertiesCreate, gem: GemCreate,user=Depends(auth_handler.get_current_user)): #depends is used for dependency injection
    if not user.is_seller:
        return JSONResponse(status_code=401,content={"message":"You are not a seller"})
    gem_properties=GemProperties(size=gem_pr.size,clarity=gem_pr.clarity,color=gem_pr.color)
    session.add(gem_properties)
    session.commit()
    gem_=Gem(availability=gem.availability,gem_type=gem.gem_type,gem_properties_id=gem_properties.id,seller_id=user.id,seller=user)
    price=calculate_gem_price(gem_,gem_properties)
    gem_.price=price
    session.add(gem_)
    session.commit()
    session.refresh(gem_)
    session.refresh(gem_properties)
    return {
        "gem": gem_,
        "properties": gem_properties
    }

@gem_router.put("/gems/{id}",tags=["Gems"])
def update_gem(id: int, gem: GemCreate, gem_pr: GemPropertiesCreate,user=Depends(auth_handler.get_current_user)):
    gem_found = session.get(Gem, id)

    if gem_found is None:
        raise HTTPException(status_code=404, detail="Gem not found")
    
    if not user.is_seller or user.id!=gem_found.seller_id:
        return JSONResponse(status_code=401,content={"message":"Unauthorized"})
    gem_properties = session.get(GemProperties, gem_found.gem_properties_id)

    for key, value in gem.model_dump().items():
        setattr(gem_found, key, value)

    for key, value in gem_pr.model_dump().items():
        setattr(gem_properties, key, value)
    
    gem_found.price = calculate_gem_price(gem_found, gem_properties)

    session.add(gem_properties)
    session.add(gem_found)
    session.commit()
    session.refresh(gem_found)
    session.refresh(gem_properties)
    
    return {
        "gem": gem_found,
        "properties": gem_properties
    }
    
@gem_router.patch("/gems/{id}",tags=["Gems"])
def partial_update_gem(id: int, gem: GemPatch, gem_pr: GemPropertiesPatch,user=Depends(auth_handler.get_current_user)):
    gem_found = session.get(Gem, id)

    if gem_found is None:
        raise HTTPException(status_code=404, detail="Gem not found")
    
    if not user.is_seller or user.id!=gem_found.seller_id:
        return JSONResponse(status_code=401,content={"message":"Unauthorized"})
    
    gem_properties = session.get(GemProperties, gem_found.gem_properties_id)

    for key, value in gem.model_dump(exclude_unset=True).items():
        setattr(gem_found, key, value)

    for key, value in gem_pr.model_dump(exclude_unset=True).items():
        setattr(gem_properties, key, value)
    
    gem_found.price = calculate_gem_price(gem_found, gem_properties)

    session.add(gem_properties)
    session.add(gem_found)
    session.commit()
    session.refresh(gem_found)
    session.refresh(gem_properties)
    
    return {
        "gem": gem_found,
        "properties": gem_properties
    }
    
@gem_router.delete("/gems/{id}",tags=["Gems"])
def delete_gem(id: int,user=Depends(auth_handler.get_current_user)):
    gem_found = session.get(Gem, id)

    if gem_found is None:
        raise HTTPException(status_code=404, detail="Gem not found")
    
    if not user.is_seller or user.id!=gem_found.seller_id:
        return JSONResponse(status_code=401,content={"message":"Unauthorized"})
    
    gem_properties = session.get(GemProperties, gem_found.gem_properties_id)
    session.delete(gem_found)
    session.delete(gem_properties)
    session.commit()    
    return {"message": "Gem along with properties deleted successfully"}

@gem_router.get("/gems/seller/me",tags=["seller"],response_model=List[Dict[str,Union[Gem,GemProperties]]])
def gems_selleer(user=Depends(auth_handler.get_current_user)):
    if not user.is_seller:
        return JSONResponse(status_code=401,content={"message":"Unauthorized"})
    statements=select(Gem,GemProperties).join(GemProperties).where(Gem.seller_id==user.id)
    gems=session.exec(statements).all()
    return [{"gem": gem, "properties": properties}for gem, properties in gems]