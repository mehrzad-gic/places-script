import argparse
from ui.cli import run_cli

def main():
    parser = argparse.ArgumentParser(description="Geo Database Management Tool")
    parser.add_argument('--db-type', required=True, choices=['mysql', 'mariadb', 'postgresql', 'sqlite'],
                        help='Database type')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', default='3306', help='Database port')
    parser.add_argument('--user', default='root', help='Database user')
    parser.add_argument('--password', default='', help='Database password')
    parser.add_argument('--database', default='geo_db', help='Database name or SQLite file path')
    
    args = parser.parse_args()
    run_cli(args)

if __name__ == "__main__":
    main()