from flask import Flask, request, render_template, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('cem-certificate-firebase-adminsdk-r5fi0-101f5161fa.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

COLLECTION_NAME = 'certificate_list'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create_document():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'search_id': request.form['search_id'],
            'SEM': request.form['SEM'],
            'certificate_id': request.form['certificate_id'],
            'POS': request.form['POS'],
            'organizer_name': "CEMP",
            'event_name': request.form['event'] ,
            'event': request.form['event']  # New field
        }
        try:
            db.collection(COLLECTION_NAME).add(data)
            flash('Document created successfully.')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error creating document: {e}')
    return render_template('create_document.html')

    @app.route('/create_custom', methods=['GET', 'POST'])
def create_custom():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'search_id': request.form['search_id'],
            'SEM': request.form['SEM'],
            'certificate_id': request.form['certificate_id'],
            'POS': request.form['POS'],
            'organizer_name': "CEMP",
            'event_name': request.form['event'] ,
            'event': request.form['event']  # New field
        }
        try:
            db.collection(COLLECTION_NAME).add(data)
            flash('Document created successfully.')
            return redirect(url_for('create_custom'))
        except Exception as e:
            flash(f'Error creating document: {e}')
    return render_template('custom_add.html')

@app.route('/read', methods=['GET', 'POST'])
def read_documents_by_search_id():
    documents = None
    if request.method == 'POST':
        search_id = request.form['search_id']
        try:
            docs = db.collection(COLLECTION_NAME).where('search_id', '==', search_id).stream()
            documents = {doc.id: doc.to_dict() for doc in docs}
            if not documents:
                flash('No documents match the search_id.')
        except Exception as e:
            flash(f'Error reading documents: {e}')
    return render_template('read_document.html', documents=documents)

@app.route('/update', methods=['GET', 'POST'])
def update_document():
    if request.method == 'POST':
        doc_id = request.form['doc_id']
        update_data = {}
        if request.form['name']:
            update_data['name'] = request.form['name']
        if request.form['search_id']:
            update_data['search_id'] = request.form['search_id']
        if request.form['SEM']:
            update_data['SEM'] = request.form['SEM']
        if request.form['certificate_id']:
            update_data['certificate_id'] = request.form['certificate_id']
        if request.form['POS']:
            update_data['POS'] = request.form['POS']
        if request.form['event']:  # New field
            update_data['event'] = request.form['event']
        try:
            db.collection(COLLECTION_NAME).document(doc_id).update(update_data)
            flash('Document updated successfully.')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error updating document: {e}')
    return render_template('update_document.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_document():
    if request.method == 'POST':
        doc_id = request.form['doc_id']
        try:
            db.collection(COLLECTION_NAME).document(doc_id).delete()
            flash('Document deleted successfully.')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error deleting document: {e}')
    return render_template('delete_document.html')

if __name__ == '__main__':
    app.run(debug=True)
