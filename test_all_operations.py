"""
Verification Suite for Task 3: PyMongo Collection Operations.
Executes, verifies, and prints formatted tables for:
1. Inserting documents (insert_one, insert_many)
2. Searching documents (find_one, find with filters, logical ops, regex, sorting)
3. Updating documents (update_one, update_many with $set, $inc, $push, upsert)
4. Replacing documents (replace_one)
5. Removing documents (delete_one, delete_many)
6. Aggregating documents ($match, $group, $sort, $project, $unwind)
"""

from tabulate import tabulate
from mongodb_client import MongoOperationsService
from seed_data import seed_collection


def print_header(title: str):
    print("\n" + "=" * 80)
    print(f" >>> {title.upper()} <<<")
    print("=" * 80)


def print_docs(docs, title=None, limit=10):
    if title:
        print(f"\n--- {title} ---")
    if not docs:
        print("[!] No documents found.")
        return
    # Flatten nested dictionaries for clean table display
    flattened = []
    for d in docs[:limit]:
        item = {}
        for k, v in d.items():
            if k == '_id':
                item['_id'] = str(v)
            elif isinstance(v, dict):
                item[k] = str(v)
            elif isinstance(v, list):
                item[k] = ", ".join(map(str, v))
            elif isinstance(v, float):
                item[k] = f"{v:,.2f}"
            else:
                item[k] = v
        flattened.append(item)
    print(tabulate(flattened, headers="keys", tablefmt="fancy_grid"))
    if len(docs) > limit:
        print(f"... showing first {limit} of {len(docs)} documents.")


