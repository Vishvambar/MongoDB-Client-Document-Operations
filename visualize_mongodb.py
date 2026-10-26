"""
Data Visualizer Module for Task 3: MongoDB Analytics.
Extracts aggregated documents from MongoDB and produces publication-quality
visual charts using Matplotlib, Seaborn, and Pandas.
"""

import os
import warnings
warnings.filterwarnings('ignore')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from config import get_collection
from mongodb_client import MongoOperationsService

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "visualizations")


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_data():
    """Queries MongoDB collection and extracts DataFrames."""
    service = MongoOperationsService()
    docs = service.search_many()
    df = pd.DataFrame(docs)
    if '_id' in df.columns:
        df['_id'] = df['_id'].astype(str)
    return df, service


def plot_category_valuation(service: MongoOperationsService):
    """Dual-axis bar chart comparing inventory valuation and stock units."""
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, "1_category_inventory_valuation.png")

    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "total_stock": {"$sum": "$stock"},
                "total_val": {"$sum": {"$multiply": ["$price", "$stock"]}}
            }
        },
        {"$sort": {"total_val": -1}}
    ]
    data = service.aggregate(pipeline)
    df_cat = pd.DataFrame(data)

    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
    plt.title("MongoDB Aggregation: Category Inventory Valuation vs. Stock Units", fontsize=13, fontweight='bold', pad=15)

    x = range(len(df_cat))
    width = 0.38
    color_val = '#3b82f6'
    color_stock = '#10b981'

    val_in_lakhs = df_cat['total_val'] / 100000.0
    bars1 = ax1.bar([i - width/2 for i in x], val_in_lakhs, width=width, label='Valuation (₹ in Lakhs)', color=color_val, alpha=0.85)
    ax1.set_xlabel('Product Category', fontsize=11, fontweight='semibold', labelpad=10)
    ax1.set_ylabel('Valuation (₹ Lakhs)', color=color_val, fontsize=11, fontweight='semibold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_cat['_id'], fontsize=10, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_val)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f"₹{h:.1f}L", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9, fontweight='bold')

    # Secondary axis: stock units
    ax2 = ax1.twinx()
    bars2 = ax2.bar([i + width/2 for i in x], df_cat['total_stock'], width=width, label='Stock Units', color=color_stock, alpha=0.85)
    ax2.set_ylabel('Total Stock Units', color=color_stock, fontsize=11, fontweight='semibold')
    ax2.tick_params(axis='y', labelcolor=color_stock)

    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"{int(h)}", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    return filepath


def plot_price_distribution(df: pd.DataFrame):
    """Box plot of price ranges across categories."""
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, "2_price_distribution_by_category.png")

    plt.figure(figsize=(10, 5), dpi=300)
    sns.set_theme(style="whitegrid")
    sns.boxplot(data=df, x='category', y='price', palette='Blues_r')
    sns.stripplot(data=df, x='category', y='price', color='black', alpha=0.6, jitter=0.2, size=6)

    plt.title("MongoDB Document Search: Price Spread by Category (with Data Points)", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Category", fontsize=11, fontweight='semibold')
    plt.ylabel("Price in ₹", fontsize=11, fontweight='semibold')
    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    return filepath


def plot_executive_dashboard(df: pd.DataFrame, service: MongoOperationsService):
    """4-Quadrant Executive MongoDB Visual Analytics Dashboard."""
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, "3_mongodb_executive_dashboard.png")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    fig.suptitle("MongoDB Client & Collection Operations - Visual Dashboard", fontsize=16, fontweight='bold', y=0.98)

    # 1. Product Count per Category (Top Left)
    ax1 = axes[0, 0]
    cat_counts = df['category'].value_counts()
    sns.barplot(x=cat_counts.index, y=cat_counts.values, ax=ax1, palette='crest')
    ax1.set_title("1. Products per Category", fontweight='bold', fontsize=11)
    ax1.set_xlabel("")
    ax1.set_ylabel("Count of Products")
    for p in ax1.patches:
        ax1.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='baseline', fontsize=10, xytext=(0, 3), textcoords='offset points')

    # 2. Tag Frequency from $unwind (Top Right)
    ax2 = axes[0, 1]
    tags_agg = service.aggregate([
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 6}
    ])
    df_tags = pd.DataFrame(tags_agg)
    if not df_tags.empty:
        sns.barplot(data=df_tags, x='count', y='_id', ax=ax2, palette='mako')
        ax2.set_title("2. Top Product Tags ($unwind Aggregation)", fontweight='bold', fontsize=11)
        ax2.set_xlabel("Tag Frequency")
        ax2.set_ylabel("Tag")

    # 3. Category Inventory Share Donut (Bottom Left)
    ax3 = axes[1, 0]
    inv_agg = service.aggregate([
        {"$group": {"_id": "$category", "total_val": {"$sum": {"$multiply": ["$price", "$stock"]}}}}
    ])
    df_inv = pd.DataFrame(inv_agg)
    if not df_inv.empty:
        ax3.pie(df_inv['total_val'], labels=df_inv['_id'], autopct='%1.1f%%', startangle=140,
                colors=sns.color_palette("Set2", len(df_inv)),
                wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
        ax3.set_title("3. Inventory Valuation Share", fontweight='bold', fontsize=11)

    # 4. Rating vs Price Scatter (Bottom Right)
    ax4 = axes[1, 1]
    sns.scatterplot(data=df, x='price', y='rating', hue='category', s=100, ax=ax4, palette='tab10')
    ax4.set_title("4. Customer Rating vs. Product Price", fontweight='bold', fontsize=11)
    ax4.set_xlabel("Price (₹)")
    ax4.set_ylabel("Customer Rating (0-5)")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    return filepath


def generate_all_visualizations():
    """Generates all 3 MongoDB analytical visual charts."""
    print("[*] Generating Visual Analytics from MongoDB...")
    df, service = fetch_data()
    if df.empty:
        print("[!] No documents found in MongoDB collection. Please seed data first.")
        return []

    c1 = plot_category_valuation(service)
    print(f" [✓] Created: {os.path.basename(c1)}")
    c2 = plot_price_distribution(df)
    print(f" [✓] Created: {os.path.basename(c2)}")
    c3 = plot_executive_dashboard(df, service)
    print(f" [✓] Created: {os.path.basename(c3)}")

    print(f"[✓] Visual charts successfully saved to: {OUTPUT_DIR}")
    return [c1, c2, c3]


if __name__ == "__main__":
    generate_all_visualizations()
