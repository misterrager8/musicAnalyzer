import random

from flask import Blueprint, render_template, request
from flask_login import current_user
from werkzeug.utils import redirect

from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Tag

tags = Blueprint("tags", __name__)
database = Database()


@tags.route("/tags_")
def tags_():
    return render_template("tags.html")


@tags.route("/tag_add", methods=["POST"])
def tag_add():
    database.add_multiple([Tag(name=i,
                               color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                               user_id=current_user.id) for i in request.form["name"].split(", ")])

    return redirect(request.referrer)


@tags.route("/tag_delete")
def tag_delete():
    _: Tag = database.get(Tag, int(request.args.get("id_")))
    database.delete_multiple([i for i in _.get_album_tags()])
    database.delete(_)

    return redirect(request.referrer)
