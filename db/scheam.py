def create_tables(cursor, db_type):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS countries (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                continent VARCHAR(50) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS provinces (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                country_id VARCHAR(36),
                FOREIGN KEY (country_id) REFERENCES countries(id),
                UNIQUE(name, country_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                province_id VARCHAR(36),
                FOREIGN KEY (province_id) REFERENCES provinces(id),
                UNIQUE(name, province_id)
            )
        """)
        if db_type != 'sqlite':
            cursor.execute("COMMIT")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False