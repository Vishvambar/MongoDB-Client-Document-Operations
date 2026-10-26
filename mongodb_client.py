"""
MongoDB Collection Operations Service.
Implements the core document operations using a PyMongo Collection object:
- Inserting (insert_one, insert_many)
- Searching (find_one, find with filters, projections, sorting, regex)
- Updating (update_one, update_many with $set, $inc, $push, upsert)
- Replacing (replace_one)
- Removing (delete_one, delete_many)
- Aggregating (aggregate with $match, $group, $sort, $project, $unwind)
"""

from typing import List, Dict, Any, Optional, Tuple
from pymongo.collection import Collection
from pymongo.results import (
    InsertOneResult,
    InsertManyResult,
    UpdateResult,
    DeleteResult
)
from bson.objectid import ObjectId

from config import get_collection


class MongoOperationsService:
    """Encapsulates PyMongo Collection object methods for document management."""

    def __init__(self, collection: Optional[Collection] = None):
        self.collection: Collection = collection if collection is not None else get_collection()

    # =========================================================================
    # 1. INSERTING DOCUMENTS
    # =========================================================================
    def insert_single(self, document: Dict[str, Any]) -> str:
        """
        Inserts a single document into the collection.
        Returns the string representation of the generated/inserted _id.
        """
        result: InsertOneResult = self.collection.insert_one(document)
        return str(result.inserted_id)

    def insert_batch(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Inserts multiple documents into the collection in a single batch.
        Returns a list of string inserted IDs.
        """
        result: InsertManyResult = self.collection.insert_many(documents)
        return [str(_id) for _id in result.inserted_ids]

    # =========================================================================
    # 2. SEARCHING / QUERYING DOCUMENTS
    # =========================================================================
    def search_one(self, filter_query: Dict[str, Any], projection: Optional[Dict[str, int]] = None) -> Optional[Dict[str, Any]]:
        """
        Finds a single document matching criteria.
        """
        return self.collection.find_one(filter_query, projection)

    def search_many(
        self,
        filter_query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, int]] = None,
        sort_field: Optional[str] = None,
        sort_order: int = 1,  # 1 for ASC, -1 for DESC
        limit: int = 0,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Finds multiple documents matching criteria with projection, sorting, and pagination.
        """
        query = filter_query or {}
        cursor = self.collection.find(query, projection)
        
        if sort_field:
            cursor = cursor.sort(sort_field, sort_order)
        if skip > 0:
            cursor = cursor.skip(skip)
        if limit > 0:
            cursor = cursor.limit(limit)
            
        return list(cursor)

    def search_by_text_or_regex(self, field: str, pattern: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Searches documents using regular expressions on specified field.
        """
        options = "" if case_sensitive else "i"
        query = {field: {"$regex": pattern, "$options": options}}
        return list(self.collection.find(query))

    # =========================================================================
    # 3. UPDATING DOCUMENTS
    # =========================================================================
    def update_single(
        self,
        filter_query: Dict[str, Any],
        update_doc: Dict[str, Any],
        upsert: bool = False
    ) -> Tuple[int, int, Optional[str]]:
        """
        Updates a single matching document.
        Returns (matched_count, modified_count, upserted_id).
        """
        result: UpdateResult = self.collection.update_one(filter_query, update_doc, upsert=upsert)
        upserted_id = str(result.upserted_id) if result.upserted_id else None
        return (result.matched_count, result.modified_count, upserted_id)

    def update_batch(
        self,
        filter_query: Dict[str, Any],
        update_doc: Dict[str, Any]
    ) -> Tuple[int, int]:
        """
        Updates all documents matching the filter criteria.
        Returns (matched_count, modified_count).
        """
        result: UpdateResult = self.collection.update_many(filter_query, update_doc)
        return (result.matched_count, result.modified_count)

    # =========================================================================
    # 4. REPLACING DOCUMENTS
    # =========================================================================
    def replace_single(
        self,
        filter_query: Dict[str, Any],
        replacement_document: Dict[str, Any],
        upsert: bool = False
    ) -> Tuple[int, int, Optional[str]]:
        """
        Completely replaces a document with replacement_document, preserving _id.
        Returns (matched_count, modified_count, upserted_id).
        """
        result: UpdateResult = self.collection.replace_one(
            filter_query,
            replacement_document,
            upsert=upsert
        )
        upserted_id = str(result.upserted_id) if result.upserted_id else None
        return (result.matched_count, result.modified_count, upserted_id)

    # =========================================================================
    # 5. REMOVING / DELETING DOCUMENTS
    # =========================================================================
    def remove_single(self, filter_query: Dict[str, Any]) -> int:
        """
        Deletes a single document matching the filter query.
        Returns deleted_count (0 or 1).
        """
        result: DeleteResult = self.collection.delete_one(filter_query)
        return result.deleted_count

    def remove_batch(self, filter_query: Dict[str, Any]) -> int:
        """
        Deletes all documents matching the filter query.
        Returns deleted_count.
        """
        result: DeleteResult = self.collection.delete_many(filter_query)
        return result.deleted_count

    def drop_collection(self) -> None:
        """Drops the entire collection."""
        self.collection.drop()

    # =========================================================================
    # 6. AGGREGATING DOCUMENTS
    # =========================================================================
    def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Executes an aggregation pipeline ($match, $group, $sort, $project, etc.).
        Returns the list of resulting aggregated documents.
        """
        return list(self.collection.aggregate(pipeline))

    # Helper: count documents
    def count_documents(self, filter_query: Optional[Dict[str, Any]] = None) -> int:
        """Counts documents in the collection matching query."""
        return self.collection.count_documents(filter_query or {})
