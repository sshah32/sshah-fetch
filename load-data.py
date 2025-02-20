import json
import psycopg2
#from datetime import datetime
from datetime import datetime, UTC

# Database connection
conn = psycopg2.connect(
    dbname="fetch",
    #user="your_username",
    #password="your_password",
    #host="your_host",
    port="5432"
)
cursor = conn.cursor()

# Load JSON files
with open('users.json') as f:
    users = json.load(f)

with open('brands.json') as f:
    brands = json.load(f)

with open('receipts.json') as f:
    receipts = json.load(f)

# Function to convert timestamp
def convert_timestamp(timestamp):
    if timestamp is None:
        return None  # Handle missing timestamps gracefully
    return datetime.fromtimestamp(timestamp / 1000, UTC).strftime('%Y-%m-%d %H:%M:%S')

# Insert Users
for user in users:
    cursor.execute("""
        INSERT INTO Users (user_id, active, created_date, last_login, role, sign_up_source, state)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING;
    """, (
        user["_id"]["$oid"],
        user["active"],
        convert_timestamp(user["createdDate"]["$date"]),
        convert_timestamp(user.get("lastLogin", {}).get("$date")),
        user.get("role", "unknown"),  # Default to 'unknown' if missing
        user.get("signUpSource", "unknown"),  # Default to 'unknown' if missing
        user.get("state", "unknown")
    ))

# Insert Brands
for brand in brands:
    cursor.execute("""
        INSERT INTO Brands (brand_id, barcode, brand_code, category, category_code, cpg_id, name, top_brand)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (brand_id) DO NOTHING;
    """, (
        brand["_id"]["$oid"],
        brand.get("barcode", None),  
        brand.get("brandCode", None),  
        brand.get("category", "unknown"),  
        brand.get("categoryCode", "unknown"),  
        brand.get("cpg", {}).get("$id", {}).get("$oid", None),  
        brand.get("name", "unknown"),  
        brand.get("topBrand", False)
    ))

# Insert Receipts
for receipt in receipts:
    cursor.execute("""
        INSERT INTO Receipts (receipt_id, user_id, bonus_points_earned, bonus_points_reason, create_date,
                              date_scanned, finished_date, modify_date, points_awarded_date, points_earned, 
                              purchase_date, purchased_item_count, rewards_receipt_status, total_spent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (receipt_id) DO NOTHING;
    """, (
        receipt["_id"]["$oid"],
        receipt.get("userId", None),  
        receipt.get("bonusPointsEarned", 0),  
        receipt.get("bonusPointsEarnedReason", "unknown"),  
        convert_timestamp(receipt.get("createDate", {}).get("$date")),  
        convert_timestamp(receipt.get("dateScanned", {}).get("$date")),  
        convert_timestamp(receipt.get("finishedDate", {}).get("$date")),  
        convert_timestamp(receipt.get("modifyDate", {}).get("$date")),  
        convert_timestamp(receipt.get("pointsAwardedDate", {}).get("$date")),  
        float(receipt.get("pointsEarned", 0)),  
        convert_timestamp(receipt.get("purchaseDate", {}).get("$date")),  
        receipt.get("purchasedItemCount", 0),  
        receipt.get("rewardsReceiptStatus", "unknown"),  
        float(receipt.get("totalSpent", 0.0))  
    ))

    # Insert Receipt Items
    for item in receipt["rewardsReceiptItemList"]:
        cursor.execute("""
            INSERT INTO rewards_receipt_items (receipt_id, barcode, description, final_price, item_price, needs_fetch_review,
                                       partner_item_id, prevent_target_gap_points, quantity_purchased, 
                                       user_flagged_barcode, user_flagged_new_item, user_flagged_price, 
                                       user_flagged_quantity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            receipt["_id"]["$oid"],
            item.get("barcode", None),
            item.get("description", "unknown"),  
            float(item.get("finalPrice", 0.0)),  
            float(item.get("itemPrice", 0.0)),  
            item.get("needsFetchReview", False),  
            item.get("partnerItemId", None),  
            item.get("preventTargetGapPoints", False),  
            item.get("quantityPurchased", 0),  
            item.get("userFlaggedBarcode", None),  
            item.get("userFlaggedNewItem", False),  
            float(item.get("userFlaggedPrice", 0.0)) if "userFlaggedPrice" in item else None,  
            item.get("userFlaggedQuantity", None)  
        ))

# Commit and close connection
conn.commit()
cursor.close()
conn.close()

