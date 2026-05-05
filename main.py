from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app=FastAPI()

@app.get('/')
def home():
    return {'message':'hello world'}

@app.get('/health')
def health():
    return {'status':'healthy'}

balances={
    "user1":1000,
    "user2":2000
}

processed_transactions={}

class TransferRequest(BaseModel):
    user_id:str
    amount:float
    transaction_id:str

@app.post('/transfer')
def transfer(request: TransferRequest):

    if request.transaction_id in processed_transactions:
        return {'message': 'Transaction already processed', 'status': 'success'}

    if request.user_id not in balances:
        raise HTTPException(status_code=404, detail="User not found")

    if balances[request.user_id] < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    

    balances[request.user_id] -= request.amount
    processed_transactions[request.transaction_id] = True
    
    return {
        'message': 'Transfer successful', 
        'remaining_balance': balances[request.user_id]
    }

@app.get('/balance')
def get_balance(user_id: str):
    if user_id not in balances:
        raise HTTPException(status_code=404, detail="User not found")
    return {"balance": balances[user_id]}

    