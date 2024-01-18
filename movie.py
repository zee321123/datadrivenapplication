import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

class MovieflixApplication:
    def __init__(custom_movie_app, root_window):
     
        # Set up the main window and configurations
        custom_movie_app.window = root_window
        custom_movie_app.window.title("MyMovieApp")
        custom_movie_app.window.geometry("800x780")
        custom_movie_app.window.resizable(False, False)

        # Set up API key and endpoints for movie data
        custom_movie_app.api_key = "7b7ed2aa5697e629fa150e5afe30f132"
        custom_movie_app.search_endpoint = "https://api.themoviedb.org/3/search/movie"
        custom_movie_app.tv_endpoint = "https://api.themoviedb.org/3/discover/tv"
        custom_movie_app.similar_endpoint = "https://api.themoviedb.org/3/movie/{}/similar"
        custom_movie_app.page_number = 1
        custom_movie_app.last_query = ""
        custom_movie_app.genres = custom_movie_app.fetch_movie_genres()

     
        custom_movie_app.window.configure(bg="#2C3E50")

        # Create navigation toggle button
        custom_movie_app.nav_toggle_button = tk.Menubutton(custom_movie_app.window, text="\u2630", font=("Helvetica", 24), bg="#2C3E50", fg="white", bd=0)
        custom_movie_app.nav_toggle_button.menu = tk.Menu(custom_movie_app.nav_toggle_button, tearoff=0, font=("Helvetica", 14), bg="#2C3E50", fg="white")
        custom_movie_app.nav_toggle_button["menu"] = custom_movie_app.nav_toggle_button.menu
        custom_movie_app.nav_toggle_button.menu.add_command(label="Home", command=custom_movie_app.show_main_page)
        custom_movie_app.nav_toggle_button.menu.add_command(label="Movies", command=custom_movie_app.show_film_page)
        custom_movie_app.nav_toggle_button.menu.add_command(label="Information", command=custom_movie_app.show_info_page)
        custom_movie_app.nav_toggle_button.place(x=10, y=10)

        # Show the main page
        custom_movie_app.show_main_page()

    def show_main_page(custom_movie_app):
        # Display the main page with a background image
        custom_movie_app.clear_widgets()

        main_image = Image.open("main.png")
        main_image = main_image.resize((800, 700))
        main_photo = ImageTk.PhotoImage(main_image)

        main_label = tk.Label(custom_movie_app.window, image=main_photo, bg="#2C3E50")
        main_label.image = main_photo
        main_label.pack(pady=60)

    def show_film_page(custom_movie_app):
        # Display the film page with search options and movie details
        custom_movie_app.clear_widgets()

        # Entry for search query
        custom_movie_app.search_variable = tk.StringVar()
        search_entry = tk.Entry(custom_movie_app.window, font=("Helvetica", 16), bg="white", fg="#2C3E50", bd=5, relief=tk.FLAT, textvariable=custom_movie_app.search_variable)
        search_entry.insert(0, "Search movies...")
        search_entry.bind("<FocusIn>", custom_movie_app.clear_search_text)
        search_entry.pack(pady=10)

        # Dropdown for movie genres
        genre_variable = tk.StringVar()
        genre_dropdown = tk.OptionMenu(custom_movie_app.window, genre_variable, *custom_movie_app.genres)
        genre_dropdown.config(bg="#3498DB", fg="white", font=("Helvetica", 12))
        genre_dropdown["menu"].config(bg="#3498DB", fg="white", font=("Helvetica", 12))
        genre_dropdown.pack(pady=10)

        genre_dropdown.place(x=custom_movie_app.window.winfo_width() - genre_dropdown.winfo_width() - 230, y=10)

        # Search button
        search_button = tk.Button(custom_movie_app.window, text="Search", command=lambda: custom_movie_app.search_movie(custom_movie_app.search_variable.get(), genre_variable.get()), bg="#3498DB", fg="white", bd=0, width=15, height=2, font=("Helvetica", 12))
        search_button.pack(pady=10)

        # Popular movies button
        popular_button = tk.Button(custom_movie_app.window, text="Popular Movies", command=custom_movie_app.fetch_popular_movies, bg="#3498DB", fg="white", bd=0, width=15, height=2, font=("Helvetica", 12))
        popular_button.pack(pady=10)

        popular_button.place(x=custom_movie_app.window.winfo_width() - popular_button.winfo_width() - 150, y=10)

        # Frames for displaying movie details, poster, and navigation
        details_frame = tk.Frame(custom_movie_app.window, bg="#ECF0F1", bd=2, relief=tk.SOLID)
        details_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        poster_frame = tk.Frame(custom_movie_app.window, bg="#2C3E50")
        poster_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        navigation_frame = tk.Frame(custom_movie_app.window, bg="#2C3E50")
        navigation_frame.pack(pady=10)

        # Navigation buttons
        next_button = tk.Button(navigation_frame, text="Next", command=custom_movie_app.next_page, bg="#3498DB", fg="white", bd=0)
        next_button.pack(side=tk.RIGHT, padx=10)

        back_button = tk.Button(navigation_frame, text="Back", command=custom_movie_app.prev_page, bg="#3498DB", fg="white", bd=0)
        back_button.pack(side=tk.LEFT, padx=10)

        # Configure grid for responsive layout
        custom_movie_app.window.grid_rowconfigure(1, weight=1)
        custom_movie_app.window.grid_columnconfigure(0, weight=1)

        # Labels for displaying movie details
        custom_movie_app.details_text_variable = tk.StringVar()
        details_label = tk.Label(details_frame, textvariable=custom_movie_app.details_text_variable, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", justify=tk.CENTER)
        details_label.pack(expand=True, fill=tk.BOTH, pady=(10, 0))

        custom_movie_app.overview_text_variable = tk.StringVar()
        overview_label = tk.Label(details_frame, textvariable=custom_movie_app.overview_text_variable, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", wraplength=500, justify=tk.CENTER)
        overview_label.pack(expand=True, fill=tk.BOTH, pady=(0, 10))

        # Label for displaying movie poster
        custom_movie_app.poster_label = tk.Label(poster_frame, text="", bg="#2C3E50", bd=5, relief=tk.RAISED)
        custom_movie_app.poster_label.pack(expand=True)

    def show_info_page(custom_movie_app):
        # Display the information page with app details
        custom_movie_app.clear_widgets()

        canvas = tk.Canvas(custom_movie_app.window, width=800, height=750, bg="#2C3E50")
        canvas.pack()

        details_bg_image = Image.open("details.png")
        details_bg_image = details_bg_image.resize((800, 750))
        details_bg_photo = ImageTk.PhotoImage(details_bg_image)

        canvas.create_image(0, 0, anchor=tk.NW, image=details_bg_photo)

        app_details_frame = tk.Frame(canvas, bg="#ECF0F1", bd=2, relief=tk.SOLID)
        app_details_frame.pack(pady=70, padx=100, fill=tk.BOTH, expand=True)

        details_title_label = tk.Label(app_details_frame, text="Details", font=("Arial", 14, "bold"), bg="#ECF0F1", fg="#2C3E50")
        details_title_label.pack(pady=(70, 0))

        app_details_text_variable = tk.StringVar()
        app_details_text_variable.set(
            "Discover the CustomMovieApp - Your Movie Companion!\n\n"
            "Explore movies easily with our app. Get details like release dates, ratings, and more.\n\n"
            "Read engaging movie descriptions. View stunning movie posters\n\n"
            "Effortless searching for your favorite films. Discover similar movies with ease.\n\n"
        )

        details_label = tk.Label(app_details_frame, textvariable=app_details_text_variable, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", justify=tk.CENTER)
        details_label.pack(expand=True, fill=tk.BOTH, pady=(70, 200))

        back_button = tk.Button(canvas, text="Back to Home", command=custom_movie_app.show_main_page, bg="#3498DB", fg="white", bd=0)
        back_button.pack(pady=20)

        custom_movie_app.window.winfo_children()[-1].lower()

    def clear_search_text(custom_movie_app, event):
        # Clear the default search text when the entry is clicked
        if custom_movie_app.search_variable.get() == "Search movies...":
            custom_movie_app.search_variable.set("")

    def fetch_movie_genres(custom_movie_app):
        # Fetch movie genres from the API
        genres_url = "https://api.themoviedb.org/3/genre/movie/list"
        params = {"api_key": custom_movie_app.api_key}
        try:
            response = requests.get(genres_url, params=params)
            response.raise_for_status()
            genres_data = response.json()
            if genres_data.get("genres"):
                return [genre["name"] for genre in genres_data["genres"]]
            else:
                return []
        except requests.exceptions.RequestException as e:
            # Show an error message if there's an issue fetching genres
            messagebox.showerror("Error", f"Error fetching movie genres: {e}")
            return []

    def search_movie(custom_movie_app, query, genre):
        # Search for movies based on the provided query and genre
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return

        params = {
            "api_key": custom_movie_app.api_key,
            "query": query,
            "page": custom_movie_app.page_number,
            "with_genres": custom_movie_app.get_genre_id(genre)
        }

        try:
            response = requests.get(custom_movie_app.search_endpoint, params=params)
            response.raise_for_status()
            movie_data = response.json()
            if movie_data.get("results"):
                first_movie = movie_data["results"][0]

                custom_movie_app.display_movie_details(first_movie)
                custom_movie_app.display_movie_poster(first_movie)
                custom_movie_app.last_query = query

            else:
                messagebox.showinfo("Information", "No results found.")
        except requests.exceptions.RequestException as e:
            # Show an error message if there's an issue with the API request
            messagebox.showerror("Error", f"Error: {e}")

    def fetch_popular_movies(custom_movie_app):
        # Fetch popular movies from the API
        params = {
            "api_key": custom_movie_app.api_key,
            "page": 1
        }

        try:
            response = requests.get(custom_movie_app.tv_endpoint, params=params)
            response.raise_for_status()
            movie_data = response.json()
            if movie_data.get("results"):
                first_movie = movie_data["results"][0]

                custom_movie_app.display_movie_details(first_movie)
                custom_movie_app.display_movie_poster(first_movie)
                custom_movie_app.last_query = "Popular Movies"

            else:
                messagebox.showinfo("Information", "No results found.")
        except requests.exceptions.RequestException as e:
            # Show an error message if there's an issue fetching popular movies data
            messagebox.showerror("Error", f"Error fetching popular movies data: {e}")

    def display_movie_details(custom_movie_app, movie_data):
        # Display details of the selected movie
        title = movie_data.get("title", "N/A")
        overview = movie_data.get("overview", "No overview available.")
        release_date = movie_data.get("release_date", "N/A")
        language = movie_data.get("original_language", "N/A")
        rating = movie_data.get("vote_average", "N/A")
        movie_id = movie_data.get("id", "N/A")

        details_text = f"Title: {title}\nRelease Date: {release_date}\n"
        details_text += f"Language: {language}\nRating: {rating}\nMovie ID: {movie_id}\n"

        custom_movie_app.details_text_variable.set(details_text)
        custom_movie_app.overview_text_variable.set(f"Overview: {overview}")

    def display_movie_poster(custom_movie_app, movie_data):
        # Display the poster of the selected movie
        poster_path = movie_data.get("poster_path")

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            poster_image_data = requests.get(poster_url).content

            poster_image = Image.open(io.BytesIO(poster_image_data))
            poster_image = poster_image.resize((150, 200))

            photo_image = ImageTk.PhotoImage(poster_image)

            custom_movie_app.poster_label.configure(image=photo_image, compound=tk.TOP)
            custom_movie_app.poster_label.image = photo_image

        else:
            messagebox.showinfo("Information", "No image available.")

    def next_page(custom_movie_app):
        # Display the next page of search results
        custom_movie_app.page_number += 1
        custom_movie_app.search_movie(custom_movie_app.last_query, "")

    def prev_page(custom_movie_app):
        # Display the previous page of search results
        if custom_movie_app.page_number > 1:
            custom_movie_app.page_number -= 1
            custom_movie_app.search_movie(custom_movie_app.last_query, "")

    def get_genre_id(custom_movie_app, genre_name):
        # Get the genre ID based on the genre name
        for genre in custom_movie_app.genres:
            if genre == genre_name:
                return genre
        return None

    def clear_widgets(custom_movie_app):
        custom_movie_app.last_query = ""

        for widget in custom_movie_app.window.winfo_children():
            if widget != custom_movie_app.nav_toggle_button:
                widget.destroy()

if __name__ == "__main__":
    root_window = tk.Tk()
    app = MovieflixApplication(root_window)
    root_window.mainloop()
