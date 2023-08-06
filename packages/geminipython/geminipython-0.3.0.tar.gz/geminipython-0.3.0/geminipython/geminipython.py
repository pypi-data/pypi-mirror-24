import aiohttp
import json
from time import time
from base64 import b64encode
import hmac
from hashlib import sha384


class Gemini( object ):
	def __init__( self, public, private=None ):
		self.__apiBase = 'https://api.gemini.com'
		self.__public = public
		self.__private = private

	async def __apiGetReq( self, command, args=None ):
		args = { }
		baseUrl = self.__apiBase + command

		async with aiohttp.ClientSession() as session:
			async with session.get( baseUrl, params=args ) as res:
				return await res.json()

	async def __apiPostReq( self, command, args=None ):
		if args is None:
			args = { }
		baseUrl = self.__apiBase + command
		args[ 'nonce' ] = int( round( time() * 1000 ) )
		args[ 'request' ] = command

		argString = json.dumps( self.__convertDictItemsToStr( args ) )
		argStringb64 = b64encode( bytes( argString, "utf-8" ) ).decode( "utf-8" )
		signature = hmac.new(
				bytes( self.__private, 'utf-8' ),
				bytes( argStringb64, 'utf-8' ),
				sha384 )
		headerPayload = {
			'X-GEMINI-APIKEY': self.__public,
			'X-GEMINI-PAYLOAD': argStringb64,
			'X-GEMINI-SIGNATURE': signature.hexdigest()
		}

		async with aiohttp.ClientSession() as session:
			async with session.post( baseUrl, headers=headerPayload ) as res:
				return await res.json()

	# thanks, https://stackoverflow.com/a/7027514
	def __convertDictItemsToStr( self, params ):
		if not isinstance( params, dict ):
			return params
		return dict( (str( k ), self.__convertDictItemsToStr( v )) for k, v in params.items() )

	########################
	# Public API Endpoints #
	########################

	def symbols( self ):
		return self.__apiGetReq( '/v1/symbols', args={ } )

	def ticker( self, symbol ):
		return self.__apiGetReq( '/v1/pubticker/' + symbol, args={ } )

	def currentOrderBook( self, symbol, limitBids=50, limitAsks=50 ):
		return self.__apiGetReq( '/v1/book/' + symbol, args={
			'limit_bits': limitBids,
			'limit_asks': limitAsks
		} )

	def tradeHistory( self, symbol, timestamp=None, limitTrades=50, includeBreaks=False ):
		args = {
			'limit_trades': limitTrades,
			'include_breaks': includeBreaks
		}

		if timestamp is not None:
			args[ 'timestamp' ] = timestamp

		return self.__apiGetReq( '/v1/trades/' + symbol, args=args )

	def currentAuction( self, symbol ):
		return self.__apiGetReq( '/v1/auction/' + symbol, args={ } )

	def auctionHistory( self, symbol, since=None, limitAuctionResults=50, includeIndicative=True ):
		args = {
			'limit_auction_results': limitAuctionResults,
			'include_indicative': includeIndicative
		}

		if since is not None:
			args[ 'since' ] = since

		return self.__apiGetReq( '/v1/auction/' + symbol + '/history' )

	########################
	# Order Placement APIs #
	########################

	def newOrder( self, symbol, amount, price, side, type, clientOrderId=None, options=None ):
		args = {
			'symbol': symbol,
			'amount': amount,
			'price': price,
			'side': side,
			'type': type,
		}

		if options is not None:
			# options:
			# "maker-or-cancel", "immediate-or-cancel", "auction-only"
			args[ 'option' ] = options
		if clientOrderId is not None:
			args[ 'client_order_id' ] = clientOrderId

		return self.__apiPostReq( "/v1/order/new", args=args )

	def cancelOrder( self, orderId ):
		return self.__apiPostReq( "/v1/order/cancel", args={
			'order_id': orderId
		} )

	def cancelAllSessionOrders( self ):
		return self.__apiPostReq( '/v1/order/cancel/session' )

	def cancelAllActiveOrders( self ):
		return self.__apiPostReq( '/v1/order/cancel/all' )

	#####################
	# Order Status APIs #
	#####################

	def orderStatus( self, orderId ):
		return self.__apiPostReq( '/v1/order/status', args={
			'order_id': orderId
		} )

	def getActiveOrders( self ):
		return self.__apiPostReq( '/v1/orders' )

	def getPastTrades( self, symbol, limitTrades=50, timestamp=None ):
		args = {
			'symbol': symbol,
			'limit_trades': limitTrades
		}

		if timestamp is not None:
			args[ 'timestamp' ] = timestamp

		return self.__apiPostReq( '/v1/mytrades', args=args )

	def getTradeVolume( self ):
		return self.__apiPostReq( '/v1/tradevolume' )

	########################
	# Fund Management APIs #
	########################

	def getAvailableBalances( self ):
		return self.__apiPostReq( '/v1/balances' )

	def newDepositAddress( self, currency, label=None ):
		args = { }
		if label is not None:
			args[ 'label' ] = label

		return self.__apiPostReq( '/v1/deposit/' + currency + '/newAddress', args=args )

	def withdrawCryptoFunds( self, currency, address, amount ):
		return self.__apiPostReq( '/v1/withdraw/' + currency, args={
			'address': address,
			'amount': amount
		} )

	################
	# Session APIs #
	################

	def heartbeat( self ):
		return self.__apiPostReq( '/v1/heartbeat', args={ } )
