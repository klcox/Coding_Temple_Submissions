import requests

class APIClient:
    """A simple API client — similar to how you'd organize a Postman collection."""
    
    def __init__(self, base_url, headers=None):
        self.base_url = base_url.rstrip("/")
        self.default_headers = headers or {}
    
    def _request(self, method, path, **kwargs):
        """Make a request and return a formatted result."""
        url = f"{self.base_url}{path}"
        
        # Merge default headers with any request-specific headers
        headers = {**self.default_headers, **kwargs.pop("headers", {})}
        
        response = requests.request(method, url, headers=headers, **kwargs)
        
        return {
            "status": response.status_code,
            "reason": response.reason,
            "time_ms": response.elapsed.total_seconds() * 1000,
            "data": response.json() if response.text else None,
            "headers": dict(response.headers),
        }
    
    def get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)
    
    def post(self, path, **kwargs):
        return self._request("POST", path, **kwargs)
    
    def put(self, path, **kwargs):
        return self._request("PUT", path, **kwargs)
    
    def patch(self, path, **kwargs):
        return self._request("PATCH", path, **kwargs)
    
    def delete(self, path, **kwargs):
        return self._request("DELETE", path, **kwargs)


class JSONPlaceholderClient(APIClient):
    """Extension of APIClient for https://jsonplaceholder.typicode.com."""

    def __init__(self):
        super().__init__("https://jsonplaceholder.typicode.com")
    
    def get_user(self, user_id):
        """Get a specific user's profile."""

        return self.get(f"/users/{user_id}")
    
    def get_user_posts(self, user_id):
        """Get all posts by a specific user."""

        return self.get(f"/users/{user_id}/posts")
    
    def create_post(self, user_id, title, body):
        """Create a new post for a user."""

        post_data = {
            "title": title,
            "body": body,
            "userId": user_id
        }

        return self.post("/posts", json=post_data)
    
    def search_posts(self, query):
        """Search posts by title (client-side filtering)."""

        posts_results = self.get("/posts")

        query = query.lower()
        return [post for post in posts_results['data'] if query in post['title'].lower()]


if __name__ == "__main__":
    
    client = JSONPlaceholderClient()

    print(f"{'-' * 5} 1. Get user 5's profile and print their name and city {'-' * 5}")
    results = client.get_user(5)
    print(f"  User 5's Name: {results['data']['name']}, City: {results['data']['address']['city']}")  # Should print Chelsey Dietrich, Roscoeview

    print(f"\n{'-' * 5} 2. Get user 5's posts and print the count {'-' * 5}")
    results = client.get_user_posts(5)
    print(f"  User 5 has {len(results['data'])} posts.")  # Should print 10

    print(f"\n{'-' * 5} 3. Create a new post and print the returned ID {'-' * 5}")
    results = client.create_post(1, "Test Title", "Test Body")
    print(f"  The Post ID for the created post is: {results['data']['id']}.")  # Should print 101

    print(f"\n{'-' * 5} 4. Search for posts with 'qui' in the title and print how many match {'-' * 5}")
    results = client.search_posts("qui")
    print(f"  {len(results)} posts contain 'qui' in the title.")  # Should print 33 