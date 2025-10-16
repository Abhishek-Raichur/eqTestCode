## :warning: Please read these instructions carefully and entirely first
* Clone this repository to your local machine.
* Use your IDE of choice to complete the assignment.
* When you have completed the assignment, you need to  push your code to this repository and [mark the assignment as completed by clicking here](https://app.snapcode.review/submission_links/56097bbd-a081-4209-b863-7a63a0bf23aa).
* Once you mark it as completed, your access to this repository will be revoked. Please make sure that you have completed the assignment and pushed all code from your local machine to this repository before you click the link.

## Operability Take-Home Exercise

Welcome to the start of our recruitment process for Operability Engineers. It was great to speak to you regarding an opportunity to join the Equal Experts network!

Please write code to deliver a solution to the problems outlined below.

We appreciate that your time is valuable and do not expect this exercise to **take more than 90 minutes**. If you think this exercise will take longer than that, I **strongly** encourage you to please get in touch to ask any clarifying questions.

### Submission guidelines
**Do**
- Provide a README file in text or markdown format that documents a concise way to set up and run the provided solution.
- Take the time to read any applicable API or service docs, it may save you significant effort.
- Make your solution simple and clear. We aren't looking for overly complex ways to solve the problem since in our experience, simple and clear solutions to problems are generally the most maintainable and extensible solutions.

**Don't**

Expect the reviewer to dedicate a machine to review the test by:

- Installing software globally that may conflict with system software
- Requiring changes to system-wide configurations
- Providing overly complex solutions that need to spin up a ton of unneeded supporting dependencies. We aspire to keep our dev experiences as simple as possible (but no simpler)!
- Include identifying information in your submission. We are endeavouring to make our review process anonymous to reduce bias.

### Exercise
If you have any questions on the below exercise, please do get in touch and we’ll answer as soon as possible.

#### Build an API, test it, and package it into a container

---

## Usage Instructions

### 1. Run Locally (Recommended for Development)

```zsh
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (all versions are pinned for reproducibility)
pip install -r requirements.txt

# Run the Flask app
FLASK_APP=app.py flask run --port 8080
```

### 2. Run Tests

First, ensure you have activated your virtual environment:
```zsh
source .venv/bin/activate
```

Then run the tests:
```zsh
python -m pytest -q
```

- All tests are located in the `tests/` directory.
- Tests use mocking for external API calls (e.g., GitHub) to ensure reliability and speed.
- Tests cover all edge cases, including error handling, empty responses, and invalid input.
- To add more tests, create or edit files in the `tests/` directory using the `pytest` framework and Python's `unittest.mock` or `pytest-mock` for mocking.

### Tests (mocked and edge cases)

- Location: `tests/test_api.py`
- Purpose: all tests are mocked to avoid real network calls and to run quickly and deterministically.

What the tests do:
- Patch the app's HTTP client with `patch("app.requests.get", ...)` so the app's call to GitHub is intercepted by mocks.
- Use an `autouse` pytest fixture that clears the app's in-memory cache (`app._gist_cache`) before each test to avoid reusing cached, real responses.
- Cover edge cases:
	- Successful response (200) returning a list of gists
	- User not found (404) -> returns `{"error": "not_found"}` with status 404
	- Upstream/network error (raises `requests.RequestException`) -> returns `{"error": "upstream_error"}` with status 502
	- Upstream returns invalid JSON -> returns `{"error": "invalid_response"}` with status 502

How to run the tests (from project root):

```zsh
# Activate your virtualenv if needed
source .venv/bin/activate

# Run all tests
python -m pytest -q

# Run a specific test file
python -m pytest tests/test_api.py -q
```

Notes:
- The tests use `unittest.mock` (via `patch` and `MagicMock`) to simulate `requests` behaviour. This ensures fast, reliable tests and that external APIs are never called during test runs.
- The README and tests aim for reproducibility: dependencies are pinned in `requirements.txt` and the test instructions above use the project's Python interpreter.

### 3. Build and Run with Docker (Recommended for Production)

```zsh
# Build the Docker image (uses multi-stage build, non-root user, and security best practices)
docker build -t python-app .

# Run the container (listens on port 8080)
docker run -p 8080:8080 python-app
```

- The Dockerfile uses a multi-stage build for a minimal, secure image.
- All dependencies are pinned in `requirements.txt` for reproducibility.
- The container runs as a non-root user for security.
- For even smaller images, consider using `python:3.11-alpine` as the base if your dependencies support it.

### 4. API Usage

- List public gists for a user (e.g. octocat):
  - `GET http://localhost:8080/octocat`
  - Returns: JSON array of gists

#### Optional Features
- Pagination: Use `?page=<n>&per_page=<m>` query params
- Caching: Results cached in-memory for 60 seconds

#### Example

```zsh
curl http://localhost:8080/octocat
```

Returns:

```json
[{
	"id": "6cad326836d38bd3a7ae",
	"description": "Hello world!",
	...
}]
```

---
Best of luck,  
Equal Experts
__________________________________________
[^1]: For example Go, Python or Ruby but not Bash or Powershell.  
[^2]: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28
