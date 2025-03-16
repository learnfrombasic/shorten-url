# **🚀 Shorten-URL: A Simple & Efficient URL Shortener**  

## **🔗 Introduction**  
Tired of long, messy URLs? **Shorten-URL** makes your links **shorter, cleaner, and easier to share** while also offering **tracking and customization**.  

Perfect for **social media, messaging, and marketing**, this service helps improve link engagement. While some platforms block unknown short URLs to prevent abuse, **responsible use makes URL shorteners a powerful tool for businesses and individuals alike**.  


## **📂 Project Structure**  
The project is organized as follows:  

```
.
├── app
│   ├── api         # API Endpoints
│   ├── common      # Common utilities
│   ├── core        # Core logic and configurations
│   ├── models      # Database models
│   ├── modules     # Main processing modules
│   └── services    # Service layer
├── assets          # Static assets (if any)
├── compose         # Docker-related configurations
├── poc             # Proof of Concept - Example implementations
└── test            # Unit and integration tests
```


## **📡 API Endpoints**  

| **Method** | **Endpoint**           | **Description** |
|-----------|----------------------|----------------------------------------------------------------|
| **POST**  | `/api/v1/shorten-data` | Generates a short URL from a given long URL. The client sends a **POST** request with the original URL. |
| **GET**   | `/{shorten_url}`       | Redirects users to the original long URL when they access a shortened link. The client sends a **GET** request with the short URL. |


### **⚡ Usage**  

You can run the **Shorten-URL** service using either **Python's virtual environment** or **Docker Compose**.


### **1️⃣ Use with Python's Environment** 🐍  

#### **🔹 Prerequisites**  
- Python **3.8+** installed  
- Virtual environment setup (recommended)  

#### **🔹 Steps**  

```bash
# Clone the repository
git clone https://github.com/yourusername/shorten-url-service.git
cd shorten-url-service

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (or create a .env file)
export HOST=0.0.0.0
export PORT=1802
export DATABASE_URL="mongodb://localhost:27017/shorten-url"

# Run the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 1802 --reload
```

Now, the service should be running at **http://localhost:1802** 🚀.

**Note:** I highly recommend using `uv` for initializing python's virtual environment.


### **2️⃣ Use with `docker-compose` 🐳**  

#### **🔹 Prerequisites**  
- **Docker** and **Docker Compose** installed  

#### **🔹 Steps**  

```bash
# Clone the repository
git clone https://github.com/learnfrombasic/shorten-url.git
cd shorten-url-service

# Build and start the service
docker-compose up --build
```

This will:  
✅ **Build the Docker image**  
✅ **Start the service on port 1802**  

Once running, access the service at:  
👉 **http://localhost:1802**  

To stop the service, run:
```bash
docker-compose down
```


## **👨‍💻 Maintainer**  
This project is maintained by:  
- **[Le Duc Minh](https://github.com/MinLee0210)**  

Feel free to contribute or reach out with ideas! 🚀  