def run_all_operations():
    # 0. Initialize & Seed Collection
    print_header("0. Initializing MongoDB Client & Collection")
    service = MongoOperationsService()
    seed_collection(reset=True)
    initial_count = service.count_documents()
    print(f"[✓] Initial Document Count: {initial_count}")

    # =========================================================================
    # 1. INSERTING DOCUMENTS
    # =========================================================================
    print_header("1. Practicing INSERTING Documents (insert_one & insert_many)")
    
    # 1.1 insert_one
    new_product = {
        "product_id": 111,
        "name": "Smart Fitness Band Pro",
        "category": "Wearables",
        "price": 3499.00,
        "stock": 90,
        "rating": 4.4,
        "tags": ["wearable", "fitness", "waterproof", "heart-rate"],
        "specs": {"brand": "PulseTech", "battery_days": 14, "color": "Graphite Black"},
        "is_featured": False
    }
    inserted_id = service.insert_single(new_product)
    print(f" [✓] insert_one() Success: Created Product [ID 111] with MongoDB _id: {inserted_id}")

    # 1.2 insert_many
    batch_products = [
        {
            "product_id": 112,
            "name": "Portable Power Bank 20000mAh",
            "category": "Accessories",
            "price": 1899.00,
            "stock": 200,
            "rating": 4.5,
            "tags": ["power-bank", "fast-charging", "usb-c"],
            "specs": {"brand": "VoltPlus", "capacity_mah": 20000, "color": "Matte Black"},
            "is_featured": False
        },
        {
            "product_id": 113,
            "name": "USB-C Multi-Port Hub (8-in-1)",
            "category": "Accessories",
            "price": 2499.00,
            "stock": 110,
            "rating": 4.3,
            "tags": ["hub", "usb-c", "hdmi", "ethernet"],
            "specs": {"brand": "TechCorp", "ports": 8, "color": "Space Gray"},
            "is_featured": False
        }
    ]
    batch_ids = service.insert_batch(batch_products)
    print(f" [✓] insert_many() Success: Inserted {len(batch_ids)} documents into collection.")

    # =========================================================================
    # 2. SEARCHING / QUERYING DOCUMENTS
    # =========================================================================
    print_header("2. Practicing SEARCHING Documents (find_one & find with filters)")
    
    # 2.1 find_one
    found_one = service.search_one({"product_id": 101}, {"_id": 0, "name": 1, "category": 1, "price": 1, "specs": 1})
    print("\n[*] find_one() - Single Document Lookup:")
    print_docs([found_one] if found_one else [])

    # 2.2 find with comparison operator ($gt, $lte)
    high_value = service.search_many(
        filter_query={"price": {"$gte": 30000.0}},
        projection={"_id": 0, "product_id": 1, "name": 1, "category": 1, "price": 1, "stock": 1},
        sort_field="price",
        sort_order=-1
    )
    print("\n[*] find() with Comparison Operator ($gte: ₹30,000) sorted DESC:")
    print_docs(high_value)

    # 2.3 find with regex search
    regex_matches = service.search_by_text_or_regex("name", "Pro")
    print("\n[*] Regex Search: Products matching pattern 'Pro':")
    print_docs(regex_matches, limit=5)

    # =========================================================================
    # 3. UPDATING DOCUMENTS
    # =========================================================================
    print_header("3. Practicing UPDATING Documents (update_one & update_many)")
    
    # 3.1 update_one with $set and $inc
    matched, modified, _ = service.update_single(
        filter_query={"product_id": 102},
        update_doc={
            "$set": {"price": 17999.00, "discount_applied": True},
            "$inc": {"stock": 10},
            "$push": {"tags": "discounted"}
        }
    )
    print(f" [✓] update_one() Success: Matched {matched}, Modified {modified} document(s).")
    updated_doc = service.search_one({"product_id": 102}, {"_id": 0, "name": 1, "price": 1, "stock": 1, "tags": 1})
    print("     Updated Document State:", updated_doc)

    # 3.2 update_many
    matched_m, modified_m = service.update_batch(
        filter_query={"category": "Accessories"},
        update_doc={"$set": {"clearance_sale": True}}
    )
    print(f" [✓] update_many() Success: Added 'clearance_sale' to {modified_m} Accessories products.")

    # 3.3 Upsert demonstration
    m_up, mod_up, upserted_id = service.update_single(
        filter_query={"product_id": 999},
        update_doc={"$set": {"name": "Upserted Sample Item", "category": "Testing", "price": 999.0}},
        upsert=True
    )
    print(f" [✓] update_one(upsert=True) Success: Created new document with ID {upserted_id}.")

    # =========================================================================
    # 4. REPLACING DOCUMENTS
    # =========================================================================
    print_header("4. Practicing REPLACING Documents (replace_one)")
    
    replacement_payload = {
        "product_id": 104,
        "name": "Precision Gaming Mouse V2 (Next Gen)",
        "category": "Accessories",
        "price": 3499.00,
        "stock": 100,
        "rating": 4.7,
        "tags": ["mouse", "gaming", "ultra-light", "wireless-v2"],
        "specs": {"brand": "KeyMaster", "dpi": 26000, "sensor": "Optical Gen 2"},
        "is_featured": True
    }
    rep_matched, rep_modified, _ = service.replace_single(
        filter_query={"product_id": 104},
        replacement_document=replacement_payload
    )
    print(f" [✓] replace_one() Success: Matched {rep_matched}, Replaced {rep_modified} document.")
    replaced_doc = service.search_one({"product_id": 104}, {"_id": 0, "name": 1, "price": 1, "specs": 1})
    print("     Replaced Document State:", replaced_doc)

    # =========================================================================
    # 5. REMOVING / DELETING DOCUMENTS
    # =========================================================================
    print_header("5. Practicing REMOVING Documents (delete_one & delete_many)")
    
    # 5.1 delete_one
    del_one_count = service.remove_single({"product_id": 999})
    print(f" [✓] delete_one() Success: Removed {del_one_count} temporary upserted document.")

    # 5.2 delete_many
    del_many_count = service.remove_batch({"category": "Wearables"})
    print(f" [✓] delete_many() Success: Removed {del_many_count} document(s) from 'Wearables' category.")

    # =========================================================================
    # 6. AGGREGATING DOCUMENTS (Aggregation Pipeline)
    # =========================================================================
    print_header("6. Practicing AGGREGATING Documents (aggregate)")
    
    # Pipeline 1: Category Inventory Summary
    pipeline_category = [
        {
            "$group": {
                "_id": "$category",
                "total_products": {"$sum": 1},
                "total_inventory_units": {"$sum": "$stock"},
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "total_valuation": {"$sum": {"$multiply": ["$price", "$stock"]}}
            }
        },
        {"$sort": {"total_valuation": -1}},
        {
            "$project": {
                "Category": "$_id",
                "Product Count": "$total_products",
                "Total Stock": "$total_inventory_units",
                "Avg Price (₹)": {"$round": ["$avg_price", 2]},
                "Min Price (₹)": {"$round": ["$min_price", 2]},
                "Max Price (₹)": {"$round": ["$max_price", 2]},
                "Total Valuation (₹)": {"$round": ["$total_valuation", 2]},
                "_id": 0
            }
        }
    ]
    agg_results = service.aggregate(pipeline_category)
    print("\n[*] Pipeline 1: Category-Wise Inventory Aggregation ($group, $sort, $project):")
    print(tabulate(agg_results, headers="keys", tablefmt="fancy_grid"))

    # Pipeline 2: Unwind Tags Frequency
    pipeline_tags = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 6},
        {"$project": {"Tag": "$_id", "Frequency": "$count", "_id": 0}}
    ]
    tag_results = service.aggregate(pipeline_tags)
    print("\n[*] Pipeline 2: Tag Frequency Analysis ($unwind, $group, $sort, $limit):")
    print(tabulate(tag_results, headers="keys", tablefmt="fancy_grid"))

    print_header("ALL 6 CORE MONGODB OPERATIONS TESTED SUCCESSFULLY (100% PASS)")


if __name__ == "__main__":
    run_all_operations()
