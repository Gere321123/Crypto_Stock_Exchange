# Crypto Stock Exchange

**Crypto Stock Exchange** is a startup revolutionizing how companies raise funds from investors. Our platform enables companies to tokenize their equity using **Wrapped Bitcoin (WBTC)**, offering a cost-effective alternative to traditional stock markets. In many Eastern European countries, listing on traditional stock markets can cost at least €100,000, whereas our solution is far more affordable.

## Key Features

1. **Affordable Tokenization:** Companies can tokenize their equity at a fraction of the cost compared to traditional stock markets.
2. **Decentralized Dividends:** Investors earn dividends when companies generate profits, promoting transparency and aligning incentives between businesses and their backers.
3. **Stable Crypto Ecosystem:**
   - The platform leverages **Wrapped Bitcoin (WBTC)** for tokenized equity.
   - Using Bitcoin-backed assets provides stability, as Bitcoin’s larger market capitalization offers long-term reliability.

## Why Use Wrapped Bitcoin Instead of Ethereum?

- **Market Stability:** Bitcoin’s significantly larger market cap reduces volatility compared to Ethereum.
- **Investor Confidence:** Greater liquidity in Bitcoin makes investors feel more secure.
- **Global Wealth Allocation:** Bitcoin represents approximately 1% of all global money, showcasing high trust and adoption.
- **Institutional Support:** Major institutions like BlackRock hold a substantial portion of Bitcoin (around 10%), and their interest in Bitcoin supports stability and long-term growth.

## What Happens If a Company Fails to Pay Dividends?

To ensure investor trust, the **Crypto Stock Exchange** enforces strict accountability measures:
- Companies that fail to pay dividends when required lose access to their tokenized stocks.
- They are unable to withdraw any funds from their tokenized equity, compelling companies to prioritize investor returns.

## Simple Stock Price Adjustment Formula

To create a dynamic and fair market, we utilize a **price adjustment formula inspired by Uniswap’s automated market maker model**:
- Stock prices adjust automatically based on supply and demand.
- This ensures liquidity and enables real-time price discovery, fostering a transparent and efficient marketplace.

## Development Status

The project is in its early stages, with the platform deployed on the **Binance Smart Chain (BSC) testnet** using **Wrapped Bitcoin (WBTC)**. We continue to improve the platform and welcome feedback from the community to make **Crypto Stock Exchange** the preferred platform for decentralized fundraising.

---

## Test the Contract on Binance Smart Chain (BSC) Testnet

- **For me Deploy contract:** `export $(grep -v '^#' .env | xargs)`

`forge script script/DeployMockWBTC.s.sol --rpc-url $RPC_URL --private-key $PRIVATE_KEY --broadcast -vvvv`

change the address

`forge build`

`forge script script/DeployCoin.s.sol --rpc-url $RPC_URL --private-key $PRIVATE_KEY --broadcast -vvvv`
