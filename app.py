import logging
from flask import Flask
from lark_oapi.adapter.flask import *
from lark_oapi.event import EventDispatcherHandler
import lark_oapi.api.im.v1 as im

from config import config
from core.processor import MessageProcessor

app = Flask(__name__)

# Initialize Processor
processor = MessageProcessor()

# Event Handler
def do_p2_im_message_receive_v1(data: im.P2ImMessageReceiveV1) -> None:
    # Offload processing to avoid blocking the webhook response
    # In production, use Celery/Redis Queue
    try:
        processor.handle_im_message_receive_v1(data.event)
    except Exception as e:
        logging.error(f"Error processing event: {e}")

# Register Handler
handler = EventDispatcherHandler.builder(config.ENCRYPT_KEY, config.VERIFICATION_TOKEN, lark.LogLevel.DEBUG) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .build()

@app.route("/webhook/event", methods=["POST"])
def event():
    resp = handler.do(parse_req())
    return parse_resp(resp)

if __name__ == "__main__":
    app.run(port=config.PORT, host="0.0.0.0")
