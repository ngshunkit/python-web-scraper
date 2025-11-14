import sqlite3
import pandas as pd
from datetime import datetime

class FundDatabase:
    def __init__(self, db_path='data/funds.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with fund table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fund_name TEXT NOT NULL,
                fund_code TEXT NOT NULL,
                risk_level TEXT,
                bid_price TEXT,
                offer_price TEXT,
                valuation_date TEXT,
                morningstar_rating TEXT,
                currency TEXT,
                scrape_timestamp TEXT,
                UNIQUE(fund_code, valuation_date)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_funds(self, funds_data):
        """Insert fund data into database"""
        conn = sqlite3.connect(self.db_path)
        
        for fund in funds_data:
            try:
                conn.execute('''
                    INSERT OR REPLACE INTO funds 
                    (fund_name, fund_code, risk_level, bid_price, offer_price, 
                     valuation_date, morningstar_rating, currency, scrape_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    fund['fund_name'],
                    fund['fund_code'],
                    fund['risk_level'],
                    fund['bid_price'],
                    fund['offer_price'],
                    fund['valuation_date'],
                    fund['morningstar_rating'],
                    fund['currency'],
                    datetime.now().isoformat()
                ))
            except Exception as e:
                print(f"Error inserting fund {fund.get('fund_code')}: {e}")
        
        conn.commit()
        conn.close()
    
    def get_latest_funds(self):
        """Retrieve latest fund data"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('SELECT * FROM funds ORDER BY scrape_timestamp DESC', conn)
        conn.close()
        return df

