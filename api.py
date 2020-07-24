import requests 


API_AUTH_KEY ="3f07b0ab597dec3ed6f9793b4087111a"


def get_upcoming_movies(region=None,page=1):
    try:
        if region is None:
            api_url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_AUTH_KEY}&page={page}"
        else:
            api_url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_AUTH_KEY}&page={page}&region={region}"

        print(api_url)
        r = requests.get(api_url)
        
        if r.status_code == 200:
            responseJson = r.json()
            results = list(responseJson['results'])
            return results
        else:
            return None
    except :
        return None


