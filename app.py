from flask import Flask, request
from marshmallow import fields, Schema, ValidationError

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

    # TODO write code to make your own

    return responseSchema.dump({
        "userAction": data['userAction'],
        "sessionId": data['sessionId'],
        "beingAction": {
            "text": "Are you ready for a hackathon?",
            "custom": {
                "action": "/areYouReady",
                "payload": "button",
                "data": [
                    {
                        "title": "Yes",
                        "payload": "Yes",
                    },
                    {
                        "title": "No",
                        "payload": "Yes",
                    },
                ]
            }
        }
    })


if __name__ == '__main__':
    app.run(port=9000)
