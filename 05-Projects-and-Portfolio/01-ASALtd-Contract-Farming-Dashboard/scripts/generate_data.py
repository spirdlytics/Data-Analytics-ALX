import pandas as pd
import numpy as np
import random
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

OUT = "/mnt/user-data/outputs"

# ---------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------

counties_rural = ["Trans Nzoia","Uasin Gishu","Bungoma","Nakuru","Meru","Kirinyaga",
                   "Makueni","Kitui","Machakos","Kisumu","Narok","Busia","Kakamega",
                   "Kisii","Nyeri","Embu"]
cities_urban = {"Nairobi":"Nairobi","Mombasa":"Mombasa","Kisumu":"Kisumu",
                "Nakuru":"Nakuru","Eldoret":"Uasin Gishu","Thika":"Kiambu",
                "Nyeri Town":"Nyeri","Meru Town":"Meru"}

products = [
    ("P01","Maize"), ("P02","Beans"), ("P03","Rice"), ("P04","Wheat"),
    ("P05","Sorghum"), ("P06","Millet"), ("P07","Green Grams"),
    ("P08","Cowpeas"), ("P09","Barley"),
]
prod_weight   = {"Maize":30,"Beans":14,"Rice":6,"Wheat":9,"Sorghum":11,
                 "Millet":8,"Green Grams":10,"Cowpeas":8,"Barley":4}
farmgate_range = {"Maize":(42,58),"Beans":(95,135),"Rice":(70,92),"Wheat":(46,56),
                   "Sorghum":(48,68),"Millet":(80,112),"Green Grams":(120,158),
                   "Cowpeas":(88,118),"Barley":(44,54)}
markup_range   = {"Maize":(1.18,1.35),"Beans":(1.15,1.30),"Rice":(1.20,1.40),
                   "Wheat":(1.15,1.28),"Sorghum":(1.15,1.30),"Millet":(1.15,1.28),
                   "Green Grams":(1.15,1.28),"Cowpeas":(1.15,1.28),"Barley":(1.15,1.28)}

farmer_types = ["Smallholder Farmer","Medium-Scale Farmer","Youth Farmer Group",
                "Women-Led Group","Cooperative","Commercial Farmer"]
farming_models = ["Rainfed","Irrigated","Mixed"]
aggregation_channels = ["Direct Delivery","Collection Center","Field Agent","Cooperative Bulking"]
cert_status = ["None","Certified Seed User","GAP Certified","Organic (In-Conversion)"]
payment_pref = ["Mobile Money","Bank Transfer","Cash"]

customer_types = ["Wholesaler","Retailer","School","Miller","Restaurant",
                   "Hospital","Supermarket","Relief/NGO Buyer"]
market_segment_map = {"Wholesaler":"Wholesale","Retailer":"Retail","School":"Institutional",
                       "Miller":"Processing","Restaurant":"Foodservice","Hospital":"Institutional",
                       "Supermarket":"Retail","Relief/NGO Buyer":"Institutional"}
payment_terms_opts = ["Cash on Delivery","Net 7","Net 14","Net 30"]
credit_risk_opts = ["Low","Medium","High"]
delivery_pref_opts = ["Company Delivery","Customer Pickup","Third-Party Transporter"]
sales_channels = ["Direct Sale","Tender/Institutional Order","Agent-Brokered","Standing Contract"]
order_priority_opts = ["Standard","Urgent","Scheduled"]

START = date(2025,1,1)
END   = date(2026,6,30)

def random_date(d0, d1):
    delta = (d1-d0).days
    return d0 + timedelta(days=random.randint(0, delta))

def season_for_month(m):
    if m in (1,2): return "Short Rains Harvest"
    if m in (3,4,5,6): return "Lean Season"
    if m in (7,8,9): return "Long Rains Harvest"
    return "Peak Demand Season"

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# ---------------------------------------------------------------
# 1. farmers.csv
# ---------------------------------------------------------------

first_names_m = ["John","Peter","James","Samuel","Joseph","Daniel","Francis","Paul",
                  "Stephen","Kennedy","Moses","David","Charles","Simon","Vincent"]
