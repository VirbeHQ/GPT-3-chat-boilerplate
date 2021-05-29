from flask import Flask, request
from marshmallow import fields, Schema, ValidationError

from server.gpt3_wrapper import Gpt3Wrapper

app = Flask(__name__)


class UserActionSchema(Schema):
    text = fields.String()
    languageCode = fields.String()


class VirbeChatRequestSchema(Schema):
    userAction = fields.Nested(UserActionSchema())
    sessionId = fields.UUID()


class CustomDataSchema(Schema):
    action = fields.String()
    payload = fields.String()
    data = fields.Raw()


class BeingActionSchema(Schema):
    text = fields.String()
    languageCode = fields.String()
    custom = fields.Nested(CustomDataSchema())


class VirbeChatResponseSchema(Schema):
    userAction = fields.Nested(UserActionSchema())
    sessionId = fields.UUID()
    beingAction = fields.Nested(BeingActionSchema())


wrapper = Gpt3Wrapper()

DEFAULT_RESPONSE = {
    "text": "Are you ready for a hackathon?",
    "custom": {
        "action": "/areYouReady",
        "payload": "button",
        "data": [
            {
                "title": "Almost",  # Title is what's displayed on the button in the web component
                "payload": "No",  # Payload is sent to engine as text if user clicks the button
            },
            {
                "title": "Hell Yeah!",
                "payload": "Yes",
            },
        ]
    }
}


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

    being_action = DEFAULT_RESPONSE
    # TODO customise your own chat response
    # gpt_response = wrapper.chat_with_gpt3(data['userAction']['text'])
    # being_action = {
    #     "text": gpt_response
    # }

    return responseSchema.dump({
        "userAction": data['userAction'],
        "sessionId": data['sessionId'],
        "beingAction": being_action
    })


if __name__ == '__main__':
    app.run(port=9000)
