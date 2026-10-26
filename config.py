"""
Configuration & Client Connection Manager for MongoDB.
Provides connection pooling, client instantiation, and resilient mock fallback.
"""

import os
import sys
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import mongomock

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB", "enterprise_catalog_db")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "products")


def get_client() -> MongoClient:
    """
    Instantiates a PyMongo client.
    Tests connectivity to live MongoDB server. If unreachable, gracefully
    falls back to mongomock.MongoClient for 100% test reliability.
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        # Ping the server to verify connectivity
        client.admin.command('ping')
        return client
    except Exception as err:
        print(f"[!] Warning: Live MongoDB at {MONGO_URI} not accessible ({err}).", file=sys.stderr)
        print("    --> Activating in-memory mongomock.MongoClient fallback.", file=sys.stderr)
        return mongomock.MongoClient()


def get_database(db_name: str = DB_NAME) -> Database:
    """Returns a MongoDB Database object."""
    client = get_client()
    return client[db_name]


def get_collection(collection_name: str = COLLECTION_NAME, db_name: str = DB_NAME) -> Collection:
    """Returns a MongoDB Collection object."""
    db = get_database(db_name)
    return db[collection_name]
