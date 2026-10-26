"""
Interactive CLI for Task 3: MongoDB Collection Operations.
Allows interactive execution of:
- Insert (insert_one, insert_many)
- Search (find_one, find, regex, sorting)
- Update (update_one, update_many, upsert)
- Replace (replace_one)
- Remove (delete_one, delete_many)
- Aggregate (multi-stage pipelines)
"""

import sys
from tabulate import tabulate
from mongodb_client import MongoOperationsService
from seed_data import seed_collection
from test_all_operations import run_all_operations, print_docs
from visualize_mongodb import generate_all_visualizations


def clear_screen():
    print("\n" + "-" * 75)


def get_input(prompt: str, default: str = None) -> str:
    val = input(f"{prompt} " + (f"[{default}]: " if default else ": ")).strip()
    return val if val else (default if default is not None else "")


def handle_insert(service: MongoOperationsService):
    print("\n--- [1] INSERT DOCUMENT ---")
    try:
        pid = int(get_input("Product ID (integer)"))
        name = get_input("Product Name")
        cat = get_input("Category", "Electronics")
        price = float(get_input("Price (₹)"))
        stock = int(get_input("Stock Units", "50"))
        rating = float(get_input("Rating (0.0 - 5.0)", "4.5"))
        tags_raw = get_input("Comma-separated tags", "tech, gadgets")
        tags = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]

        doc = {
            "product_id": pid,
            "name": name,
            "category": cat,
            "price": price,
            "stock": stock,
            "rating": rating,
            "tags": tags,
            "specs": {"brand": "Generic", "color": "Black"},
            "is_featured": False
        }
        inserted_id = service.insert_single(doc)
        print(f"[✓] insert_one() Success! Document inserted with _id: {inserted_id}")
    except Exception as e:
        print(f"[✗] Error inserting document: {e}")


def handle_search(service: MongoOperationsService):
    print("\n--- [2] SEARCH DOCUMENTS ---")
    print("  [a] Search by Product ID (find_one)")
    print("  [b] Search by Category (find)")
    print("  [c] Search by Price Range ($gte / $lte)")
    print("  [d] Search by Name Pattern (Regex)")
    sub = get_input("Select search type (a-d)", "a").lower()

    if sub == "a":
        try:
            pid = int(get_input("Enter Product ID"))
            doc = service.search_one({"product_id": pid})
            print_docs([doc] if doc else [], title=f"PRODUCT ID {pid}")
        except ValueError:
            print("[!] Invalid integer ID.")
    elif sub == "b":
        cat = get_input("Enter Category Name (e.g. Computing, Audio, Accessories)")
        docs = service.search_many({"category": {"$regex": f"^{cat}$", "$options": "i"}})
        print_docs(docs, title=f"CATEGORY: {cat}")
    elif sub == "c":
        try:
            min_p = float(get_input("Minimum Price (₹)", "0"))
            max_p = float(get_input("Maximum Price (₹)", "1000000"))
            docs = service.search_many(
                {"price": {"$gte": min_p, "$lte": max_p}},
                sort_field="price",
                sort_order=1
            )
            print_docs(docs, title=f"PRODUCTS PRICED ₹{min_p:,.2f} - ₹{max_p:,.2f}")
        except ValueError:
            print("[!] Invalid price input.")
    elif sub == "d":
        pattern = get_input("Enter search text keyword")
        docs = service.search_by_text_or_regex("name", pattern)
        print_docs(docs, title=f"SEARCH RESULTS FOR '{pattern}'")


def handle_update(service: MongoOperationsService):
    print("\n--- [3] UPDATE DOCUMENTS ---")
    try:
        pid = int(get_input("Enter Product ID to update"))
        existing = service.search_one({"product_id": pid})
        if not existing:
            print(f"[!] Product ID {pid} not found.")
            return

        print(f"Current Name: {existing['name']} | Price: ₹{existing['price']:,.2f} | Stock: {existing['stock']}")
        new_price = get_input("New Price (₹) [Leave blank to keep current]", "")
        stock_delta = get_input("Stock Increment (+/- integer) [Leave blank for 0]", "")

        update_ops = {}
        if new_price:
            update_ops.setdefault("$set", {})["price"] = float(new_price)
        if stock_delta and int(stock_delta) != 0:
            update_ops.setdefault("$inc", {})["stock"] = int(stock_delta)

        if not update_ops:
            print("[-] No updates specified.")
            return

        m, mod, _ = service.update_single({"product_id": pid}, update_ops)
        print(f"[✓] update_one() Success: Matched {m}, Modified {mod} document(s).")
    except Exception as e:
        print(f"[✗] Update failed: {e}")


