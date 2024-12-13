# Bangkit Academy 2024 - Product-Based Capstone Team - C242-PS507 

## 📖 My SunSign - Cloud Computing

My SunSign is an innovative application that interprets and translates hand signs into meaningful text using advanced image processing and machine learning techniques.

### Role of Cloud Computing in My SunSign

Cloud computing enables My SunSign to process images, make predictions, and store data efficiently. It provides scalability and reliability, ensuring the application can handle multiple requests simultaneously.

### Cloud Computing Services Used

#### Cloud Engine

Used for deploying and managing application services, ensuring high availability and performance.

#### Firebase Authentication

Provides secure authentication mechanisms for user management and data protection.

#### Cloud Storage

Stores and serves user-uploaded images and static resources efficiently.

#### Google Cloud Monitoring and Logging

Monitors application performance and provides real-time analytics and logging for troubleshooting.

## API Backend

The API backend is built using FastAPI and TensorFlow, handling image predictions and database operations.

[API Backend Repository](https://github.com/your-repo-link)

## Installation Instructions API Backend

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-repo-link.git
    ```

2. **Navigate to the application directory**:

    ```bash
    cd your-app-directory
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    Create a [.env](http://_vscodecontentref_/0) file and specify the model path:

    ```env
    MODEL_PATH=path_to_your_model
    ```

5. **Run the application**:

    ```bash
    uvicorn app.main:app --reload
    ```

## Testing the API

You can test the API using `curl` or tools like **Postman**.

### Predict Endpoint

```bash
curl -X POST "http://localhost:8000/predict/" -F "file=@path_to_your_image.jpg"