#!/usr/bin/python
# coding: utf-8
from flask import Flask


from flask import  request, jsonify, render_template, redirect

from petfinder.database import db_session
from petfinder.models import PetRecord

app = Flask(__name__)

def is_array_included(array1, array2):
    retval = True
    for item_from_1 in array1:
        if item_from_1 not in array2:
            retval = False
            break
    return retval

def create_app():
    @app.route('/petrecords/del/<int:id>', methods=["POST", "GET"])
    def petrecords_del(id):
        rec_to_delete = PetRecord.query.filter_by(id=id)
        rec_to_delete.delete()

        db_session.commit()

        return redirect("/petrecords", code=302)

    @app.route('/petrecords/add', methods=['POST','GET'])
    def petrecord_add():
        if request.method == "POST":
            name = request.form["name"]
            phone = request.form["phone"]
            type = request.form["type"]
            color = request.form["color"]
            desc = request.form["desc"]
            new_pet_record = PetRecord(name=name, phone=phone, type=type, color=color, desc=desc)
            db_session.add(new_pet_record)
            db_session.commit()

            return redirect("/petrecords", code=302)
        else:
            petrecords = PetRecord.query.all()
            return render_template('petrecord_add.html', petrecords=petrecords)

    @app.route('/')
    @app.route('/petrecords',methods=['POST','GET'])
    def petrecords():
        tags_par = ''
        petrecords = PetRecord.query.all()
        records_to_send = petrecords
        if request.method == "POST":
            tags_filter = request.form["tags"].split(' ')
            if len(tags_filter) > 0 and tags_filter[0] != '':
                tags_par = request.form["tags"]
                records_to_send = []
                for rec in petrecords:
                    tags = rec.tags.split(',')
                    if is_array_included(tags_filter, tags):
                        records_to_send.append(rec)
        context = {}
        context['petrecords']=records_to_send
        context['filter'] = tags_par

        return render_template('list.html', context=context)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)