first_names_f = ["Mary","Jane","Grace","Ruth","Esther","Alice","Faith","Lucy",
                  "Agnes","Beatrice","Catherine","Josephine","Nancy","Sarah","Winnie"]
surnames = ["Wanjiru","Kiplagat","Otieno","Mutua","Cherop","Njoroge","Wafula","Mwangi",
            "Kamau","Achieng","Kiptoo","Barasa","Muthoni","Odhiambo","Chebet","Kariuki",
            "Wekesa","Nyongesa","Kiprono","Auma"]
group_words = ["Farmers Group","Cereal Growers Cooperative","Women in Agriculture Group",
               "Youth Agribusiness Group","Farmers Cooperative Society","Grain Growers Association"]

farmers = []
for i in range(1,121):
    fid = f"F{i:04d}"
    ftype = random.choices(farmer_types, weights=[38,18,12,12,12,8])[0]
    is_group = ftype in ("Youth Farmer Group","Women-Led Group","Cooperative")
    county = random.choice(counties_rural)
    if is_group:
        name = f"{county.split()[0]} {random.choice(group_words)} #{random.randint(1,40)}"
        gender_lead = random.choice(["Male","Female"]) if ftype!="Women-Led Group" else "Female"
    else:
        if random.random() < 0.42:
            fn = random.choice(first_names_f); gender_lead="Female"
        else:
            fn = random.choice(first_names_m); gender_lead="Male"
        name = f"{fn} {random.choice(surnames)}"
    farm_size = round(np.random.gamma(2.2, 1.6) + (8 if ftype in ("Commercial Farmer","Medium-Scale Farmer") else 0), 1)
    farm_size = clamp(farm_size, 0.5, 85)
    primary = random.choices(list(prod_weight.keys()), weights=list(prod_weight.values()))[0]
    reliability = clamp(int(np.random.normal(76,13)), 30, 99)
    farmers.append({
        "farmer_id": fid,
        "farmer_name": name,
        "farmer_type": ftype,
        "county": county,
        "sub_county": f"{county} Sub-County {random.randint(1,4)}",
        "ward": f"{county} Ward {random.randint(1,9)}",
        "gender_of_lead_farmer": gender_lead,
        "farm_size_acres": farm_size,
        "primary_cereal": primary,
        "farming_model": random.choices(farming_models, weights=[55,15,30])[0],
        "aggregation_channel": random.choice(aggregation_channels),
        "certification_status": random.choices(cert_status, weights=[55,25,15,5])[0],
        "distance_to_collection_center_km": round(clamp(np.random.exponential(9)+1,0.5,60),1),
        "payment_preference": random.choices(payment_pref, weights=[65,25,10])[0],
        "reliability_score": reliability,
        "registration_date": random_date(date(2021,1,1), date(2024,12,15)).isoformat(),
    })
farmers_df = pd.DataFrame(farmers)
farmers_df.to_csv(f"{OUT}/farmers.csv", index=False)

# ---------------------------------------------------------------
# 2. customers.csv
# ---------------------------------------------------------------

biz_words = ["Traders","Enterprises","Wholesalers","Stores","Supplies","Foods",
             "Ltd","General Merchants","Distributors","Millers"]
