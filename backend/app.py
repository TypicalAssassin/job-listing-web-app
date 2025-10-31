from flask import Flask
from flask_cors import CORS
from config import Config
from db import db, init_db
from routes.job_routes import job_bp

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS for frontend communication
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(job_bp)
    
    # Root endpoint
    @app.route('/')
    def home():
        return {
            'message': 'Job Listing API',
            'endpoints': {
                'GET /api/jobs': 'Get all jobs',
                'GET /api/jobs/<id>': 'Get single job',
                'POST /api/jobs': 'Create new job',
                'PUT /api/jobs/<id>': 'Update job',
                'DELETE /api/jobs/<id>': 'Delete job'
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)