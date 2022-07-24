from flask import abort, redirect, render_template, request
from http import HTTPStatus

from . import app, db
from .forms import LinkCreationForm
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkCreationForm()
    host_url = request.host_url
    if form.validate_on_submit():
        raw_id_data = form.custom_id.data
        if not raw_id_data.strip():
            custom_id = get_unique_short_id()
        else:
            custom_id = raw_id_data
        url_map = URL_map(original=form.original_link.data.strip(),
                          short=custom_id)
        success_msg = 'Ваша короткая ссылка готова: '
        db.session.add(url_map)
        db.session.commit()
        return render_template('homepage.html', form=form, host_url=host_url,
                               success_msg=success_msg, custom_id=custom_id)

    return render_template('homepage.html', form=form, host_url=host_url)


@app.route('/<custom_id>', methods=['GET'])
def long_link_view(custom_id):
    url_map = URL_map.query.filter_by(short=custom_id).first()
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    long_url = url_map.original
    return redirect(long_url, code=HTTPStatus.FOUND)
