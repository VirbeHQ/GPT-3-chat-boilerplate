from flask import Flask, request
from marshmallow import fields, Schema, ValidationError

app = Flask(__name__)

class UserActionSchema(Schema):
    text = fields.String()
    languageCode = fields.String()


class VirbeChatRequestSchema(Schema):
    userAction = fields.Nested(UserActionSchema())
    sessionId = fields.UUID()


class BeingActionSchema(Schema):
    text = fields.String()
    languageCode = fields.String()


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

    return responseSchema.dump({
        "userAction": data['userAction'],
        "sessionId": data['sessionId'],
        "beingAction": {
            "text": "TODO custom chat response"
        }
    })


if __name__ == '__main__':
    app.run(port=9000)
