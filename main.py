import os
from datetime import datetime, timezone
from typing import Optional, Dict

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

from app.document_image_processor import DocumentImageProcessor
from app.db_model import DBModel, Survey, db, Interactions, Records
from app.chabot_session import ChatbotSession
from config.conf import API_KEY, SECRET_KEY, SQLALCHEMY_DATABASE_URI
from http import HTTPStatus

class ChatbotAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_app_config()
        self.campaign = 'USA_bot_IA'
        self.db_model = DBModel(self.app)
        self.chat_session = ChatbotSession()
        CORS(self.app)
        self.setup_routes()

    def setup_app_config(self) -> None:
        """Initialize Flask application configuration."""
        self.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        self.app.config['SECRET_KEY'] = SECRET_KEY

    def setup_routes(self) -> None:
        """Setup all application routes."""
        self.app.route('/')(self.home)
        self.app.route('/form')(self.form)
        self.app.route('/login', methods=['POST'])(self.login)
        self.app.route('/chat', methods=['POST'])(self.chat)
        self.app.route('/buttonchat/<path:filename>')(self.serve_script)
        self.app.route('/prueba')(self.prueba)
        self.app.route('/logout', methods=['GET'])(self.logout)
        self.app.route('/survey', methods=['GET'])(self.survey)
        self.app.route('/webhookSurvey', methods=['POST'])(self.survey_logout)

    def home(self):
        return render_template('index.html')

    def form(self):
        return render_template('form.html')

    def login(self):
        try:
            data = request.json
            guid = data['guid']
            name = data['name']
            mail = data['mail']

            if guid not in self.chat_session.active_chatbots:
                initial_message = f'Nombre del usuario: {name}'
                self.chat_session.create_session(
                    guid, 
                    API_KEY, 
                    'data/data.csv', 
                    'data/embeddings.csv', 
                    initial_message, 
                )

            self._save_user_record(guid, name, mail)
            return jsonify(success=True)

        except KeyError as e:
            return jsonify({'error': f'Missing required field: {str(e)}'}), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    def chat(self):
        try:
            data = request.json
            conversation = data['conversation']
            question = data['question']
            guid = data['guid']

            if not guid:
                return jsonify({'error': 'Chatbot session not found'}), HTTPStatus.BAD_REQUEST

            chatbot = self.chat_session.get_chatbot(guid)
            if not chatbot:
                # Try to get user info from Records table
                user_record = Records.query.filter_by(guid=guid).first()
                if not user_record:
                    return jsonify({'error': 'User record not found'}), HTTPStatus.BAD_REQUEST
                
                # Create new chatbot session
                initial_message = f'Nombre del usuario: {user_record.name}'
                self.chat_session.create_session(
                    guid, 
                    API_KEY, 
                    'data/data.csv', 
                    'data/embeddings.csv', 
                    initial_message
                )
                chatbot = self.chat_session.get_chatbot(guid)

            answer = chatbot.ask_question(question)
            self._save_interaction(guid, question, answer)

            return jsonify({
                'answer': answer, 
                'conversation': conversation
            })

        except Exception as e:
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    def serve_script(self, filename):
        return send_from_directory(
            os.path.join(self.app.root_path, 'static', 'buttonchat'),
            filename
        )

    def prueba(self):
        return render_template('Prueba.html')

    def logout(self):
        guid = request.args.get('guid')
        if guid:
            self.chat_session.remove_session(guid)
        return 'Sesión cerrada', HTTPStatus.OK

    def survey(self):
        return render_template('survey.html')

    def survey_logout(self):
        try:
            data = request.json
            self._save_survey(
                guid=data['guid'],
                rating1=data['rating'],
                rating2=data['rating2']
            )
            return 'Survey data received and saved successfully', HTTPStatus.OK
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    def _save_user_record(self, guid: str, name: str, mail: str) -> None:
        """Save user record to database."""
        record = Records(
            guid=guid,
            name=name,
            campaign=self.campaign,
            mail=mail,
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(record)
        db.session.commit()

    def _save_interaction(self, guid: str, question: str, answer: str) -> None:
        """Save chat interaction to database."""
        interaction = Interactions(
            guid=guid,
            prompt=question,
            response=answer,
            timestamp=datetime.now(timezone.utc),
            campaign=self.campaign
        )
        db.session.add(interaction)
        db.session.commit()

    def _save_survey(self, guid: str, rating1: int, rating2: int) -> None:
        """Save survey response to database."""
        survey = Survey(
            guid=guid,
            campaign=self.campaign,
            rating1=rating1,
            rating2=rating2,
        )
        db.session.add(survey)
        db.session.commit()

    def run(self, host: str = '0.0.0.0', port: str = '8000', debug: bool = True) -> None:
        """Run the Flask application."""
        self.app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    api = ChatbotAPI()
    api.run()
