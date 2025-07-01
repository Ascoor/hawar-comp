# hawar-comp

## Configuration

The React frontend reads its API endpoint from `frontend/src/config.js`. The file exports an object with a `baseURL` property pointing to the backend server:

```javascript
const API_CONFIG = {
  baseURL: 'http://localhost:8000',
};

export default API_CONFIG;
```

Modify `baseURL` to match the host and port of your API. For example, when running in production you might set it to `https://api.example.com`. You can create different copies of this file for development, staging, and production environments as needed.