customers = []
for i in range(1,61):
    cid = f"C{i:04d}"
    ctype = random.choices(customer_types, weights=[22,18,10,8,10,6,14,12])[0]
    city = random.choice(list(cities_urban.keys()))
    county = cities_urban[city]
    if ctype == "School":
        name = f"{random.choice(['St. Mary','St. Joseph','Moi','Kenyatta','Uhuru','Jubilee','Riverside','Greenfield'])} {random.choice(['Primary School','Secondary School','Academy'])}"
    elif ctype == "Hospital":
        name = f"{city} {random.choice(['County Hospital','Medical Centre','Nursing Home'])}"
    elif ctype == "Restaurant":
        name = f"{random.choice(['Savanna','Nyama Choma','Delight','Highlands','Coastal','Urban'])} {random.choice(['Restaurant','Eatery','Grill'])}"
    elif ctype == "Relief/NGO Buyer":
        name = f"{random.choice(['Hope','Uplift','Harvest','Bridge','Care'])} {random.choice(['Relief Foundation','Aid Trust','NGO Kenya'])}"
    elif ctype == "Supermarket":
        name = f"{random.choice(['QuickMart','SaveMore','Metro','FreshChoice','Value'])} Supermarket {city}"
    else:
        name = f"{random.choice(surnames)} {random.choice(biz_words)}"
    preferred = random.choices(list(prod_weight.keys()), weights=list(prod_weight.values()))[0]
    avg_order = int(clamp(np.random.gamma(3, 350) + (2000 if ctype in ("Wholesaler","Miller") else 0), 100, 20000))
    customers.append({
        "customer_id": cid,
        "customer_name": name,
        "customer_type": ctype,
        "city": city,
        "county": county,
        "market_segment": market_segment_map[ctype],
        "average_order_size_kg": avg_order,
        "payment_terms": random.choices(payment_terms_opts, weights=[30,25,25,20])[0],
        "credit_risk_level": random.choices(credit_risk_opts, weights=[55,32,13])[0],
        "preferred_product": preferred,
        "delivery_preference": random.choice(delivery_pref_opts),
        "relationship_start_date": random_date(date(2022,1,1), date(2024,12,20)).isoformat(),
    })
customers_df = pd.DataFrame(customers)
customers_df.to_csv(f"{OUT}/customers.csv", index=False)

# ---------------------------------------------------------------
# 3. procurement.csv  (also seeds batches for inventory & sales)
# ---------------------------------------------------------------

prod_names = list(prod_weight.keys())
prod_weights_list = list(prod_weight.values())
farmer_ids = farmers_df["farmer_id"].tolist()
farmer_lookup = farmers_df.set_index("farmer_id").to_dict("index")

procurement = []
batches = {}  # batch_id -> dict with product, accepted_qty, received_date, county, warehouse

for i in range(1,901):
    pid = f"PR{i:05d}"
    bid = f"B{i:05d}"
    product_name = random.choices(prod_names, weights=prod_weights_list)[0]
    product_id = dict(products)[product_name] if False else [p for p,n in products if n==product_name][0]
    fid = random.choice(farmer_ids)
    finfo = farmer_lookup[fid]
    county = finfo["county"]
    pdate = random_date(START, date(2026,6,15))
    season = season_for_month(pdate.month)

    base_lo, base_hi = farmgate_range[product_name]
    # seasonal price effect: prices lower right after harvest, higher in lean season
    season_mult = {"Long Rains Harvest":0.92,"Short Rains Harvest":0.95,
                   "Lean Season":1.12,"Peak Demand Season":1.05}[season]
    farmgate_price = round(random.uniform(base_lo, base_hi) * season_mult, 2)

    quantity = round(clamp(np.random.gamma(2.4, 380), 50, 12000), 0)
    distance = finfo["distance_to_collection_center_km"]
    transport_cost = round(quantity * (0.9 + distance*0.035) / 1000 * random.uniform(0.9,1.15) * 100, 2)
    handling_cost = round(quantity * random.uniform(0.5, 1.2), 2)

    moisture = round(clamp(np.random.normal(12.5,2.1),8,22),1)
    late_delivery_prob = clamp(0.05 + distance/400, 0.05, 0.35)
    is_late = random.random() < late_delivery_prob

    if moisture <= 13:
        grade = random.choices(["Grade A","Grade B","Grade C"], weights=[60,32,8])[0]
    elif moisture <= 16:
        grade = random.choices(["Grade A","Grade B","Grade C"], weights=[25,50,25])[0]
    else:
        grade = random.choices(["Grade A","Grade B","Grade C"], weights=[5,35,60])[0]

    reject_prob = clamp((moisture-11)*0.05, 0, 0.5)
    if random.random() < reject_prob:
        rejected = round(quantity * random.uniform(0.03,0.25),0)
    else:
        rejected = 0
    accepted = quantity - rejected

    reliability = finfo["reliability_score"]
    pay_status = random.choices(["Paid","Pending","Delayed"], weights=[70,18,12])[0]
    if pay_status == "Paid":
        days_to_pay = int(clamp(np.random.normal(30-reliability*0.2, 4), 0, 21))
    elif pay_status == "Delayed":
        days_to_pay = int(clamp(np.random.normal(35,10), 20, 75))
    else:
        days_to_pay = None

    warehouse = f"{county} Aggregation Warehouse"

    procurement.append({
        "procurement_id": pid,
        "batch_id": bid,
        "farmer_id": fid,
        "product_id": product_id,
        "product_name": product_name,
        "procurement_date": pdate.isoformat(),
        "season": season,
        "county_sourced": county,
        "quantity_kg": int(quantity),
        "farmgate_price_kes_per_kg": farmgate_price,
        "transport_cost_kes": transport_cost,
        "handling_cost_kes": handling_cost,
        "moisture_percent": moisture,
        "grade": grade,
        "rejected_quantity_kg": int(rejected),
        "accepted_quantity_kg": int(accepted),
        "collection_center": f"{county} Collection Center {random.randint(1,3)}",
        "payment_status": pay_status,
        "days_to_pay_farmer": days_to_pay if days_to_pay is not None else "",
        "_late_delivery": is_late,
    })

    batches[bid] = {
        "product_id": product_id, "product_name": product_name,
        "accepted_quantity_kg": accepted, "received_date": pdate,
        "county": county, "warehouse": warehouse, "grade": grade,
        "moisture_percent": moisture, "sold_quantity_kg": 0,
    }

