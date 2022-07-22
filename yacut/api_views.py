import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_custom_id():
    incoming_data = request.get_json()
    if incoming_data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in incoming_data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if 'custom_id' in incoming_data and incoming_data['custom_id'] is not None:
        short = incoming_data['custom_id']
        if short.strip() == '':
            short = get_unique_short_id()
        else:
            existing_url_map = URL_map.query.filter_by(short=short).first()
            if existing_url_map is not None:
                raise InvalidAPIUsage(f'Имя "{short}" уже занято.')
            permitted_symbols = re.compile('^[A-Za-z0-9]{1,16}$')
            if not permitted_symbols.match(short):
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки'
                )
    elif 'custom_id' not in incoming_data or incoming_data['custom_id'] is None:
        incoming_data['custom_id'] = get_unique_short_id()

    url_map = URL_map()
    url_map.from_dict(incoming_data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_page(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    long_url = URL_map.query.filter_by(short=short_id).first().original
    return jsonify({'url': long_url}), 200
