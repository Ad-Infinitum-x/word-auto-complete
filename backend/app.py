from flask import Flask
from flask_cors import CORS
from db_utils import init_db
from bpe_utils import bpe_autocomplete, train_bpe

app = Flask(__name__)
CORS(app)
init_db(app)

bpe_model = train_bpe("hello, hella, helli, testing", vocab_size=1000)

@app.route('/autocomplete/<string:input_text>', methods=['GET'])
def autocomplete(input_text):
    suggestions = bpe_autocomplete(input_text, bpe_model)
    return {"suggestions": suggestions}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
