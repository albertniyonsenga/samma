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

[![Movie Finder Demo](https://img.youtube.com/vi/ID/0.jpg)](https://www.youtube.com/watch?v=ID)

*Click image to watch demo video on Loom*

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
# If you wanna hack into api
cd samma-api

# If you wanna hack into a website
cd web
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
