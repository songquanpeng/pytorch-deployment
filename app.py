import jinja2
from flask import Flask, render_template

from utils import load_cfg

cfg = load_cfg()
app = Flask(__name__)


@app.context_processor
def inject_config():
    return dict(cfg=cfg)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/model/<model_name>', methods=['GET'])
def model(model_name):
    try:
        return render_template(f'{model_name}.html', title=model_name)
    except jinja2.exceptions.TemplateNotFound:
        return render_template('index.html', message=f'No such model: {model_name}.', is_warning=True)


@app.route('/api/<model_name>', methods=['POST'])
def predict(model_name):
    return {
        "success": True,
        "message": model_name
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=cfg.port)
