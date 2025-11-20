import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Reservation, Message

app = FastAPI(title="Cafe & Bar API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"name": "Cafe & Bar API", "status": "ok"}

@app.get("/api/menu")
def get_menu():
    """Static menu items for now. Can be moved to DB later."""
    return {
        "drinks": [
            {"name": "Espresso", "price": 3.0, "desc": "Rich and bold single shot"},
            {"name": "Cappuccino", "price": 4.5, "desc": "Espresso, steamed milk, foam"},
            {"name": "Latte", "price": 4.5, "desc": "Creamy espresso and milk"},
            {"name": "Iced Coffee", "price": 4.0, "desc": "Cold brewed, smooth finish"},
            {"name": "Old Fashioned", "price": 9.0, "desc": "Whiskey, bitters, sugar"},
            {"name": "Mojito", "price": 8.5, "desc": "Rum, mint, lime, soda"},
        ],
        "bites": [
            {"name": "Avocado Toast", "price": 7.5, "desc": "Sourdough, smashed avo, seeds"},
            {"name": "Club Sandwich", "price": 9.5, "desc": "Turkey, bacon, tomato, mayo"},
            {"name": "Cheese Platter", "price": 12.0, "desc": "Assorted cheeses & crackers"},
        ],
    }

@app.post("/api/reservations")
def create_reservation(payload: Reservation):
    try:
        reservation_id = create_document("reservation", payload)
        return {"ok": True, "id": reservation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reservations")
def list_reservations(limit: int = 50):
    try:
        docs = get_documents("reservation", limit=limit)
        # Make ObjectId json-friendly if needed
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def send_message(payload: Message):
    try:
        msg_id = create_document("message", payload)
        return {"ok": True, "id": msg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
