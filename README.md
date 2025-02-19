# sshah-fetch
Fetch Rewards Coding Exercise - Analytics Engineer



1. Create Tables:
postgres=# create database "fetch";
CREATE DATABASE
postgres=# \c fetch
You are now connected to database "fetch" as user "sanchitshah".
fetch=# \dn
      List of schemas
  Name  |       Owner       
--------+-------------------
 public | pg_database_owner
(1 row)

fetch=# CREATE TABLE Users (
    user_id VARCHAR(24) PRIMARY KEY,
    active BOOLEAN,
    created_date TIMESTAMP,
    last_login TIMESTAMP,
    role VARCHAR(50),
    sign_up_source VARCHAR(50),
    state VARCHAR(10)
);
CREATE TABLE
fetch=# 
fetch=# CREATE TABLE Brands (
    brand_id VARCHAR(24) PRIMARY KEY,
    barcode VARCHAR(50) UNIQUE,
    brand_code VARCHAR(50),
    category VARCHAR(100),
    category_code VARCHAR(50),
    cpg_id VARCHAR(24),
    name VARCHAR(255),
    top_brand BOOLEAN
);
CREATE TABLE
fetch=# CREATE TABLE Receipts (
    receipt_id VARCHAR(24) PRIMARY KEY,
    user_id VARCHAR(24),
    bonus_points_earned INT,
    bonus_points_reason TEXT,
    create_date TIMESTAMP,
    date_scanned TIMESTAMP,
    finished_date TIMESTAMP NULL,
    modify_date TIMESTAMP,
    points_awarded_date TIMESTAMP NULL,
    points_earned DECIMAL(10,2),
    purchase_date TIMESTAMP,
    purchased_item_count INT,
    rewards_receipt_status VARCHAR(50),
    total_spent DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
CREATE TABLE
fetch=# CREATE TABLE Receipt_Items (
    item_id SERIAL PRIMARY KEY,
    receipt_id VARCHAR(24),
    barcode VARCHAR(50),
    description TEXT,
    final_price DECIMAL(10,2),
    item_price DECIMAL(10,2),
    needs_fetch_review BOOLEAN,
    partner_item_id VARCHAR(50),
    prevent_target_gap_points BOOLEAN,
    quantity_purchased INT,
    user_flagged_barcode VARCHAR(50),
    user_flagged_new_item BOOLEAN,
    user_flagged_price DECIMAL(10,2) NULL,
    user_flagged_quantity INT NULL,
    FOREIGN KEY (receipt_id) REFERENCES Receipts(receipt_id),
    FOREIGN KEY (barcode) REFERENCES Brands(barcode)
);
CREATE TABLE
fetch=# 
