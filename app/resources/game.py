from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import UserModel, GameModel, WordModel


class Games(Resource):
    @jwt_required
    def post(self):
        """
            Create Game
            Creates a new game and returns it`s model
            ---
            tags:
              - Games API
            responses:
              500:
                description: Internal Server Error
              201:
                description: A new game was created
                schema:
                  id: game
                  properties:
                    id:
                      type: string
                      description: The game id
                      default: 5e090b871462bac3017889f8
                    lives:
                      type: integer
                      description: how many mistakes can user make
                      default: 5
                    named_letters:
                      type: array
                      description: named letters container
                      items:
                        type: string
                      default: []
                    disguised_word:
                      type: string
                      description: word with masked letters
                      default: _ _ _ _ _ _
                    state:
                      type: string
                      description: Current status of the game
                      enum: [FAILED, SUCCEEDED, IN PROGRESS]
                      default: IN PROGRESS
                    started_at:
                      type: string
                      description: timestamp of the game beginning
                      default: 2019-12-29 20:24:39.893884
                    score:
                      type: number
                      description: Score, calculated when the game is finished
                      default: 0
        """
        user = UserModel.objects.get(pk=get_jwt_identity())
        word = WordModel.get_random_word()
        game = GameModel(author=user, word=word).save()

        return game.serialize(), HTTPStatus.CREATED


class Game(Resource):
    @jwt_required
    def get(self, game_id):
        """
            Retrieve Game
            Returns the game model in the current condition
            ---
            tags:
              - Games API
            parameters:
              - name: game_id
                in: path
                type: string
                required: true
                description: The game id
            responses:
              500:
                description: Internal Server Error
              200:
                description: The game was successfully returned
                schema:
                  id: game
        """
        game = GameModel.objects.get(pk=game_id)

        return game.serialize(), HTTPStatus.OK


class GameTurn(Resource):
    @jwt_required
    def post(self, game_id):
        """
            Create Game Turn
            Saves the certain game turn and returns the game model with the turn applied
            ---
            tags:
              - Games API
            parameters:
              - name: game_id
                in: path
                type: string
                required: true
                description: The game id
              - name: body
                in: body
                required: true
                schema:
                  id: turn
                  required:
                    - letter
                  properties:
                    letter:
                      type: string
                      description: A letter which the user thinks in the word
                      default: "F"
            responses:
              500:
                description: Internal Server Error
              200:
                description: The turn was successfully saved
                schema:
                  id: game
        """
        data = request.get_json()
        game = GameModel.objects.get(pk=game_id)
        if game.is_pending():
            game.make_turn(data['letter'])

        return game.serialize(), HTTPStatus.CREATED
