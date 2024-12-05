# Database Schema for `stock` Table

This document outlines the structure of the `stock` table in the database, including the column names and their respective indices.

## Table: `stock`

| Index | Column Name        | Type            | Description                                                              |
|-------|--------------------|-----------------|--------------------------------------------------------------------------|
| 0     | `id`               | `INTEGER`       | Primary key, auto-incremented ID for each stock entry.                   |
| 1     | `url`              | `TEXT`          | URL for the company or stock.                                            |
| 2     | `companyname`      | `TEXT`          | Name of the company.                                                     |
| 3     | `description`      | `TEXT`          | Short description of the company or stock.                               |
| 4     | `long_description` | `TEXT`          | Detailed description of the company or stock.                            |
| 5     | `picture_url`      | `TEXT`          | URL of the company's picture.                                            |
| 6     | `wallpaper_url`    | `TEXT`          | URL of the company's wallpaper.                                          |
| 7     | `other_pictures`   | `TEXT`          | URLs of additional pictures related to the company.                      |
| 8     | `annual_demand`    | `TEXT`          | Annual demand for the stock or company.                                  |
| 9     | `website`          | `TEXT`          | Website URL for the company.                                             |
| 10    | `number_of_stock`  | `INTEGER`       | Number of stocks available.                                              |
| 11    | `virtualBit`       | `REAL`          | Virtual Bit amount associated with the company.                          |
| 12    | `username`         | `TEXT`          | Username of the associated user.                                         |
| 13    | `marketcap`        | `REAL`          | Market capitalization of the company or stock.                           |
| 14    | `available_coins`  | `INTEGER`       | Number of available coins in circulation.                                |
| 15    | `total_supply`     | `INTEGER`       | Total supply of coins for the company.                                   |
| 16    | `price`            | `REAL`          | Current price of the stock.                                              |
| 17    | `priceinUSD`       | `REAL`          | Price of the stock in USD.                                               |
| 18    | `start_date`       | `TEXT`          | Start date of the stock or company in the database.                      |
| 19    | `bit_balance`      | `REAL`          | Bit balance associated with the stock.                                   |
| 20    | `price_history_24` | `TEXT`          | Price history for the last 24 hours.                                     |
| 21    | `price_history_5d` | `TEXT`          | Price history for the last 5 days.                                       |
| 22    | `price_history_1m` | `TEXT`          | Price history for the last 1 month.                                      |
| 23    | `price_history_3m` | `TEXT`          | Price history for the last 3 months.                                     |
| 24    | `price_history_1y` | `TEXT`          | Price history for the last 1 year.                                       |
| 25    | `price_history_5y` | `TEXT`          | Price history for the last 5 years.                                      |
| 26    | `price_history_all`| `TEXT`          | All-time price history for the stock.                                    |
| 27    | `profit_24`        | `INTEGER`       | Profit in the last 24 hours.                                             |
| 28    | `profit_5d`        | `INTEGER`       | Profit in the last 5 days.                                               |
| 29    | `profit_1m`        | `INTEGER`       | Profit in the last 1 month.                                              |
| 30    | `profit_3m`        | `INTEGER`       | Profit in the last 3 months.                                             |
| 31    | `profit_1y`        | `INTEGER`       | Profit in the last 1 year.                                               |
| 32    | `profit_5y`        | `INTEGER`       | Profit in the last 5 years.                                              |
| 33    | `profit_all`       | `INTEGER`       | All-time profit for the stock.                                           |
| 34    | `network`          | `TEXT`          | Network associated with the stock or company.                            |
| 35    | `country`          | `TEXT`          | Country where the company is based.                                      |
| 36    | `min_price_24`     | `REAL`          | Minimum price in the last 24 hours.                                      |
| 37    | `max_price_24`     | `REAL`          | Maximum price in the last 24 hours.                                      |
| 38    | `min_price_5d`     | `REAL`          | Minimum price in the last 5 days.                                        |
| 39    | `max_price_5d`     | `REAL`          | Maximum price in the last 5 days.                                        |
| 40    | `min_price_1m`     | `REAL`          | Minimum price in the last 1 month.                                       |
| 41    | `max_price_1m`     | `REAL`          | Maximum price in the last 1 month.                                       |
| 42    | `min_price_3m`     | `REAL`          | Minimum price in the last 3 months.                                      |
| 43    | `max_price_3m`     | `REAL`          | Maximum price in the last 3 months.                                      |
| 44    | `min_price_1y`     | `REAL`          | Minimum price in the last 1 year.                                        |
| 45    | `max_price_1y`     | `REAL`          | Maximum price in the last 1 year.                                        |
| 46    | `min_price_5y`     | `REAL`          | Minimum price in the last 5 years.                                       |
| 47    | `max_price_5y`     | `REAL`          | Maximum price in the last 5 years.                                       |
| 48    | `min_price_all`    | `REAL`          | Minimum price for all-time.                                              |
| 49    | `max_price_all`    | `REAL`          | Maximum price for all-time.                                              |

---

### Notes:
- **Price History** columns (`price_history_24`, `price_history_5d`, etc.) store the price trends for specific periods, such as 24 hours, 5 days, 1 month, etc. They are stored as text, which could potentially be a JSON string or comma-separated values.
- **Profit** columns (`profit_24`, `profit_5d`, etc.) store the profit percentages or values for each respective period.
- The **min** and **max** price columns store the minimum and maximum prices for each period (24 hours, 5 days, etc.).
- The `country` column stores the country of the company.
