geminipy
=============

This is an asynchronous Python wrapper for the `Gemini API <https://docs.gemini.com/rest-api/#symbols>`_, implemented with the `aiohttp` module. Usage is as follows:

::

    from gemini import Gemini
    g = Gemini( 'PUBLIC_API_KEY', ['PRIVATE_API_KEY'] )
    
    ...
    
    import asyncio
    
    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        print( loop.run_until_complete( g.ticker( 'BTCUSD' ) ) )

or, of course, any other way that you would run an asynchronous task.