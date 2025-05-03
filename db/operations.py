from uuid import uuid4

def insert_country(cursor, db_type, name, continent):
    country_id = str(uuid4())
    try:
        cursor.execute("INSERT INTO countries (id, name, continent) VALUES (%s, %s, %s)", 
                      (country_id, name, continent))
        if db_type != 'sqlite':
            cursor.execute("COMMIT")
        return country_id
    except Exception as e:
        print(f"Error inserting country: {e}")
        return None

def insert_province(cursor, db_type, name, country_id):
    province_id = str(uuid4())
    try:
        cursor.execute("INSERT INTO provinces (id, name, country_id) VALUES (%s, %s, %s)", 
                      (province_id, name, country_id))
        if db_type != 'sqlite':
            cursor.execute("COMMIT")
        return province_id
    except Exception as e:
        print(f"Error inserting province: {e}")
        return None

def insert_city(cursor, db_type, name, province_id):
    city_id = str(uuid4())
    try:
        cursor.execute("INSERT INTO cities (id, name, province_id) VALUES (%s, %s, %s)", 
                      (city_id, name, province_id))
        if db_type != 'sqlite':
            cursor.execute("COMMIT")
        return city_id
    except Exception as e:
        print(f"Error inserting city: {e}")
        return None

def get_countries(cursor):
    cursor.execute("SELECT id, name, continent FROM countries")
    return cursor.fetchall()

def get_provinces(cursor, country_id):
    cursor.execute("SELECT id, name FROM provinces WHERE country_id = %s", (country_id,))
    return cursor.fetchall()