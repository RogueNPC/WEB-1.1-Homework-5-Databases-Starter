from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

############################################################
# SETUP
############################################################

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/plantsDatabase"
mongo = PyMongo(app)

plants_collection = mongo.db.plants
harvests_collection = mongo.db.harvests

############################################################
# ROUTES
############################################################

@app.route('/')
def plants_list():
    """Display the plants list page."""

    plants_data = plants_collection.find()

    context = {
        'plants': plants_data,
    }
    return render_template('plants_list.html', **context)

@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    if request.method == 'POST':
        new_plant = {
            'name': request.form.get('plant_name'),
            'variety': request.form.get('variety'),
            'photo_url': request.form.get('photo'),
            'date_planted': request.form.get('date_planted')
        }
        returned_obj = plants_collection.insert_one(new_plant)
        # {'_id': ObjectId('5fc82959f7e05cf1fe55d433'), 'name': 'Cranberry', 'variety': 'Fruit', 'photo_url': '', 'date_planted': '2020-12-01'}
        return redirect(url_for('detail', plant_id=returned_obj.inserted_id))

    else:
        return render_template('create.html')

@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""

    plant_to_show = plants_collection.find_one({'_id': ObjectId(plant_id)})

    # TODO: Use the `find` database operation to find all harvests for the
    # plant's id.
    # HINT: This query should be on the `harvests` collection, not the `plants`
    # collection.
    harvests = harvests_collection.find({'_id': ObjectId(plant_id)})

    context = {
        'plant' : plant_to_show,
        'harvests': harvests
    }
    return render_template('detail.html', **context)

@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """
    Accepts a POST request with data for 1 harvest and inserts into database.
    """

    # TODO: Create a new harvest object by passing in the form data from the
    # detail page form.
    new_harvest = {
        'quantity': '', # e.g. '3 tomatoes'
        'date': '',
        'plant_id': plant_id
    }

    # TODO: Make an `insert_one` database call to insert the object into the 
    # `harvests` collection of the database.

    return redirect(url_for('detail', plant_id=plant_id))

@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    if request.method == 'POST':
        # TODO: Make an `update_one` database call to update the plant with the
        # given id. Make sure to put the updated fields in the `$set` object.

        
        return redirect(url_for('detail', plant_id=plant_id))
    else:
        # TODO: Make a `find_one` database call to get the plant object with the
        # passed-in _id.
        plant_to_show = ''

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    # TODO: Make a `delete_one` database call to delete the plant with the given
    # id.

    # TODO: Also, make a `delete_many` database call to delete all harvests with
    # the given plant id.

    return redirect(url_for('plants_list'))

if __name__ == '__main__':
    app.run(debug=True)

