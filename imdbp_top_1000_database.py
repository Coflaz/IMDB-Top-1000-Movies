from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pygame

driver_path = "/Users/student/Desktop/Project Ideas/IMDB Top 1000/chromedriver"

service = Service(driver_path)
driver = webdriver.Chrome(service=service)

pygame.init()
music_file = "/Users/student/Desktop/Project Ideas/IMDB Top 1000/Waiting Jazz.mp3"
pygame.mixer.music.load(music_file)
pygame.mixer.music.play(loops=-1)

driver.get("https://www.google.com")
time.sleep(2)

google_search_bar = driver.find_element(By.CLASS_NAME, "gLFyf")
google_search_bar.send_keys('IMDb "Top 1000" (Sorted by IMDb Rating Descending)')
google_search_bar.send_keys(Keys.ENTER)

try:
    top_1000_imdb_link = driver.find_element(By.CLASS_NAME, "LC20lb")
    time.sleep(2)
    top_1000_imdb_link.click()
except:
    print("Element not found or cannot be clicked.")

movie_names = []
movie_years = []
movie_durations = []
movie_genres = []
movie_ratings_stars = []
movie_ratings_metascore = []
movie_descriptions = []
movie_directors = []
movie_stars = []
movie_gross = []

def movie_info_parser():
    movie_contents_header = driver.find_elements(By.CLASS_NAME, "lister-item-header")

    for movie_content in movie_contents_header:
        movie_name = movie_content.find_element(By.TAG_NAME, "a")
        movie_names.append(movie_name.text)

        movie_year = movie_content.find_element(By.CLASS_NAME, "lister-item-year").text
        movie_years.append(int(movie_year[-5:-1]))

    movie_contents = driver.find_elements(By.CLASS_NAME, "lister-item-content")

    for movie_content in movie_contents:
        movie_duration = movie_content.find_element(By.CLASS_NAME, "runtime").text
        movie_durations.append(int(movie_duration.split(" ")[0]))

        movie_genre = movie_content.find_element(By.CLASS_NAME, "genre").text
        movie_genres.append(movie_genre)

        movie_rating_star = movie_content.find_element(By.CLASS_NAME, "ratings-imdb-rating").text
        movie_ratings_stars.append(float(movie_rating_star))

        try:
            movie_rating_metascore = movie_content.find_element(By.CLASS_NAME, "metascore").text
            movie_ratings_metascore.append(int(movie_rating_metascore))
        except:
            movie_ratings_metascore.append("N/A")

        movie_description = movie_content.find_element(By.XPATH, ".//p[@class='text-muted']").text
        movie_descriptions.append(movie_description)

        try:
            gross_span = movie_content.find_elements(By.CSS_SELECTOR, "p.sort-num_votes-visible span[name='nv'][data-value]")
            
            if len(gross_span) >= 2:  # Ensure there's at least a second span element
                second_gross_span = gross_span[1]
                data_value = second_gross_span.get_attribute("data-value")
                
                if data_value:
                    gross_value = data_value.strip('$')
                    if int(gross_value.replace(",", "")) > 100000:
                        movie_gross.append(gross_value)
                    else:
                        movie_gross.append("N/A")
                else:
                    movie_gross.append("N/A")
            else:
                movie_gross.append("N/A")
        except:
            movie_gross.append("N/A")


    # Extracting directors and stars information

next_clicker = 0

def next_page_opener():
    global next_clicker
    if next_clicker <= 8:
        next_clicker += 1
        print("Scraped page {}.".format(next_clicker))
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".lister-page-next.next-page")))
        next_button.click()
    else:
        print("Scraped page {}.".format(next_clicker))
        pass


while True:
    try:
        movie_info_parser()
        time.sleep(3)
        next_page_opener()
        time.sleep(3)

        if next_clicker == 9:
            print("All pages scraped.")
            break
    except Exception as e:
        print(e)
        driver.quit()
        break


movie_list = []
for i in range(len(movie_names)):
    movie_list.append({
        "name": movie_names[i],
        "year": movie_years[i],
        "duration": movie_durations[i],
        "genre": movie_genres[i],
        "rating_star": movie_ratings_stars[i],
        "rating_metascore": movie_ratings_metascore[i],
        "description": movie_descriptions[i],
        "gross": movie_gross[i]
    })
driver.quit()

def list_movies_by_year(year_start, year_end):
    year_by_year_movie_list = []
    for movie in movie_list:
        if movie["year"] >= year_start and movie["year"] <= year_end:
            year_by_year_movie_list.append(movie)
    return year_by_year_movie_list

def list_all_movies():
    for movie in movie_list:
            print("\n")
            print("Movie: {}\nYear: {}\nDuration: {} mins\nGenre: {}\nIMDb Rating: {}\nMetascore: {}\nDescription: {}\nGross: ${}".format(
                movie["name"], movie["year"], movie["duration"], movie["genre"], movie["rating_star"], movie["rating_metascore"], movie["description"], movie["gross"]))
            print("\n")

