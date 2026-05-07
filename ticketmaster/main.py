from fastapi import FastAPI, HTTPException
import time
import datetime as dt

app = FastAPI()

Inventory={"seat_1A":{"price":2000,"locked_by":None,"sold":False,"locked_until":None},"seat_1B":{"price":2000,"locked_by":None,"sold":False,"locked_until":None},"seat_1C":{"price":2000,"locked_by":None,"sold":False,"locked_until":None}}

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/reserve/{item_id}")
def reserve_item(item_id: str, current_user: str):
    now = time.time()
    if item_id not in Inventory:
        raise HTTPException(status_code=404, detail="item not found")
    if(Inventory[item_id]["sold"]==True):
        raise HTTPException(status_code=400, detail="already sold")
    elif(Inventory[item_id]["locked_by"] != current_user and Inventory[item_id]["locked_by"] != None and Inventory[item_id]["locked_until"] > now):
        raise HTTPException(status_code=400, detail="already locked by someone")
    else:
        Inventory[item_id]["locked_by"] = current_user
        Inventory[item_id]["locked_until"] = now+60
        return {"message": "reserved", "item_id": item_id, "locked_until": Inventory[item_id]["locked_until"]}


@app.post("/purchase/{item_id}")
def purchase_item(item_id: str, current_user: str):
    now = time.time()
    if item_id not in Inventory:
        raise HTTPException(status_code=404, detail="item not found")
    if(Inventory[item_id]["sold"]==True):
        raise HTTPException(status_code=400, detail="already sold")
        Inventory[item_id]["locked_by"] = None
        Inventory[item_id]["locked_until"] = None
    elif(Inventory[item_id]["locked_by"] != current_user):
        raise HTTPException(status_code=400, detail="you must reserve the item first")
    elif(Inventory[item_id]["locked_until"] < now):
        raise HTTPException(status_code=400, detail="your reservation has expired")
    else:
        Inventory[item_id]["sold"] = True
        return {"message": "purchased", "item_id": item_id, "price": Inventory[item_id]["price"]}
    

        

    
