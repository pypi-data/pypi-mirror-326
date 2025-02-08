from perennial_sdk.main.markets import *
from perennial_sdk.utils.calc_funding_rate_draft_two import calculate_funding_and_interest_for_sides

class MarketInfo:
    def __init__(self):
        pass

    def get_all_snapshots(self) -> dict:
        try:
            all_markets = []
            snapshot_dict = {}

            for market_name, market_address in arbitrum_markets.items():
                all_markets.append(market_name)

            snapshot_dict = fetch_market_snapshot(all_markets)

            processed_snapshot_dict = {}
            for market_name, item in snapshot_dict.items():
                try:
                    market_snapshots = item['preUpdate']['marketSnapshots']
                    for snapshot in market_snapshots:
                        market_address = snapshot['marketAddress']
                        symbol = get_symbol_for_market_address(market_address)
                        processed_snapshot_dict[symbol] = item

                except KeyError as e:
                    logger.error(f"market_info.py - KeyError encountered while parsing snapshot: {e}", exc_info=True)

            return processed_snapshot_dict

        except Exception as e:
            logger.error(f'market_info.py/get_all_snapshots - Failed to fetch funding rates. Error: {e}', exc_info=True)
            return None

    def fetch_market_price(self, symbol: str, snapshot: dict = None) -> dict:
        try:
            if not snapshot:
                snapshot = fetch_market_snapshot([symbol])
                pre_update_snapshots = snapshot['result']["preUpdate"]["marketSnapshots"]
                post_update_snapshots = snapshot['result']["postUpdate"]["marketSnapshots"]
            else:
                pre_update_snapshots = snapshot["preUpdate"]["marketSnapshots"]
                post_update_snapshots = snapshot["postUpdate"]["marketSnapshots"]

            pre_update_market_snapshot = next(
                (s for s in pre_update_snapshots if get_symbol_for_market_address(s["marketAddress"]) == symbol),
                None
            )
            post_update_market_snapshot = next(
                (s for s in post_update_snapshots if get_symbol_for_market_address(s["marketAddress"]) == symbol),
                None
            )

            if not pre_update_market_snapshot or not post_update_market_snapshot:
                raise ValueError(f"Market snapshots for symbol {symbol} not found in pre/post updates")

            pre_update_market_price = float(pre_update_market_snapshot["global"]["latestPrice"]) / BIG_6_DIVISOR
            latest_market_price = float(post_update_market_snapshot["global"]["latestPrice"]) / BIG_6_DIVISOR

            return {
                "pre_update_market_price": pre_update_market_price,
                "latest_market_price": latest_market_price
            }
        
        except Exception as e:
            logger.error(f'market_info.py/fetch_market_price() - Error while fetching latest market price for market {symbol}. Error: {e}', exc_info=True)
            return None

    def fetch_market_funding_rate(self, symbol: str, snapshot: dict = None):
        try:
            if not snapshot:
                snapshot = fetch_market_snapshot([symbol])

            raw_funding_dict = calculate_funding_and_interest_for_sides(snapshot)
            hourly_net_rate_long = float(raw_funding_dict['long']['funding_rate_long_hourly']) - float(raw_funding_dict['long']['funding_fee_long_hourly']) + float(raw_funding_dict['long']['interest_fee_long_hourly'])
            hourly_net_rate_short = float(raw_funding_dict['short']['funding_rate_short_hourly']) - float(raw_funding_dict['short']['funding_fee_short_hourly']) + float(raw_funding_dict['short']['interest_fee_short_hourly'])

            return {
                "net_rate_long_1hr": hourly_net_rate_long,
                "net_rate_short_1hr": hourly_net_rate_short
            }

        except Exception as e:
            logger.error(f'market_info.py/fetch_market_funding_rate() - Error while fetching funding rates for market {symbol}. Error: {e}', exc_info=True)
            return None

    def fetch_margin_maintenance_info(self, symbol: str, snapshot: dict = None):
        try:
            if not snapshot:
                snapshot = fetch_market_snapshot([symbol])
                margin_fee = snapshot["result"]["postUpdate"]["marketSnapshots"][0]["riskParameter"]["margin"] / 1e4
                min_margin = snapshot["result"]["postUpdate"]["marketSnapshots"][0]["riskParameter"]["minMargin"] / BIG_6_DIVISOR
                maintenance_fee = snapshot["result"]["postUpdate"]["marketSnapshots"][0]["riskParameter"]["maintenance"] / 1e4
                min_maintenance = snapshot["result"]["postUpdate"]["marketSnapshots"][0]["riskParameter"]["minMaintenance"] / BIG_6_DIVISOR
            else:
                margin_fee = snapshot["postUpdate"]["marketSnapshots"][0]["riskParameter"]["margin"] / 1e4
                min_margin = snapshot["postUpdate"]["marketSnapshots"][0]["riskParameter"]["minMargin"] / BIG_6_DIVISOR
                maintenance_fee = snapshot["postUpdate"]["marketSnapshots"][0]["riskParameter"]["maintenance"] / 1e4
                min_maintenance = snapshot["postUpdate"]["marketSnapshots"][0]["riskParameter"]["minMaintenance"] / BIG_6_DIVISOR

            return {
                "market": symbol.upper(),
                "margin_fee": margin_fee,
                "min_margin": min_margin,
                "maintenance_fee": maintenance_fee,
                "min_maintenance": min_maintenance
            }
        
        except Exception as e:
            logger.error(f'market_info.py/fetch_margin_maintenance_info() - Error while fetching latest market price for market {symbol}. Error: {e}', exc_info=True)
            return None
