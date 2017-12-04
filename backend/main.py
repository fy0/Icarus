from app import app
import config

if __name__ == '__main__':
    import model._models
    import view._views
    app.run(host=config.HOST, port=config.PORT)
