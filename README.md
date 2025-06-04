# Path of Exile Weapon Search

This small Django project provides a simple search page that queries the community PoE wiki via its Cargo API. Results are filtered by weapon class, attack speed and DPS.

## Development setup

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install django requests
```

2. Run the development server:

```bash
python manage.py runserver
```

3. Open `http://localhost:8000/` in your browser.

A network connection is required for the search results to load because the server fetches data from `poewiki.net`.
