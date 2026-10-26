# Python MongoDB Client & Document Operations (PyMongo)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-9.0%2B-47A248.svg?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![PyMongo](https://img.shields.io/badge/PyMongo-4.16%2B-green.svg)](https://pymongo.readthedocs.io/)
[![Status](https://img.shields.io/badge/Operations%20Verified-100%25-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)]()

> **Practical Experiment 3**: Create a Python-based MongoDB client using the `pymongo` module and, using a Collection object, practice foundational document operations: insert, search, remove, update, replace, and multi-stage aggregation pipelines.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Document Schema](#-document-schema)
- [Core Document Operations](#-core-document-operations)
- [Directory Structure](#-directory-structure)
- [Installation & Quick Start](#-installation--quick-start)
- [Multi-Stage Aggregation Pipelines](#-multi-stage-aggregation-pipelines)
- [Analytical Visualizations (300 DPI)](#-analytical-visualizations-300-dpi)
- [Reports & Documentation](#-reports--documentation)

---

## 🎯 Project Overview
This project implements a complete, production-grade **Python MongoDB Client** using the official `pymongo` driver. Operating on an e-commerce catalog Collection object (`products`), it demonstrates the complete lifecycle of document-oriented NoSQL engineering:
1. Client initialization, automated connection fallback (supporting local MongoDB and `mongomock` in-memory fallback), and database/collection instantiation.
2. Single and batch document insertion (`insert_one`, `insert_many`).
3. Rich query filters using comparison operators (`$gt`, `$lte`, `$in`), regex search, and projection masks.
4. In-place atomic field mutations using `$set`, `$inc`, and array modifications (`$push`), along with conditional `upsert=True`.
5. Full document replacement using `replace_one`.
6. Atomic document deletion (`delete_one`, `delete_many`).
7. Advanced multi-stage Aggregation Pipelines utilizing `$match`, `$unwind`, `$group`, `$sort`, and `$project`.
8. High-resolution visual analytics (300 DPI) depicting inventory stock values, pricing, and category performance.

---

## 📄 Document Schema

```json
{
  "_id": "ObjectId('671d4a9f1a2b3c4d5e6f7a8b')",
  "product_id": "PROD_1001",
  "name": "Wireless Noise Cancelling Headphones",
  "category": "Electronics",
  "price": 149.99,
  "stock_quantity": 45,
  "ratings": {
    "average": 4.6,
    "review_count": 128
  },
  "tags": ["audio", "wireless", "bluetooth", "accessories"],
  "supplier": {
    "name": "Apex Electronics Ltd",
    "contact": "sales@apexelectronics.com"
  },
  "status": "In Stock",
  "created_at": "2026-10-27T00:00:00Z"
}
```

---

## ⚡ Core Document Operations

| Operation Type | PyMongo API | Description & Syntax |
| :--- | :--- | :--- |
| **Insert** | `insert_one()`, `insert_many()` | Ingests single or batch BSON documents with auto-generated `_id` |
| **Search / Query** | `find()`, `find_one()` | Evaluates filter criteria (`price >= 100`, `$regex` on product names) |
| **Field Update** | `update_one()`, `update_many()` | Modifies fields atomically using `$set`, `$inc`, and `$push` |
| **Replace** | `replace_one()` | Replaces an entire document while preserving its original `_id` |
| **Delete** | `delete_one()`, `delete_many()` | Removes matched documents matching criteria (e.g., zero stock) |
| **Aggregation** | `aggregate()` | Multi-stage pipeline computing category analytics and unwinding tags |

---

## 📂 Directory Structure

```
MongoDB_Client_Document_Operations/
├── config.py                       # MongoDB connection URI & collection configuration
├── mongodb_client.py               # Core MongoDB client with all CRUD & aggregation operations
├── seed_data.py                     # Realistic e-commerce product catalog seeder
├── test_all_operations.py           # Non-interactive automated 100% verification runner
├── main.py                          # Interactive terminal CLI control panel
├── visualize_mongodb.py            # 300 DPI high-resolution visual analytics
├── requirements.txt                 # Project dependencies
├── EXPERIMENT_3_REPORT.md           # 15-page comprehensive academic manual
├── OUTPUT_REPORT_SUBMISSION.md      # Printable 1-2 page evaluator report
└── visualizations/
    ├── 1_category_revenue.png       # Aggregated category inventory value & counts
    ├── 2_stock_vs_price.png         # Stock quantity vs unit price distribution
    ├── 3_rating_distributions.png   # Product rating density curves
    └── 4_mongodb_executive_dashboard.png # Executive 4-panel catalog dashboard
```

---

## 🚀 Installation & Quick Start

### 1. Prerequisites
- **Python 3.10+**
- **MongoDB 6.0+** running on `localhost:27017` (or Docker/Podman container):
  ```bash
  # Start MongoDB via Podman/Docker if not running natively:
  podman run -d --name mongodb-local -p 27017:27017 mongo:latest
  ```

### 2. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Automated Verification Test Suite
```bash
python3 test_all_operations.py
```

### 4. Interactive CLI Menu
```bash
python3 main.py
```

### 5. Generate Visual Analytics Charts
```bash
python3 visualize_mongodb.py
```

---

## 📊 Analytical Visualizations (300 DPI)

| Visualization | Description | File Path |
| :--- | :--- | :--- |
| **Category Inventory Valuation** | Total stock value and product volume across categories | `visualizations/1_category_revenue.png` |
| **Stock Quantity vs Price** | Correlation scatter analyzing pricing vs available units | `visualizations/2_stock_vs_price.png` |
| **Rating Quality Breakdown** | Distribution of customer rating scores across departments | `visualizations/3_rating_distributions.png` |
| **MongoDB Executive Dashboard** | Complete 4-panel visual audit of the catalog database | `visualizations/4_mongodb_executive_dashboard.png` |

---

## 📑 Reports & Documentation
- **Full Academic Lab Manual**: [`EXPERIMENT_3_REPORT.md`](EXPERIMENT_3_REPORT.md) — Theory (BSON, WiredTiger, Indexing, Sharding), Step-by-Step Code Walkthrough, and 10 Viva Voce Q&As.
- **Concise Evaluator Submission (1-2 Pages)**: [`OUTPUT_REPORT_SUBMISSION.md`](OUTPUT_REPORT_SUBMISSION.md) — Formatted verification tables and benchmarks for viva presentation.