def list_movies_by_genre(genre):
    genre_movie_list = []
    for movie in movie_list:
        if genre.lower() in movie["genre"].lower():
            genre_movie_list.append(movie)
    return genre_movie_list

def list_movies_by_gross(gross_start, gross_end):
    if gross_end == "unknown":
        gross_end = 100000000000000
    gross_movie_list = []
    for movie in movie_list:
        if movie["gross"] != "N/A":
            if int(movie["gross"].replace(",", "")) >= gross_start and int(movie["gross"].replace(",", "")) <= gross_end:
                gross_movie_list.append(movie)
    return gross_movie_list

def list_movies_by_metascore(metascore_start, metascore_end):
    if metascore_end == "unknown" or metascore_end == "100":
        metascore_end = 100
    metascore_movie_list = []
    for movie in movie_list:
        if movie["rating_metascore"] != "N/A":
            if movie["rating_metascore"] >= metascore_start and movie["rating_metascore"] <= metascore_end:
                metascore_movie_list.append(movie)
    return metascore_movie_list

def print_the_user_list_again():
    print("\n")
    print("Write a movie name to list all the information about it!")
    time.sleep(1)
    print("Type #1 to list all movies")
    time.sleep(1)
    print("Type #2 to list movies by year")
    time.sleep(1)
    print("Type #3 to list movies by genre")
    time.sleep(1)
    print("Type #4 to list movies by gross")
    time.sleep(1)
    print("Type #5 to list movies by metascore")
    time.sleep(1)
    print("Type 'list' to list all the commands again")
    time.sleep(1)
    print("Type #6 to exit (or just type 'exit')")
    print("\n")

# Improved user input handling
print_the_user_list_again()

while True:
    user_input = input("\nPlease enter a movie name or '#number': \n")
    if user_input.lower() == "exit" or user_input == "#6":
        print("\nExiting...\n")
        time.sleep(1)
        pygame.mixer.music.stop()
        pygame.quit()   
        break
    elif user_input == "#1":
        list_all_movies()
    elif user_input == "#2":
        year_start = int(input("Enter the start year: "))
        year_end = int(input("Enter the end year: "))
        year_by_year_movie_list = list_movies_by_year(year_start, year_end)
        for movie in year_by_year_movie_list:
            print("\n")
            print("Movie: {}\nYear: {}\nDuration: {} mins\nGenre: {}\nIMDb Rating: {}\nMetascore: {}\nDescription: {}\nGross: ${}".format(movie["name"], movie["year"], movie["duration"], movie["genre"], movie["rating_star"], movie["rating_metascore"], movie["description"], movie["gross"]))
            print("\n")
    elif user_input == "#3":
        genre = input("Enter the genre: ")
        genre_movie_list = list_movies_by_genre(genre)
        for movie in genre_movie_list:
            print("\n")
            print("Movie: {}\nYear: {}\nDuration: {} mins\nGenre: {}\nIMDb Rating: {}\nMetascore: {}\nDescription: {}\nGross: ${}".format(movie["name"], movie["year"], movie["duration"], movie["genre"], movie["rating_star"], movie["rating_metascore"], movie["description"], movie["gross"]))
            print("\n")
    elif user_input == "#4":
        gross_start = int(input("Enter the start gross: "))
        gross_end = input("Enter the end gross (or 'unknown'): ")
        gross_movie_list = list_movies_by_gross(gross_start, gross_end)
        for movie in gross_movie_list:
            print("\n")
            print("Movie: {}\nYear: {}\nDuration: {} mins\nGenre: {}\nIMDb Rating: {}\nMetascore: {}\nDescription: {}\nGross: ${}".format(movie["name"], movie["year"], movie["duration"], movie["genre"], movie["rating_star"], movie["rating_metascore"], movie["description"], movie["gross"]))
            print("\n")
    elif user_input == "#5":
        metascore_start = int(input("Enter the start metascore: "))
        metascore_end = input("Enter the end metascore (or 'unknown'): ")
        metascore_movie_list = list_movies_by_metascore(metascore_start, metascore_end)
        for movie in metascore_movie_list:
            print("\n")
            print("Movie: {}\nYear: {}\nDuration: {} mins\nGenre: {}\nIMDb Rating: {}\nMetascore: {}\nDescription: {}\nGross: ${}".format(movie["name"], movie["year"], movie["duration"], movie["genre"], movie["rating_star"], movie["rating_metascore"], movie["description"], movie["gross"]))
            print("\n")
    elif user_input.lower() == "list":
        print_the_user_list_again()
    else:
        found_movie = False
        for movie in movie_list:
            if user_input.lower() in movie["name"].lower():
                found_movie = True
                print("\n")
                print("Movie: {}\nYear: {}\nDuration: {} mins\nGenre: {}\nIMDb Rating: {}\nMetascore: {}\nDescription: {}\nGross: ${}".format(
                    movie["name"], movie["year"], movie["duration"], movie["genre"], movie["rating_star"], movie["rating_metascore"], movie["description"], movie["gross"]))
                print("\n")
                break

        if not found_movie:
            print("\n")
            print("Movie not found.")
            print("\n")