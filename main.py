import requests
import pandas as pd
import time

def get_info(title, release_year):
    
    url = "http://www.omdbapi.com/?apikey=bcbd2e80&"
    params = {"t" : title, "y": release_year}
    
    try:
        response = requests.get(url=url, params=params)
        data = response.json()
        
        if "Error" in data:
            print(data["error"])
            return None
        elif data.get("Response") == "True":
            movie = data
            
            imbd_rating = ''
            actors_names = ''
            votes = ''
            
            if "imdbRating" in movie:
                imbd_rating = movie["imdbRating"]
            
            if "Actors" in movie:
                actors_names = movie["Actors"]
            
            if "imdbVotes" in movie:
                votes = movie["imdbVotes"]
                
            return {
                "imbd_rating": imbd_rating,
                "actors_names": actors_names,
                "votes": votes,
            }
            
        else:
            print("Movie not found")    
            return None
    except requests.exceptions.ConnectionError:
        print("Error: The server is unavailable or the URL is invalid.")
    except requests.exceptions.Timeout:
        print("Error: The request has timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error:: {e}")
    
    

df = pd.read_csv("movies.csv")
df["imbd_rating"] = ""
df["actors_names"] = ""
df["votes"] = ""

df["title"] = df["title"].str.replace(":", "")


for index, row in df.iterrows():
    mis_data = get_info(row["title"], row["release_year"])
    
    if mis_data:
        if mis_data["imbd_rating"]:
            df.at[index, "imbd_rating"] = mis_data["imbd_rating"]
        if mis_data["actors_names"]:
            df.at[index, "actors_names"] = mis_data["actors_names"]
        if mis_data["votes"]:
            df.at[index, "votes"] = mis_data["votes"]
    
    time.sleep(3)
    

df.to_xml("movies.xml", parser="etree", root_name="Movies", row_name="Movie", index=None, elem_cols=["title", "release_year", "genre", "director", "country", "duration", "imbd_rating", "actors_names", "votes"])

df.to_csv("movies.csv", index=False)
df_sorted = df.sort_values(by="imbd_rating", ascending=False)

print(df_sorted.iloc[:11])


