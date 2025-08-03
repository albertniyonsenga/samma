# Samma: Movie Finder
## Motivation
I have been one of the best movie lovers growing up, and eventually found no time for that, which made me shift to reading their plot on Wikipedia or watching their summary on YouTube. That's made me think of a simple way to access that information easily, so first, I thought of making a Python Package that can give me all the information in my terminal.

```python
# Simply by commands and save its plot
Ifilimu "Inception"-save
```
I tried my best to craft it; however, the time and capacity to make it complete and fully functional didn't allow me to do so, so I had to shift to web-based, which is the main idea we will discuss below. However, don't hesitate to check out [ifilimu's development](https://pypi.org/project/ifilimu) ifilimu's development so far.

## Project Overview
Samma: Movie Finder is a sophisticated web application that demonstrates the practical implementation of web infrastructure concepts. This project combines frontend development with robust backend integration, featuring a failover system automatically switching between API endpoints when failures occur.

### Demo Video
See Movie Finder in action with a demonstration of the backend failover system:

https://github.com/user-attachments/assets/e748d59b-c9f1-4c76-8bf4-07f40318beeb

<details>
<summary>Implementation</summary>

## System Architecture
```
Client Browser
│
├─> Primary Backend (https://samma-api.onrender.com)
│   │
│   └─> Failover 1 (https://samma-api-prod.onrender.com)
│       │
│       └─> Failover 2 (https://samma-api-failover.onrender.com)
│
├─> Local Storage (Recent Searches)
│
└─> UI Components
    ├─ Search Interface
    ├─ Results Display
    └─ Status Indicators
```
## Technical Implementation
### Backend Failover System

```javascript
const BACKENDS = [
  "https://samma-api.onrender.com",
  "https://samma-api-prod.onrender.com",
  "https://samma-api-failover.onrender.com"
];

async function callBackend(path, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(`${BACKENDS[currentBackendIndex]}${path}`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return await response.json();
    } catch (error) {
      if (i === retries - 1 && currentBackendIndex < BACKENDS.length - 1) {
        currentBackendIndex++;
        i = -1;  // Reset retry counter
      }
    }
  }
  throw new Error("All backends failed");
}
```

This implementation demonstrates:
1. **API endpoint rotation** when failures occur
2. **Retry logic** with configurable attempts
3. **Visual status indicators** showing active backend
4. **Graceful degradation** when all backends fail

### Frontend Architecture
- **Responsive Design**: Mobile-first approach with CSS Grid/Flexbox
- **Performance Optimization**: Minimal dependencies, efficient rendering
- **State Management**: LocalStorage for persistent recent searches
- **Error Handling**: User-friendly error messages with retry options

```css
/* Visual backend status indicators */
.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #555;
}

.status-dot.active {
  background: #6cffa0;
  box-shadow: 0 0 8px rgba(108, 255, 160, 0.8);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}
```

### API Integration Features
1. **Rate Limit Awareness**: Sequential backend switching avoids hitting rate limits
2. **Header Management**: Proper Content-Type and Accept headers
3. **Response Validation**: Checks for valid JSON before processing
4. **Error Mapping**: Converts HTTP errors to user-friendly messages

## Technical Limits and Solutions
1. **API Dependency**:
   - *Challenge*: Requires compatible backend APIs
   - *Solution*: Abstracted API client with adapter pattern

2. **Rate Limiting**:
   - *Challenge*: Backend API rate restrictions
   - *Solution*: Multiple endpoints with failover

3. **Browser Compatibility**:
   - *Challenge*: Support for older browsers
   - *Solution*: Progressive enhancement approach

4. **Security Constraints**:
   - *Challenge*: Frontend-only implementation
   - *Solution*: Ready for HTTPS/TLS integration provided by our hosting platform - GitHub Pages
</details>

## Project Setup

```bash
# Clone repository
git clone https://github.com/albertniyonsenga/samma.git
cd samma
```
```
# If you wanna hack into api
cd samma-api
```
```
# If you wanna hack into a website
cd web
```
<details> 
<summary> API Setup & Usage </summary>
    
### 1. Prerequisites
- **Python 3.10+**
- **OMDb API Key** – obtain from [omdbapi.com](https://www.omdbapi.com).  
  Your free tier allows up to ~1,000 daily requests, and the API returns fields like `Title`, `Year`, `Plot`, `Poster` (or `"N/A"`), `Actors`, `Genre`, `imdbRating`, etc., all compatible with your FastAPI `/movie?title=` endpoint :contentReference[oaicite:0]{index=0}.


### 2. Clone & Environment Setup

```bash
git clone https://github.com/albertniyonsenga/samma.git
cd samma-api
````

Create a `.env` (or export directly):

```
OMDB_API_KEY=your-omdb-api-key
```

Or for shell:

```bash
export OMDB_API_KEY=your-omdb-api-key
```

---

### 3. Install & Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn httpx
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/` — the API root will show a JSON like:

```json
{
  "message": "🎬 Welcome to Movie Search API powered by Samma Backend",
  "endpoints": {
    "movie": "/movie?title=<TITLE>",
    "search": "/search?query=<TERM>&page=<PAGE_NUMBER>"
  },
  "docs": "/docs"
}
```

⚠️ Do **not** use `uvicorn app:app`; since your file is named `main.py`, the correct module path is `main:app`. Otherwise, you'll see:

````
ModuleNotFoundError: No module named 'app'
``` :contentReference[oaicite:5]{index=5}
````
---

### 4. CORS Middleware

Your `main.py` includes:

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(...)
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)
````

This setup permits requests from **any origin**—essential for separate frontend domains—and handles both simple GETs and preflight `OPTIONS`, automatically setting the needed CORS headers ([FastAPI][1]).

---

### 5. Running with Docker

```bash
docker build -t movie-api:latest .
docker run --env OMDB_API_KEY=your_key_here -p 80:80 movie-api:latest
```

The FastAPI app will serve at `http://localhost:80/movie?title=Inception`.

---

### 6. Deploying to Render.com

Ensure your `render.yaml` includes:

```yaml
services:
  - type: web
    name: movie-api
    runtime: docker
    dockerfilePath: ./Dockerfile
    plan: free
    envVars:
      - key: OMDB_API_KEY
        sync: false
```

Render will prompt you for `OMDB_API_KEY` securely. It will run `uvicorn main:app --host=0.0.0.0 --port 80` by default (as specified in the Dockerfile).

---

### 7. API Endpoints (Sample Requests)

| Endpoint      | Description                     | Example URL                    |
| ------------- | ------------------------------- | ------------------------------ |
| `GET /`       | Welcome message & documentation | `https://your-api-domain.com/` |
| `GET /movie`  | Fetch movie details by title    | `?title=Inception`             |
| `GET /search` | Search movies with pagination   | `?q=Matrix&page=1`         |

**Example using `curl`:**

```bash
curl "https://your-api-domain.com/movie?title=Inception"
```

**Note:** The response JSON is a direct pass-through of OMDb fields such as:
`Title`, `Year`, `Plot`, `Actors`, `Director`, `Genre`, `Runtime`, `Poster`, `imdbRating`, etc.

---

### 8. Frontend Integration (JavaScript Example)

```javascript
fetch(`/movie?title=${encodeURIComponent(title)}`)
  .then(res => {
    if (!res.ok) throw new Error(res.status);
    return res.json();
  })
  .then(data => {
    console.log(data.Title, data.Plot, data.Poster, data.imdbRating);
  })
  .catch(err => console.error("Error:", err));
```

Your UI can map these fields to render title, year, plot, actors, poster, and IMDb rating.

---

### ✅ Quick Checklist

* \[x] `.env` or environment variable setup
* \[x] Run with `uvicorn main:app`, **not** `app:app`
* \[x] CORS configured to allow all origins via FastAPI middleware
* \[x] Dockerfile presents at `/movie?title=<TITLE>` endpoint
* \[x] Included fast, reliable API response fields from OMDb
* \[x] Ready for frontend consumption—poster renders, recent searches, and failover handled

---

### Troubleshooting Tips

| Issue                                                  | Cause                                       | Resolution                                                                                                                              |
| ------------------------------------------------------ | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'app'`           | Uvicorn using `app:app`, file is `main.py`  | Update to `uvicorn main:app` ([Stack Overflow][2], [KodeKloud Notes][3], [Stat 545][4], [sentry.io][5])                                 |
| `CORS policy: No 'Access-Control-Allow-Origin' header` | Browser blocked cross-domain request        | Verify CORS middleware with `allow_origins=["*"]`, and that `allow_methods`/`allow_headers` are set ([FastAPI][1], [Stack Overflow][6]) |
| `"Poster": "N/A"` or image fails to load               | OMDb API returns no poster or blocked image | Ensure your frontend hides or replaces poster element gracefully, use `Poster !== "N/A"` condition                                      |

---

With this setup, you’re ready to **develop**, **test**, or **deploy** your backend—and integrate it seamlessly with your frontend. Enjoy building! 🎬

```
::contentReference[oaicite:29]{index=29}
```

[1]: https://fastapi.tiangolo.com/tutorial/cors/
[2]: https://stackoverflow.com/questions/71311507/modulenotfounderror-no-module-named-app-fastapi-docker/71312543
[3]: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Deployment/What-Is-CORS 
[4]: https://stat545.com/diy-web-data.html
[5]: https://sentry.io/answers/fastapi-docker-no-module-named-app-error/
[6]: https://stackoverflow.com/questions/65635346/how-can-i-enable-cors-in-fastapi

</details>
<details>
    <summary> Front-end Setup and usage</summary>
    
This section guides you to **run the front-end UI** after switching to the `web` branch of your repository. This is the branch containing the static site files (`index.html`, `style.css`, etc.), and is *separate from your back-end repo or branch*.

---

### Switch to the `web` branch

From your terminal inside the project folder:

```bash
git fetch origin
git switch web
```
**Boom then you're ready to hack the front-end.**
</details>

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
