# sshah-fetch
Fetch Rewards Coding Exercise - Analytics Engineer

# First: Review Existing Unstructured Data and Diagram a New Structured Relational Data Model #
Review the 3 sample data files provided below. Develop a simplified, structured, relational diagram to represent how you would model the data in a data warehouse. The diagram should show each table’s fields and the joinable keys. You can use pencil and paper, readme, or any digital drawing or diagramming tool with which you are familiar. If you can upload the text, image, or diagram into a git repository and we can read it, we will review it!

![IMG_9949](https://github.com/user-attachments/assets/077cf9a8-5525-4822-8f04-500e0af6a8e8)



1. Create Tables:

```
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

```
# Second: Write queries that directly answer predetermined questions from a business stakeholder
# Third: Evaluate Data Quality Issues in the Data Provided
1. Same Barcode Names for Multiple Brands
```
(sanchit-venv) sanchitshah@mac Downloads % python3 load-data.py
Traceback (most recent call last):
  File "/Users/sanchitshah/Downloads/load-data.py", line 50, in <module>
    cursor.execute("""
    ~~~~~~~~~~~~~~^^^^
        INSERT INTO Brands (brand_id, barcode, brand_code, category, category_code, cpg_id, name, top_brand)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<10 lines>...
        brand.get("topBrand", False)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ))
    ^^
psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "brands_barcode_key"
DETAIL:  Key (barcode)=(511111504139) already exists.
```
2. Improper formatting of JSON records in the `.json` files. Formatted file looks like below. 
```
[{"_id":{"$oid":"601ac115be37ce2ead437551"},"barcode":"511111019862","category":"Baking","categoryCode":"BAKING","cpg":{"$id":{"$oid":"601ac114be37ce2ead437550"},"$ref":"Cogs"},"name":"test brand @1612366101024","topBrand":false},
{"_id":{"$oid":"601c5460be37ce2ead43755f"},"barcode":"511111519928","brandCode":"STARBUCKS","category":"Beverages","categoryCode":"BEVERAGES","cpg":{"$id":{"$oid":"5332f5fbe4b03c9a25efd0ba"},"$ref":"Cogs"},"name":"Starbucks","topBrand":false},
{"_id":{"$oid":"601ac142be37ce2ead43755d"},"barcode":"511111819905","brandCode":"TEST BRANDCODE @1612366146176","category":"Baking","categoryCode":"BAKING","cpg":{"$id":{"$oid":"601ac142be37ce2ead437559"},"$ref":"Cogs"},"name":"test brand @1612366146176","topBrand":false}]
```
3. Some of the columns Missing for certain records. For example Users table did not have lastLogin for all columns. I'd propose to add a workaround to add a default value if not provided, working with stakeholders/end users around what they'd expect as well.

4. 

# Fourth: Communicate with Stakeholders
Construct an email or slack message that is understandable to a product or business leader who isn’t familiar with your day to day work. This part of the exercise should show off how you communicate and reason about data with others. Commit your answers to the git repository along with the rest of your exercise.

Summary of Slack message to Stakeholder summarizing what other info I plan to gather working with stakeholder ( below I have attempted to answer the questions in Detail ) 

Dear Stakeholder, As we design and understand the Data Model for this data I am able to perform the data loading for these with some assumptions. I'd like to take a moment and ask some clarifying questions to prepare a datastore that is performant, resilient and scalable. Some of these questions include  whether the columns expect to have duplicates and preferred default values for it. Is it possible to define the data retention criterias for these tables ? And if we can have an better understanding of the anticipated read and write workload patterns. Thank you.

# Attempting all the other considerations I'd take when I Design this datastore.

What questions do you have about the data?
1) What columns can we expect to have Unique Data ? If duplicate data comes in , how to handle conflict ( for example on conflict ... do nothing, on conflict...update ) ? 
2) Ask Questions about the Read and Write frequency - to get an idea of how much normalized this data need to be made while drawing the ER diagram, and the implementation. Trade-off's is : Normalized ( removing redundancy by breaking down JSON into structured tables ) vs Denormalized ( Ease of Querying Data ) 
3) Any preference of default values in the event of missing or null columns ?
4) Are any fields computed or derived from other fields?

How did you discover the data quality issues?
1) Through Data Loading: I came across Data Quality Issues while Inserting the Json data using python into Structured SQL table , while reading the data.Example of Issues: Missing Data for some columns, Duplicate Data , Same Barcode for multiple Brands  
2) Through Data consistency checks 
3) Through Data completeness ( for example: totaltimespent if negative, timestamp if not in expected format ) 

   
What do you need to know to resolve the data quality issues?
1) Add proper logging and Error handling
2) Check for Missing or Null values
3) Check for Duplicates

What other information would you need to help you optimize the data assets you're trying to create?
1) Cost Considerations and Data Pruning Strategizes
2) Understand Users Read and Write SLA's and Frequencies
3) Short term and Long Term Utilization for these Tables
   

What performance and scaling concerns do you anticipate in production and how do you plan to address them?
1) Performance Considerations:
Storage consumption and Ease of Retrieval: Some of the columns ( example: bonusPointsEarnedReason ) may take up lots of storage based on the amount of data coming in. Hence, while performing writes ( this may increase WAL buffers, increased Storage sizes, TOAST tables, etc ) if not stored w/ proper limits. For reads - it would require to have the right Index based on the Query pattens ( example: timestamp, createddate, lastlogin, etc based on the Requirement of the User )
Data Pruning and Archival: Strategies to keep in place around moving the cold data to archived storage and Hot data in the Main/partitioned table. Discussing the Data Prune SLA's beforehand while designing the table.

   
2) Scalability Considerations:
for Read/write scaling: Have a connection pooler like pgbouncer/RDS proxy to handle the concurrent read/writes. 
for data processing: we can use stream processing to make it event driven, and load it as it comes. However, if the data load is not that frequent, I'd recommend batch processing. Kafka integrated with Spark/ETL scripts can help with scaling Data Ingestion keeping in mind Data security, Re-try of failures.
for Data Accessibility: I'd consider horizontal scaling : Sharing based on for example timestamp, with the goal to evenly distribute the data accross shards/partitions )
for Concurrent processing: Implement caching through Redis for Rate limiting.
for Proactive Monitoring: Integrate the database/datastore with tools like pganalyze, graphana, PRTG, Datadog - to get in-depth view of the Process lifecycle and Query Times Historically and present view. Identify the key indicators such as the last event ceated - based on the agreed SLA with the stakeholder. ) 




