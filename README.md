# **🚀 Shorten-URL: A Simple & Efficient URL Shortener**  

## **🔗 Introduction**  
Tired of long, messy URLs? **Shorten-URL** makes your links **shorter, cleaner, and easier to share** while also offering **tracking and customization**.  

Perfect for **social media, messaging, and marketing**, this service helps improve link engagement. While some platforms block unknown short URLs to prevent abuse, **responsible use makes URL shorteners a powerful tool for businesses and individuals alike**.  

---

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

---

## **📡 API Endpoints**  

| **Method** | **Endpoint**           | **Description** |
|-----------|----------------------|----------------------------------------------------------------|
| **POST**  | `/api/v1/shorten-data` | Generates a short URL from a given long URL. The client sends a **POST** request with the original URL. |
| **GET**   | `/{shorten_url}`       | Redirects users to the original long URL when they access a shortened link. The client sends a **GET** request with the short URL. |

---

## **⚡ Usage**  
🔨 **STATUS: In Progress** – Stay tuned for updates!  

---

## **👨‍💻 Maintainer**  
This project is maintained by:  
- **[Le Duc Minh](https://github.com/MinLee0210)**  

Feel free to contribute or reach out with ideas! 🚀  