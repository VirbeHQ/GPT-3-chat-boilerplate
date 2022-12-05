from flask import Flask, request
from marshmallow import fields, Schema, ValidationError

from server.gpt3_wrapper import Gpt3Wrapper

app = Flask(__name__)


class UserActionSchema(Schema):
    text = fields.String(required=True)


class VirbeChatRequestSchema(Schema):
    userAction = fields.Nested(UserActionSchema(), required=True)
    conversationId = fields.UUID(required=True)
    endUserId = fields.UUID(required=True)
    languageCode = fields.String(required=False)
    context = fields.Raw(allow_none=True, required=False)


class CustomDataSchema(Schema):
    action = fields.String()
    payload = fields.String()
    data = fields.Raw()


class BeingActionSchema(Schema):
    text = fields.String()
    custom = fields.Nested(CustomDataSchema())


class IntentSchema(Schema):
    name = fields.String()
    confidence = fields.Number()


class VirbeChatResponseSchema(Schema):
    conversationId = fields.UUID(required=True)
    intent = fields.Nested(IntentSchema())
    beingActions = fields.List(fields.Nested(BeingActionSchema()), required=True)


wrapper = Gpt3Wrapper()

DEFAULT_RESPONSE = [{
    "text": "Are you ready for a hackathon?",
    "custom": {
        "action": "/areYouReady",
        "payload": "virbe",
        "data": {
            "ui": [
                {
                    "type": "button",
                    "title": "Almost",  # Title is what's displayed on the button in the web component
                    "payload": "No",  # Payload is sent to engine as text if user clicks the button
                },
                {
                    "type": "button",
                    "title": "Hell Yeah!",
                    "payload": "Yes",
                }, ]
        }
    }
}]


@app.route("/api/chat/", methods=["POST"])
def chat():
    json_data = request.get_json()

    requestSchema = VirbeChatRequestSchema()
    responseSchema = VirbeChatResponseSchema()
    if not json_data:
        return {"message": "No input data provided"}, 400

    try:
        data = requestSchema.load(data=json_data)
    except ValidationError as err:
        return err.messages, 422

    being_actions = DEFAULT_RESPONSE

    # TODO customise your own chat response
    # user_ask = data['userAction']['text']
    # gpt_response = wrapper.chat_with_gpt3(user_ask)
    # being_actions = [{
    #     "text": gpt_response
    # }]

    return responseSchema.dump({
        "intent": {"name": "default", "confidence": 1.0},
        "conversationId": data['conversationId'],
        "beingActions": being_actions
    })


if __name__ == '__main__':
    app.run(port=9000)
