from google.cloud import firestore
from google.cloud import storage
from dotenv import load_dotenv

db = firestore.Client()
storage_client = storage.Client()

class ImageDatabase:
    def __init__(self):
        self.collection = db.collection('images')
        self.bucket = storage_client.bucket('sunsign-drive')

    def add_image(self, title, image_url):
        doc_ref = self.collection.document(title)
        doc_ref.set({
            'title': title,
            'image_url': image_url
        })

    def get_image(self, title):
        doc_ref = self.collection.document(title)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    def delete_image(self, title):
        doc_ref = self.collection.document(title)
        doc_ref.delete()

    def search_images(self, query):
        return self.collection.where('title', '>=', query).where('title', '<=', query + '\uf8ff').get()

    def populate_database(self):
        characters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + ['nothing', 'space', 'del']
        for char in characters:
            image_url = f'https://storage.googleapis.com/sunsign-drive/{char}.jpg'
            self.add_image(char, image_url)
