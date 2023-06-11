# Electricity-trade

This project provides you to load data about electricity pricing for the next day and allows you to get data about pricing on certain date

# Installing using GitHub

```
git clone https://github.com/MarynaProkhorenko/electricity-trade
cd social_media_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Make and run migrations

```
alembic revision --autogenerate - m "Initial migration"
alembic upgrade head
```

# To run the scheduled task
```
python load_data_to_db.py
```

# To get API for some date
```
python get_api_endpoint.py
```
- Path to get data: /pricing/search/date, where date - is desirable date of data
in format dd.mm.yyyy