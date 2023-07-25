# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to create a bot that demonstrates the following:
- Use [LUIS](https://www.luis.ai) to implement core AI capabilities.
- Implement a multi-turn conversation using Dialogs.
- Handle user interruptions for such things as `Help` or `Cancel`.
- Prompt for and validate requests for information from the user.
"""
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity

from config import DefaultConfig
from dialogs import MainDialog, BookingDialog
from bots import DialogAndWelcomeBot

from adapter_with_error_handler import AdapterWithErrorHandler
from flight_booking_recognizer import FlightBookingRecognizer

import logging
logger = logging.getLogger()
#logger.setLevel(logging.INFO)

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)

# Create MemoryStorage, UserState and ConversationState
MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
ADAPTER = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)

# Create dialogs and Bot
RECOGNIZER = FlightBookingRecognizer(CONFIG)
BOOKING_DIALOG = BookingDialog()
DIALOG = MainDialog(RECOGNIZER, BOOKING_DIALOG)
BOT = DialogAndWelcomeBot(CONVERSATION_STATE, USER_STATE, DIALOG)
logger.info('print_debug04')

async def hello(req:Request):
    logger.info('hello')
    logger.info(f'request == {req}')
    if req.method == "POST":
        logger.info('inside_post')
    else:
        logger.info(f'outside_post {req.method}')
        #logger.info(req.method)

    return Response(text="Hello, World!")

def init_func(argv):
    logger.info('print_init_func')
    app = web.Application()
    logger.info('line63')
    app.router.add_post('/api/messages',hello)
    logger.info('line65')
    return app

if __name__ == '__main__':
    logger.info('print_main')
    APP = init_func(None)
    web.run_app(APP, host="0.0.0.0", port=CONFIG.PORT)

'''
# Listen for incoming requests on /api/messages.
async def messages(req: Request) -> Response:
    print('debug03')
    print(req.method)
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

def init_func(argv):
    print('debug02')
    APP = web.Application()
    APP.router.add_post("/api/messages", messages)
    return APP

if __name__ == "__main__":
    print('debug01')
    APP = init_func(None)
    web.run_app(APP, host='0.0.0.0', port=8000)
    #try:
    #    web.run_app(APP, host="0.0.0.0", port=CONFIG.PORT)
    #except Exception as error:
    #    raise error
'''