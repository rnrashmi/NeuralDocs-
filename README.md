## **Document Ingestion & RAG-based Q&A Backend**

A Python backend application for **document ingestion, embedding generation, and Retrieval-Augmented Generation (RAG)-based Q&A**, built with **Django REST Framework** and **Hugging Face Transformers**.

---

## **Features**

- 📄 **Document Ingestion API**: Accepts and stores documents with embeddings.
- ❓ **Q&A API**: Retrieves relevant documents and generates answers using RAG.
- 📑 **Document Selection API**: Filters documents for focused Q&A by title.
- 🔒 **Token Authentication**: Secure API access using Django Token Authentication.
- ⚡ **Asynchronous Processing**: Improves efficiency with async API handling.
- 🗄 **PostgreSQL + pgvector**: Stores embeddings for fast retrieval.
- 🔄 **Bulk Document Creation & Embeddings**: Generates fake documents and assigns embeddings.

---

## **Tech Stack & Dependencies**

- **Backend:** Django 4.2, Django REST Framework, Django Token Authentication
- **LLM & Embeddings:** Hugging Face Transformers
- **Database:** PostgreSQL with `pgvector`
- **Async Processing:** Django's async capabilities
- **Environment Management:** Python 3.9+, `venv`
- **Data Generation:** Faker for fake document creation

Install dependencies:

```sh
pip install -r requirements.txt
```

---

## **Setup & Running the Project**

### **1. Clone the Repository**

```sh
git clone https://github.com/rnrashmi/NeuralDocs-
cd NeuralDocs-
```

### **2. Set Up Virtual Environment**

```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3. Install Dependencies**

```sh
pip install -r requirements.txt
```

### **4. Configure PostgreSQL**

1. Install PostgreSQL and enable `pgvector` extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
2. Update `DATABASES` in `settings.py` using Django database URL:
   ```python
   import dj_database_url
   DATABASES = {
       'default': dj_database_url.config(default='postgres://your_user:your_password@localhost:5432/your_db')
   }
   ```

### **5. Run Migrations**

```sh
python manage.py migrate
```

### **6. Create a Superuser for Authentication**

```sh
python manage.py createsuperuser
```

Follow the prompts to set up an admin user.

### **7. Start the Django Server**

```sh
python manage.py runserver
```

---

## **Bulk Create Documents and Embeddings**

To generate **fake documents** and assign **fake embeddings**, run:

```sh
python manage.py bulk_create_embeddings
```

This will:
✅ Create **fake documents** (if none exist)
✅ Generate **randomized embeddings** for them
✅ Store the embeddings in PostgreSQL using `pgvector`

---

## **Document Selection API**

### **Use Case**
The **Document Selection API** allows users to **select documents by title** instead of ID for RAG-based Q&A. This enables dynamic filtering of relevant documents for better query responses.

### **Select Documents by Title**
```sh
curl -X POST http://127.0.0.1:8000/api/select/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token your_generated_token" \
     -d '{"titles": ["Document Title 1", "Document Title 2"]}'
```
Response:
```json
{
    "message": "Documents selected successfully",
    "selected_titles": ["Document Title 1", "Document Title 2"]
}
```


### **Clear Selected Documents**
```sh
curl -X DELETE http://127.0.0.1:8000/api/select/ \
     -H "Authorization: Token your_generated_token"
```
Response:
```json
{
    "message": "Document selection cleared"
}
```

---

## **Usage**

### **Authentication (Obtain Token)**

```sh
curl -X POST http://127.0.0.1:8000/api/token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

Response:

```json
{
    "token": "your_generated_token"
}
```

### **Ingest a Document (Authenticated Request)**

```sh
curl -X POST http://127.0.0.1:8000/api/ingest/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token your_generated_token" \
     -d '{"title": "Sample Doc", "content": "This is a test document"}'
```

### **Retrieve Answer using RAG (Authenticated Request)**

```sh
curl -X POST http://127.0.0.1:8000/api/qa/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token your_generated_token" \
     -d '{"query": "What is in the document?"}'
```

---
