import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, ReturnDocument

load_dotenv()

_client = None
_db = None

def _get_client() -> MongoClient:
    global _client, _db
    if _client is None:
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        _db_name = os.getenv("MONGO_DB", "ai_complaint_agent")
        _db = _client[_db_name]
        _ensure_indexes()
    return _client

def _get_db():
    if _db is None:
        _get_client()
    return _db

def _ensure_indexes():
    db = _db
    db.interactions.create_index([("user_id", ASCENDING), ("created_at", ASCENDING)])
    db.interactions.create_index([("intent", ASCENDING)])
    db.kb.create_index([("slug", ASCENDING)], unique=True)

# ---------- Public API ----------

def save_interaction(user_id: str, message: str, intent: str, urgency: str, response: str, meta: Optional[Dict[str, Any]] = None) -> str:
    """Persist a single interaction."""
    _get_client()
    doc = {
        "user_id": user_id,
        "message": message,
        "intent": intent,
        "urgency": urgency,
        "response": response,
        "meta": meta or {},
        "created_at": datetime.utcnow(),
    }
    res = _db.interactions.insert_one(doc)
    return str(res.inserted_id)

def get_user_history(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    _get_client()
    cur = _db.interactions.find({"user_id": user_id}).sort("created_at", ASCENDING).limit(limit)
    return list(cur)

def upsert_kb_article(slug: str, question: str, answer: str, tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """Seed/maintain a lightweight KB now; you can upgrade to embeddings later."""
    _get_client()
    doc = {
        "slug": slug,
        "question": question,
        "answer": answer,
        "tags": tags or [],
        "updated_at": datetime.utcnow(),
    }
    return _db.kb.find_one_and_update(
        {"slug": slug},
        {"$set": doc, "$setOnInsert": {"created_at": datetime.utcnow()}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )

def find_kb_answer_by_tag(tag: str) -> List[Dict[str, Any]]:
    _get_client()
    return list(_db.kb.find({"tags": tag}).limit(5))
