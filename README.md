# YT-Search-with-Django

## About the App
- Built using a Django backend and a PostgreSQL database
- Uses Celery for asynchronously procesing the predefined search query `Space` every `30` seconds (time interval can be changed in the `settings/dev.py` file)
- Uses Redis as the messaging queue to send the task message to the Celery workers
- Fully Dockerized
- App will automatically search for an available valid (not having esxeeded it's quota) API key, and if not available gives a proper error log
- Can add new API keys through a dashboard & filter
- Search dashboard with sorting (Partial matching available)
- Search API (Partial matching available)

## Launching the app
- Pull the github repo, and change the `SEARCH TERM` in `docker/docker.env` file if you want (Default is "Space")
- From the root folder having the `docker-compose` file, launch it for the first time using `docker-compose --build` 
- Go to `<ip>:<port>/admin` (`http://localhost:8000/admin` if in local machine) and login using `admin` & `password` as credentials
- Add a valid Developer API key through the dashboard
- For the first time, the app will load all matching results for the past 6 hours
- From next asynchronous run of the celery workers, all videos uploaded after the latest stored video will be loaded
- You can check the schema of the db if you go to the url: `<ip>:<port>/dbschema`

## Search API
- Paginated response (Max 100 per page. Can change this setting easily) along with token for next page
- The search query/term will be matched against both title & description to find results
  - If any of the words in the query are present in any order in either title, or description, the result will added to the response (case-insensitive)
- To use the API: (Example)
```
import requests
import json

url = "http://localhost:8000/api/search/keyword_search/"
data = {"search_term": "Good"}
r = requests.get(data=data, url=url)
json.loads(r.content)
```
- Response content is of form:
```
{'count': 1,
 'next': None,
 'previous': None,
 'results': [{'title': 'Space Shooter Game| Galaxy Attack',
   'description': 'Save world from alien attack new feature game with new look and more stages interesting and increase performance.',
   'publish_time': '2020-10-13T17:57:14Z',
   'thumbnail_url': 'https://i.ytimg.com/vi/BICSrItx3HA/default.jpg',
   'video_id': 'BICSrItx3HA'
   }
  ]
}
```

## Dashboard to view the stored videos and add new API keys
- A superuser will automatically by created, and the user can go to `<ip>:<port>/admin` to login with an `admin` username and `password` password
- API Key section:
  - The admin can then add a new API key in the `API keys` section
- Search Results section:
  - All the search results stored will be available here, and can search for them or sort by various attributes including Title, Description, Publish time & Date, Thumbnail URL & VideoID
  - Can also delete any of the results