procurement_df = pd.DataFrame(procurement).drop(columns=["_late_delivery"])
procurement_df.to_csv(f"{OUT}/procurement.csv", index=False)

# ---------------------------------------------------------------
# 4. sales.csv
# ---------------------------------------------------------------

customer_ids = customers_df["customer_id"].tolist()
customer_lookup = customers_df.set_index("customer_id").to_dict("index")

# group available batches by product for matching against customer preference
batches_by_product = {}
for bid, b in batches.items():
    batches_by_product.setdefault(b["product_name"], []).append(bid)

sales = []
for i in range(1,751):
    sid = f"S{i:05d}"
    cid = random.choice(customer_ids)
    cinfo = customer_lookup[cid]
    # prefer customer's preferred product 65% of the time, else any product
    if random.random() < 0.65 and batches_by_product.get(cinfo["preferred_product"]):
        product_name = cinfo["preferred_product"]
    else:
        product_name = random.choices(prod_names, weights=prod_weights_list)[0]
    candidates = [b for b in batches_by_product.get(product_name, [])
                  if batches[b]["accepted_quantity_kg"] - batches[b]["sold_quantity_kg"] > 20]
    if not candidates:
        continue
    bid = random.choice(candidates)
    binfo = batches[bid]
    product_id = binfo["product_id"]

    remaining = binfo["accepted_quantity_kg"] - binfo["sold_quantity_kg"]
    desired = clamp(cinfo["average_order_size_kg"]*random.uniform(0.4,1.1), 20, remaining)
    qty = int(clamp(desired, 20, remaining))
    binfo["sold_quantity_kg"] += qty

    sale_date_earliest = binfo["received_date"] + timedelta(days=random.randint(1,10))
    sale_date = random_date(sale_date_earliest, min(sale_date_earliest+timedelta(days=75), END))

    base_lo, base_hi = farmgate_range[product_name]
    mk_lo, mk_hi = markup_range[product_name]
    grade_mult = {"Grade A":1.06,"Grade B":1.0,"Grade C":0.9}[binfo["grade"]]
    selling_price = round(random.uniform(base_lo, base_hi) * random.uniform(mk_lo, mk_hi) * grade_mult, 2)

    discount = 0
    if random.random() < 0.22:
        discount = round(random.uniform(1,8),1)

    delivery_cost = round(qty * random.uniform(0.4,1.3), 2) if cinfo["delivery_preference"]!="Customer Pickup" else 0.0

    pay_status = random.choices(["Paid","Pending","Overdue"],
                                 weights={"Low":[75,18,7],"Medium":[58,27,15],
                                          "High":[40,30,30]}[cinfo["credit_risk_level"]])[0]
    if pay_status=="Paid":
        days_to_pay = int(clamp(np.random.normal(9,5),0,21))
    elif pay_status=="Pending":
        days_to_pay = int(clamp(np.random.normal(20,8),5,40))
    else:
        days_to_pay = int(clamp(np.random.normal(48,15),30,90))

    channel = "Tender/Institutional Order" if cinfo["customer_type"] in ("School","Hospital","Relief/NGO Buyer") else \
              random.choices(sales_channels, weights=[45,10,25,20])[0]
    priority = random.choices(order_priority_opts, weights=[65,15,20])[0]

    sales.append({
        "sale_id": sid,
        "batch_id": bid,
        "customer_id": cid,
        "product_id": product_id,
        "product_name": product_name,
        "sale_date": sale_date.isoformat(),
        "city_sold": cinfo["city"],
        "customer_type": cinfo["customer_type"],
        "quantity_sold_kg": qty,
        "selling_price_kes_per_kg": selling_price,
        "discount_percent": discount,
        "delivery_cost_kes": delivery_cost,
        "payment_status": pay_status,
        "days_to_customer_payment": days_to_pay,
        "sales_channel": channel,
        "order_priority": priority,
    })

