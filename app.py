from flask import Flask
from config.config import Config  # 修改导入路径

def create_app():
    app = Flask(
        __name__,
        static_folder=Config.STATIC_FOLDER,
        template_folder=Config.TEMPLATE_FOLDER
    )
    app.config.from_object(Config)
    Config.init_app(app)
    
    # 注册蓝图（示例）
    from web.controller.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True