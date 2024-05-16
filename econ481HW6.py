#!/usr/bin/env python
# coding: utf-8

# # Exercise 0

# In[29]:


def github() -> str:
    return "https://github.com/nstfchloe/econ-481/blob/main/econ481HW6.py"


# # Exercise 1

# In[30]:


import sqlalchemy
from sqlalchemy import create_engine

path = '/home/jovyan/econ-481-jupyterhub/auctions.db'
engine = create_engine(f'sqlite:///{path}')


# In[31]:


from sqlalchemy import inspect

inspector = inspect(engine)


# In[32]:


import pandas as pd
from sqlalchemy.orm import Session

class DataBase:
    def __init__(self, loc: str, db_type: str = "sqlite") -> None:
        """Initialize the class and connect to the database"""
        self.loc = loc
        self.db_type = db_type
        self.engine = create_engine(f'{self.db_type}:///{self.loc}')
    def query(self, q: str) -> pd.DataFrame:
        """Run a query against the database and return a DataFrame"""
        with Session(self.engine) as session:
            df = pd.read_sql(q, session.bind)
        return(df)

auctions = DataBase(path)


# In[33]:


def std() -> str:
    query = """
    SELECT 
        itemId, 
        (
            SELECT 
                sqrt(sum((bidAmount - avg_bid) * (bidAmount - avg_bid)) / (count(bidAmount) - 1)) 
            FROM 
                Bids
            WHERE 
                Bids.itemId = Items.itemId
        ) AS std
    FROM 
        (SELECT 
            itemId,bidAmount,
            avg(bidAmount) as avg_bid 
         FROM 
            Bids 
         GROUP BY 
            itemId 
         HAVING 
            count(bidAmount) > 1) AS Items
    """
    return query


# # Exercise 2

# In[34]:


def bidder_spend_frac() -> str:
    query = '''
    WITH HighestBids AS (
        SELECT 
            bidderName, 
            itemId, 
            MAX(bidAmount) AS highest_bid
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    TotalExpenditure AS (
        SELECT 
            bidderName, 
            SUM(highest_bid) AS total_expenditure
        FROM 
            HighestBids
        GROUP BY 
            bidderName
    ),
    BidderMaxBids AS (
        SELECT 
            bidderName, 
            MAX(bidAmount) AS max_bid_per_item
        FROM 
            bids
        GROUP BY 
            bidderName, itemId
    ),
    OverallBids AS (
        SELECT
            bidderName,
            SUM(max_bid_per_item) AS sum_of_bids
        FROM
            BidderMaxBids
        GROUP BY
            bidderName
    )       
    SELECT 
        te.bidderName,
        te.total_expenditure,
        ob.sum_of_bids,
        CASE
            WHEN ob.sum_of_bids > 0 
            THEN te.total_expenditure * 1.0 / ob.sum_of_bids
            ELSE 0
        END AS expenditure_ratio
    FROM 
        TotalExpenditure te
    JOIN 
        OverallBids ob ON te.bidderName = ob.bidderName;
    '''
    return query


# # Exercise 3

# In[36]:


def min_increment_freq() -> str:
    query = """
    WITH NonBuyNowItems AS (
        SELECT itemId 
        FROM items 
        WHERE isBuyNowUsed = 0
    ),
    IncrementalBids AS (
        SELECT 
            b1.itemId,
            b1.bidAmount
        FROM 
            bids b1
        JOIN 
            NonBuyNowItems nbi ON b1.itemId = nbi.itemId
        WHERE 
            b1.bidAmount = (
                SELECT MAX(b2.bidAmount)
                FROM bids b2
                WHERE b2.itemId = b1.itemId 
                    AND b2.bidTime < b1.bidTime
            ) + (
                SELECT bidIncrement 
                FROM items 
                WHERE itemId = b1.itemId
            )
    )
    SELECT 
        COUNT(*) * 1.0 / (SELECT COUNT(*) FROM bids WHERE itemId IN (SELECT itemId FROM NonBuyNowItems)) AS increment_frequency
    FROM 
        IncrementalBids;
    """
    return query


# # Exercise 4

# In[38]:


def win_perc_by_timestamp() -> str:
    query = """
    WITH AuctionDurations AS (
        SELECT
            itemId,
            MIN(bidTime) AS auction_start,
            MAX(bidTime) AS auction_end
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    TimeSegmentedBids AS (
        SELECT
            b.itemId,
            b.bidderName,
            b.bidAmount,
            1 + CAST(10 * ((julianday(b.bidTime) - julianday(ad.auction_start)) / 
                (julianday(ad.auction_end) - julianday(ad.auction_start))) AS INTEGER) AS time_bin
        FROM
            bids b
        JOIN
            AuctionDurations ad ON b.itemId = ad.itemId
    ),
    TopBids AS (
        SELECT 
            itemId, 
            MAX(bidAmount) AS highest_bid
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    TimeSegmentedWinningBids AS (
        SELECT
            tsb.time_bin,
            tsb.bidAmount,
            tsb.itemId
        FROM
            TimeSegmentedBids tsb
        JOIN
            TopBids tb ON tsb.itemId = tb.itemId AND tsb.bidAmount = tb.highest_bid
    )
    SELECT
        time_bin,
        COUNT(*) * 1.0 / (SELECT COUNT(*) FROM TimeSegmentedBids WHERE time_bin = tswb.time_bin) AS winning_percentage
    FROM
        TimeSegmentedWinningBids tswb
    GROUP BY
        time_bin;
    """
    return query


# In[ ]:




