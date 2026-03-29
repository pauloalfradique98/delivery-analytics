from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.dashboard import dashboard_bp
    from app.routes.bairros import bairros_bp
    from app.routes.metricas import metricas_bp
    from app.routes.historico import historico_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(bairros_bp)
    app.register_blueprint(metricas_bp)
    app.register_blueprint(historico_bp)

    return app