sales_df = pd.DataFrame(sales)
sales_df.to_csv(f"{OUT}/sales.csv", index=False)

# ---------------------------------------------------------------
# 5. inventory_quality.csv (one row per batch)
# ---------------------------------------------------------------

shrinkage_reasons = ["Moisture Loss","Pest Damage","Spillage During Handling",
                      "Weighing Variance","None"]

inv_rows = []
for bid, b in batches.items():
    opening = b["accepted_quantity_kg"]
    sold = b["sold_quantity_kg"]
    moisture = b["moisture_percent"]
    grade = b["grade"]

    shrink_rate = clamp((moisture-10)*0.004 + random.uniform(0,0.01), 0, 0.06)
    shrinkage = int(round(opening * shrink_rate))
    closing = max(0, opening - sold - shrinkage)

    if shrinkage == 0:
        reason = "None"
    else:
        reason = random.choices(shrinkage_reasons[:-1], weights=[45,20,25,10])[0]

    if moisture > 16 or grade=="Grade C":
        aflatoxin = random.choices(["Low","Medium","High"], weights=[20,45,35])[0]
    elif moisture > 13:
        aflatoxin = random.choices(["Low","Medium","High"], weights=[45,40,15])[0]
    else:
        aflatoxin = random.choices(["Low","Medium","High"], weights=[75,22,3])[0]

    fumigation = "Yes" if (aflatoxin in ("Medium","High") or random.random()<0.1) else "No"

    storage_days = (END - b["received_date"]).days if sold < opening else \
        random.randint(3,75)
    storage_days = int(clamp(storage_days, 1, 400))

    condition_score = round(clamp(np.random.normal(7.6 - (0.15 if aflatoxin=="High" else 0),1.1),2,10),1)

    inv_rows.append({
        "batch_id": bid,
        "product_id": b["product_id"],
        "product_name": b["product_name"],
        "warehouse_location": b["warehouse"],
        "received_date": b["received_date"].isoformat(),
        "storage_days": storage_days,
        "opening_stock_kg": int(opening),
        "accepted_quantity_kg": int(opening),
        "sold_quantity_kg": int(sold),
        "closing_stock_kg": int(closing),
        "shrinkage_kg": shrinkage,
        "shrinkage_reason": reason,
        "quality_grade": grade,
        "moisture_percent": moisture,
        "aflatoxin_risk_level": aflatoxin,
        "fumigation_required": fumigation,
        "warehouse_condition_score": condition_score,
    })

inv_df = pd.DataFrame(inv_rows)
inv_df.to_csv(f"{OUT}/inventory_quality.csv", index=False)

print("farmers:", len(farmers_df))
print("customers:", len(customers_df))
print("procurement:", len(procurement_df))
print("sales:", len(sales_df))
print("inventory_quality:", len(inv_df))