def handle_replace(service: MongoOperationsService):
    print("\n--- [4] REPLACE DOCUMENT ---")
    try:
        pid = int(get_input("Enter Product ID to replace completely"))
        existing = service.search_one({"product_id": pid})
        if not existing:
            print(f"[!] Product ID {pid} not found.")
            return

        print(f"Replacing document for: {existing['name']}")
        name = get_input("New Product Name")
        cat = get_input("New Category", existing["category"])
        price = float(get_input("New Price (₹)", str(existing["price"])))
        stock = int(get_input("New Stock", str(existing["stock"])))

        new_payload = {
            "product_id": pid,
            "name": name,
            "category": cat,
            "price": price,
            "stock": stock,
            "rating": existing.get("rating", 4.0),
            "tags": ["replaced", "updated"],
            "specs": {"replaced": True}
        }
        m, mod, _ = service.replace_single({"product_id": pid}, new_payload)
        print(f"[✓] replace_one() Success: Matched {m}, Replaced {mod} document.")
    except Exception as e:
        print(f"[✗] Replacement failed: {e}")


def handle_remove(service: MongoOperationsService):
    print("\n--- [5] REMOVE / DELETE DOCUMENT ---")
    try:
        pid = int(get_input("Enter Product ID to remove"))
        doc = service.search_one({"product_id": pid})
        if not doc:
            print(f"[!] Product ID {pid} not found.")
            return

        confirm = get_input(f"Are you sure you want to remove '{doc['name']}'? (y/N)", "N")
        if confirm.lower() == 'y':
            deleted = service.remove_single({"product_id": pid})
            print(f"[✓] delete_one() Success: Deleted {deleted} document.")
        else:
            print("[-] Removal cancelled.")
    except Exception as e:
        print(f"[✗] Delete failed: {e}")


def handle_aggregate(service: MongoOperationsService):
    print("\n--- [6] AGGREGATE DOCUMENTS ---")
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "total_items": {"$sum": 1},
                "total_units": {"$sum": "$stock"},
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "valuation": {"$sum": {"$multiply": ["$price", "$stock"]}}
            }
        },
        {"$sort": {"valuation": -1}},
        {
            "$project": {
                "Category": "$_id",
                "Products": "$total_items",
                "Total Stock": "$total_units",
                "Avg Price (₹)": {"$round": ["$avg_price", 2]},
                "Min Price (₹)": {"$round": ["$min_price", 2]},
                "Max Price (₹)": {"$round": ["$max_price", 2]},
                "Inventory Valuation (₹)": {"$round": ["$valuation", 2]},
                "_id": 0
            }
        }
    ]
    results = service.aggregate(pipeline)
    print(tabulate(results, headers="keys", tablefmt="fancy_grid"))


def main():
    service = MongoOperationsService()
    clear_screen()
    print("=" * 75)
    print("   TASK 3: PYTHON MONGODB CLIENT & COLLECTION OPERATIONS (PYMONGO)")
    print("   Practicing: Insert | Search | Update | Replace | Remove | Aggregate")
    print("=" * 75)

    if service.count_documents() == 0:
        seed_collection(reset=False)

    while True:
        clear_screen()
        doc_count = service.count_documents()
        print(f"            === MONGODB OPERATIONS DASHBOARD ({doc_count} Documents) ===")
        print("  [1] Insert Document        (insert_one / insert_many)")
        print("  [2] Search Documents       (find_one / find, filters, regex, sort)")
        print("  [3] Update Document        (update_one with $set, $inc, $push)")
        print("  [4] Replace Document       (replace_one)")
        print("  [5] Remove Document        (delete_one / delete_many)")
        print("  [6] Aggregate Documents    (Multi-stage aggregation pipeline)")
        print("  [7] Run Test Suite         (Automated 100% verification pass)")
        print("  [8] Generate Visual Charts (Matplotlib & Seaborn analytics)")
        print("  [9] Reset & Seed Database  (Restore default 10 sample products)")
        print("  [0] Exit")
        print("-" * 75)

        choice = get_input("Select an option (0-9)")
        if choice == "0":
            print("\nExiting MongoDB Client System. Goodbye!\n")
            break
        elif choice == "1":
            handle_insert(service)
            input("\nPress Enter to continue...")
        elif choice == "2":
            handle_search(service)
            input("\nPress Enter to continue...")
        elif choice == "3":
            handle_update(service)
            input("\nPress Enter to continue...")
        elif choice == "4":
            handle_replace(service)
            input("\nPress Enter to continue...")
        elif choice == "5":
            handle_remove(service)
            input("\nPress Enter to continue...")
        elif choice == "6":
            handle_aggregate(service)
            input("\nPress Enter to continue...")
        elif choice == "7":
            run_all_operations()
            input("\nPress Enter to continue...")
        elif choice == "8":
            charts = generate_all_visualizations()
            print(f"\n[✓] Generated {len(charts)} chart figures in visualizations/ folder.")
            input("\nPress Enter to continue...")
        elif choice == "9":
            seed_collection(reset=True)
            input("\nPress Enter to continue...")
        else:
            print("[!] Invalid option. Please enter 0 to 9.")


if __name__ == "__main__":
    main()
