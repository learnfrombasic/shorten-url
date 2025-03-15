# 🚀 URL Shortening Algorithms: A Comparison

There are several algorithms for **URL shortening**, each with different trade-offs in efficiency, uniqueness, and readability.

---

## **1️⃣ Hashing (SHA-256, MD5, MurmurHash, etc.)**
### **How It Works:**
- Uses a **hash function** to generate a unique short key from the original URL.
- The **first few characters** of the hash serve as the short URL.
- **Collision handling** can be done using a **predefined salt** or additional randomness.

### **Pros:**
✔️ No need for a **database** (stateless).  
✔️ Deterministic (same URL → same short URL).  
✔️ Good for **one-time usage** when retrieval isn't needed.

### **Cons:**
❌ **Collisions** are possible, requiring retries.  
❌ Hashes can be **longer** than necessary.  

✅ **Best for:** **Stateless** systems where storing mappings isn’t feasible.

---

## **2️⃣ Base Encoding (Base-62, Base-24, Base-58, etc.)**
### **How It Works:**
- Converts a **unique integer ID** into a **shortened URL** using a custom character set.
- Example encodings:
  - **Base-62** → `[0-9a-zA-Z]` (62 possible characters).
  - **Base-24** → `[A-Z, 2-9]` (avoids ambiguous characters like `0, O, 1, I`).

### **Pros:**
✔️ **Shorter URLs** than hashing.  
✔️ **No collisions** (since it's based on unique IDs).  
✔️ **Easy to decode** back to the original ID.

### **Cons:**
❌ Requires a **database** to store mappings.  
❌ Random ID generation needs extra bookkeeping.

✅ **Best for:** High-performance URL shortening like **Bit.ly & TinyURL**.

---

## **3️⃣ Counter-Based (Auto-Incrementing ID)**
### **How It Works:**
- Uses a **global counter** for unique IDs.
- The ID is **Base-encoded** (e.g., Base-62 or Base-24).

### **Example:**
| ID  | Short URL (Base-62) |
|-----|----------------------|
| 1   | `a` |
| 2   | `b` |
| 1000 | `g8` |

### **Pros:**
✔️ **Fast & predictable**.  
✔️ **No hashing needed** (direct ID encoding).  

### **Cons:**
❌ **Sequential IDs expose system data** (users can guess the next URL).  
❌ Needs **distributed counter management** for high-scale systems.

✅ **Best for:** **Fast lookups** in structured databases.

---

## **4️⃣ Randomized Short Codes (UUID, NanoID)**
### **How It Works:**
- Generates a **random alphanumeric string** as the short URL.
- **NanoID** is an optimized alternative to UUID (shorter and more efficient).

### **Example (NanoID, length=6, Base-62)**  

"abc123" "zYxwVu"

### **Pros:**
✔️ No **global counter** or **hashing** required.  
✔️ Works **without a database**.  
✔️ **Unpredictable & secure**.

### **Cons:**
❌ **Collisions are possible** (though rare).  
❌ Cannot **decode back** to an ID.  

✅ **Best for:** **Stateless** systems that need **randomized short URLs**.

---

## **5️⃣ Pseudo-Random Mapping (HMAC-Based or XOR)**
### **How It Works:**
- Uses a **secret key** and an **HMAC function** (e.g., `HMAC-SHA256`) to generate a **deterministic but random-looking** short code.

### **Pros:**
✔️ More **secure** than direct hashing.  
✔️ **Tamper-resistant**.  
✔️ Can be **reversible** if needed.

### **Cons:**
❌ Requires **key management** (if using HMAC).  
❌ Short URL length still depends on entropy.

✅ **Best for:** **Secure URL shortening** where predictability is a concern.

---

## **🔍 Comparison Table**

| Algorithm | Short URL Length | Requires DB? | Collision Risk? | Easily Decodable? | Best For |
|-----------|----------------|-------------|----------------|------------------|-----------|
| **Hashing (SHA-256, MD5, etc.)** | Medium | ❌ No | ✅ Yes (without salt) | ❌ No | Stateless, decentralized systems |
| **Base Encoding (Base-62, Base-24, Base-58)** | Short | ✅ Yes | ❌ No | ✅ Yes | High-performance retrieval |
| **Counter-Based (Auto-Increment + Base Encoding)** | Short | ✅ Yes | ❌ No | ✅ Yes | Predictable, fast lookup |
| **Random Short Codes (NanoID, UUID)** | Short | ❌ No | ✅ Low | ❌ No | Secure and stateless |
| **HMAC-Based or XOR Mapping** | Short | ❌ No | ✅ No | ✅ Yes | Secure URL shortening |

---

## **🛠️ Which One Should You Use?**
- If **security & randomness** matter → **NanoID** or **HMAC-based mapping**.  
- If **speed & easy retrieval** matter → **Base-62 with a database-backed counter**.  
- If **stateless operation** is required → **Hashing (with collision handling)**.  
- If **scalability** is a priority → **Distributed counter + Base encoding**.  

