# import websockets
# import asyncio
# import json
#
#
# async def receive_bitmex_data():
#     async with websockets.connect("wss://www.bitmex.com/realtime?subscribe=liquidation:XBTUSD") as ws:
#         try:
#             data = await asyncio.wait_for(ws.recv(), timeout=20)
#         except asyncio.TimeoutError:
#             try:
#                 pong_waiter = await ws.ping()
#                 await asyncio.wait_for(pong_waiter, timeout=10)
#             except asyncio.TimeoutError:
#                 raise
#         else:
#             print('.', end='', flush=True)
#             await handle_data(data)
#         print('Client closed')
#         ws.close()
#
# async def handle_data(data):
#     """ Liquidation messages look like this:
#      {
#        'table': 'liquidation',
#        'data':
#            [{
#              'orderID': '49fd4c3a-c832-dced-11d4-1e7042f97b62',
#              'price': 6705,
#              'side': 'Buy',
#              'leavesQty': 3,
#              'symbol': 'XBTUSD'
#            }],
#        'action': 'insert'
#      }
#     """
#     x = json.loads(data)
#     if 'table' in x and x['table'] == 'liquidation':
#         #print('########################### LIQUIDATION ###########################')
#         #print(x)
#         #await client.send_message(channel, x)
#         # XXX: Clean this mess up
#         if 'action' in x and x['action'] == 'insert':
#             if 'data' in x and isinstance(x['data'], list):
#                 side = 'short' if x['data'][0]['side'] == 'Buy' else 'long'
#                 liq_str = 'Liquidating ' + x['data'][0]['symbol'] + ' ' + side + ': ' + x['data'][0]['side'] + ' ' + str(x['data'][0]['leavesQty']) + ' at ' + str(x['data'][0]['price'])
#                 print(liq_str)

from bitmex_websocket import BitMEXWebsocket
import logging
from time import sleep


# Basic use of websocket.
def run():
    logger = setup_logger()

    # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.
    ws = BitMEXWebsocket(endpoint="wss://www.bitmex.com/realtime?subscribe=liquidation:XBTUSD", symbol="XBTUSD",
                         api_key=None, api_secret=None)

    logger.info("Instrument data: %s" % ws.get_instrument())

    # Run forever
    while(ws.ws.sock.connected):
        logger.info("Ticker: %s" % ws.get_ticker())
        if ws.api_key:
            logger.info("Funds: %s" % ws.funds())
        # logger.info("Market Depth: %s" % ws.market_depth())
        # logger.info("Recent Trades: %s\n\n" % ws.recent_trades())
        sleep(10)


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    run()