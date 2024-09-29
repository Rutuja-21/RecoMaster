from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
from model import recommend,output_recommended_recipes
import razorpay
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Load dataset
dataset = pd.read_csv('C:/RecoMaster/Data/food1.csv')
dataset.info()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

akey = os.getenv("APIKEY")
skey = os.getenv("SECRETKEY")

client = razorpay.Client(auth=(akey,skey))

class Params(BaseModel):
    n_neighbors: int = 5
    return_distance: bool = False

class PredictionIn(BaseModel):
    nutrition_input: List[float] = Field(..., min_items=9, max_items=9)
    ingredients: List[str] = []
    params: Optional[Params] = None

class Recipe(BaseModel):
    Name: str
    CookTime: str
    PrepTime: str
    TotalTime: str
    RecipeIngredientParts: List[str]
    Calories: float
    FatContent: float
    SaturatedFatContent: float
    CholesterolContent: float
    SodiumContent: float
    CarbohydrateContent: float
    FiberContent: float
    SugarContent: float
    ProteinContent: float
    RecipeInstructions: List[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None

class PaymentRequest(BaseModel):
    amount: int  # Amount in INR (e.g., 99 for ₹99)
    email: str
    contact: str
    
@app.get("/")
def home():
    return {"health_check": "OK"}

@app.post("/predict/", response_model=PredictionOut)
def update_item(prediction_input: PredictionIn):
    recommendation_dataframe = recommend(
        dataset, 
        prediction_input.nutrition_input, 
        prediction_input.ingredients, 
        prediction_input.params.dict()
    )
    output = output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output": None}
    else:
        return {"output": output}

@app.post("/create_payment_link/")
def create_payment_link(payment: PaymentRequest):
    try:
        # Convert amount to paise (₹1 = 100 paise)
        amount_in_paise = payment.amount * 100

        # Razorpay Payment Link API call
        response = client.payment_link.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "accept_partial": False,
            "description": "RecoMaster Subscription",
            "customer": {
                "email": payment.email,
                "contact": payment.contact
            },
            "notify": {
                "sms": True,
                "email": True
            },
            "reminder_enable": True,
            "callback_url": "http://localhost:8080/payment_success",
            "callback_method": "get"
        })

        # Log or return the response for debugging
        logging.info(f"Payment link creation response: {response}")
        return {"payment_link": response['short_url']}
    
    except Exception as e:
        # Log the error to understand what's going wrong
        logging.error(f"Error while creating payment link: {str(e)}")
        return {"error": str(e)}

# If running directly, include the following line to start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)

