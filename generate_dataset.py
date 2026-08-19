import pandas as pd
import random
from datetime import datetime, timedelta

from geolocation import LOCATIONS

NUM_RECORDS = 1000

users = [
    "john",
    "alice",
    "bob",
    "charlie",
    "emma",
    "david",
    "harry",
    "sophia",
    "oliver",
    "isabella"
]

devices = [
    "Laptop",
    "Desktop",
    "Mobile",
    "Unknown"
]

data = []

start_date = datetime(2025, 1, 1)

for _ in range(NUM_RECORDS):

    username = random.choice(users)

    date = start_date + timedelta(
        days=random.randint(0, 365)
    )

    location = random.choice(LOCATIONS)

    country = location["country"]
    city = location["city"]

    latitude = location["latitude"]
    longitude = location["longitude"]

    ip_address = ".".join(
        str(random.randint(1, 255))
        for _ in range(4)
    )

    if random.random() < 0.8:

        hour = random.randint(8, 22)

        login_success = 1

        failed_attempts = random.randint(0, 1)

        device = random.choice(
            ["Laptop", "Desktop", "Mobile"]
        )

        suspicious = 0

    else:

        hour = random.choice(
            [0, 1, 2, 3, 4]
        )

        login_success = random.choice(
            [0, 1]
        )

        failed_attempts = random.randint(
            3, 6
        )

        device = "Unknown"

        suspicious = 1

    minute = random.randint(0, 59)

    login_time = f"{hour:02}:{minute:02}"

    data.append([

        username,

        date.strftime("%Y-%m-%d"),

        login_time,

        ip_address,

        country,

        city,

        latitude,

        longitude,

        device,

        login_success,

        failed_attempts,

        suspicious

    ])

df = pd.DataFrame(

    data,

    columns=[

        "Username",

        "Login_Date",

        "Login_Time",

        "IP_Address",

        "Country",

        "City",

        "Latitude",

        "Longitude",

        "Device",

        "Login_Success",

        "Failed_Attempts",

        "Suspicious"
    ]
)

df.to_csv(
    "Dataset/login_data.csv",
    index=False
)

print("Dataset Generated Successfully")
print("Records:", len(df))

print(df.head())