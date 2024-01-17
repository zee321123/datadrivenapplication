import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie API App")
        self.root.geometry("800x780")
        self.root.resizable(False, False)

        self.api_key = "7b7ed2aa5697e629fa150e5afe30f132"
        self.search_base_url = "https://api.themoviedb.org/3/search/movie"
        self.tv_base_url = "https://api.themoviedb.org/3/discover/tv"
        self.similar_base_url = "https://api.themoviedb.org/3/movie/{}/similar"
        self.page_number = 1
        self.last_query = ""
        self.genres = self.fetch_movie_genres()  # Fetch movie genres on initialization

        # Set background color to a professional dark shade
        self.root.configure(bg="#2C3E50")

        # Menubutton for Toggle
        self.toggle_button = tk.Menubutton(self.root, text="\u2630", font=("Helvetica", 24), bg="#2C3E50", fg="white", bd=0)
        self.toggle_button.menu = tk.Menu(self.toggle_button, tearoff=0, font=("Helvetica", 14), bg="#2C3E50", fg="white")
        self.toggle_button["menu"] = self.toggle_button.menu
        self.toggle_button.menu.add_command(label="Home", command=self.show_welcome_page)
        self.toggle_button.menu.add_command(label="Movies", command=self.show_movies_page)
        self.toggle_button.menu.add_command(label="Details", command=self.show_details_page)
        self.toggle_button.place(x=10, y=10)

        # Welcome Page
        self.show_welcome_page()

    def show_welcome_page(self):
        # Clear the existing widgets
        self.clear_widgets()

        # Load and display the image
        home_image = Image.open("home.png")
        home_image = home_image.resize((800, 700))
        home_photo = ImageTk.PhotoImage(home_image)

        home_label = tk.Label(self.root, image=home_photo, bg="#2C3E50")
        home_label.image = home_photo
        home_label.pack(pady=60)

    def show_movies_page(self):
        # Clear the existing widgets
        self.clear_widgets()

        # Search Entry
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.root, font=("Helvetica", 16), bg="white", fg="#2C3E50", bd=5, relief=tk.FLAT, textvariable=self.search_var)
        search_entry.insert(0, "Search movies...")
        search_entry.bind("<FocusIn>", self.clear_search_text)
        search_entry.pack(pady=10)

        # Genre Dropdown
        genre_var = tk.StringVar()
        genre_dropdown = tk.OptionMenu(self.root, genre_var, *self.genres)
        genre_dropdown.config(bg="#3498DB", fg="white", font=("Helvetica", 12))
        genre_dropdown["menu"].config(bg="#3498DB", fg="white", font=("Helvetica", 12))
        genre_dropdown.pack(pady=10)

        genre_dropdown.place(x=self.root.winfo_width() - genre_dropdown.winfo_width() - 230, y=10)

        # Search Button with Genre
        search_button = tk.Button(self.root, text="Search", command=lambda: self.search_movie(search_entry.get(), genre_var.get()), bg="#3498DB", fg="white", bd=0, width=15, height=2, font=("Helvetica", 12))
        search_button.pack(pady=10)

        # Popular Movies Button
        popular_button = tk.Button(self.root, text="Popular Movies", command=self.fetch_popular_movies, bg="#3498DB", fg="white", bd=0, width=15, height=2, font=("Helvetica", 12))
        popular_button.pack(pady=10)

        # Place Popular Movies Button at the top right corner
        popular_button.place(x=self.root.winfo_width() - popular_button.winfo_width() - 150, y=10)

        # Frame for Movie Details
        details_frame = tk.Frame(self.root, bg="#ECF0F1", bd=2, relief=tk.SOLID)  # Light background color
        details_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        # Movie Description Title
        details_title_label = tk.Label(details_frame, text="Movie Description", font=("Helvetica", 14, "bold"), bg="#ECF0F1", fg="#2C3E50")
        details_title_label.pack(pady=(10, 0))

        # Movie Poster Frame
        poster_frame = tk.Frame(self.root, bg="#2C3E50")
        poster_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        # Next and Back Buttons
        navigation_frame = tk.Frame(self.root, bg="#2C3E50")
        navigation_frame.pack(pady=10)

        next_button = tk.Button(navigation_frame, text="Next", command=self.next_page, bg="#3498DB", fg="white", bd=0)
        next_button.pack(side=tk.RIGHT, padx=10)

        back_button = tk.Button(navigation_frame, text="Back", command=self.prev_page, bg="#3498DB", fg="white", bd=0)
        back_button.pack(side=tk.LEFT, padx=10)

        # Set weight for rows and columns to make the content centered
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Movie Details Frame
        self.details_text = tk.StringVar()
        details_label = tk.Label(details_frame, textvariable=self.details_text, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", justify=tk.CENTER)
        details_label.pack(expand=True, fill=tk.BOTH, pady=(10, 0))

        # Movie Overview Text
        self.overview_text = tk.StringVar()
        overview_label = tk.Label(details_frame, textvariable=self.overview_text, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", wraplength=500, justify=tk.CENTER)
        overview_label.pack(expand=True, fill=tk.BOTH, pady=(0, 10))

        # Movie Poster Frame
        self.poster_label = tk.Label(poster_frame, text="", bg="#2C3E50", bd=5, relief=tk.RAISED)
        self.poster_label.pack(expand=True)

    def show_details_page(self):
        # Clear the existing widgets
        self.clear_widgets()

        # Create a Canvas widget for the background image
        canvas = tk.Canvas(self.root, width=800, height=750, bg="#2C3E50")
        canvas.pack()

        # Load and display the background image
        details_bg_image = Image.open("details.png")
        details_bg_image = details_bg_image.resize((800, 750))
        details_bg_photo = ImageTk.PhotoImage(details_bg_image)

        canvas.create_image(0, 0, anchor=tk.NW, image=details_bg_photo)

        # Frame for App Details
        app_details_frame = tk.Frame(canvas, bg="#ECF0F1", bd=2, relief=tk.SOLID)  # Light background color
        app_details_frame.pack(pady=70, padx=100, fill=tk.BOTH, expand=True)

        # App Details Title
        details_title_label = tk.Label(app_details_frame, text="Details", font=("Helvetica", 14, "bold"), bg="#ECF0F1", fg="#2C3E50")
        details_title_label.pack(pady=(70, 0))

        # App Details Text
        app_details_text = tk.StringVar()
        app_details_text.set(
            "Discover the MovieflixApp - Your Movie Companion!\n\n"
            "Explore movies easily with our app. Get details like release dates, ratings, and more.\n\n"
            "Read engaging movie descriptions. View stunning movie posters\n\n"
            "Effortless searching for your favorite films. Discover similar movies with ease.\n\n"
        )

        details_label = tk.Label(app_details_frame, textvariable=app_details_text, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", justify=tk.CENTER)
        details_label.pack(expand=True, fill=tk.BOTH, pady=(70, 200))

        # Back to Menu Button
        back_button = tk.Button(canvas, text="Back to Menu", command=self.show_welcome_page, bg="#3498DB", fg="white", bd=0)
        back_button.pack(pady=20)

        # Set the canvas as the last child to make it the background
        self.root.winfo_children()[-1].lower()

    def clear_search_text(self, event):
        if self.search_var.get() == "Search movies...":
            self.search_var.set("")

    def fetch_movie_genres(self):
        genres_url = "https://api.themoviedb.org/3/genre/movie/list"
        params = {"api_key": self.api_key}
        try:
            response = requests.get(genres_url, params=params)
            response.raise_for_status()
            genres_data = response.json()
            if genres_data.get("genres"):
                return [genre["name"] for genre in genres_data["genres"]]
            else:
                return []
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching movie genres: {e}")
            return []

    def search_movie(self, query, genre):
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return

        params = {
            "api_key": self.api_key,
            "query": query,
            "page": self.page_number,
            "with_genres": self.get_genre_id(genre)  # Add genre parameter
        }

        try:
            response = requests.get(self.search_base_url, params=params)
            response.raise_for_status()
            movie_data = response.json()
            if movie_data.get("results"):
                first_movie = movie_data["results"][0]

                # Display movie details
                self.display_movie_details(first_movie)

                # Display movie poster
                self.display_movie_poster(first_movie)

                # Keep track of the last search query
                self.last_query = query

            else:
                messagebox.showinfo("Information", "No results found.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching movie data: {e}")

    def fetch_popular_movies(self):
        params = {
            "api_key": self.api_key,
            "page": 1  # You may adjust the page number as needed
        }

        try:
            response = requests.get(self.tv_base_url, params=params)
            response.raise_for_status()
            movie_data = response.json()
            if movie_data.get("results"):
                first_movie = movie_data["results"][0]

                # Display movie details
                self.display_movie_details(first_movie)

                # Display movie poster
                self.display_movie_poster(first_movie)

                # Keep track of the last search query (in this case, it's not a search query but a category)
                self.last_query = "Popular Movies"

            else:
                messagebox.showinfo("Information", "No results found.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching popular movies data: {e}")

    def display_movie_details(self, movie_data):
        title = movie_data.get("title", "N/A")
        overview = movie_data.get("overview", "No overview available.")
        release_date = movie_data.get("release_date", "N/A")
        language = movie_data.get("original_language", "N/A")
        rating = movie_data.get("vote_average", "N/A")
        movie_id = movie_data.get("id", "N/A")

        # Movie Details Text
        details_text = f"Title: {title}\nRelease Date: {release_date}\n"
        details_text += f"Language: {language}\nRating: {rating}\nMovie ID: {movie_id}\n"

        self.details_text.set(details_text)

        # Movie Overview Text
        self.overview_text.set(f"Overview: {overview}")

    def display_movie_poster(self, movie_data):
        poster_path = movie_data.get("poster_path")

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            poster_image_data = requests.get(poster_url).content

            poster_image = Image.open(io.BytesIO(poster_image_data))
            poster_image = poster_image.resize((150, 200))

            photo_image = ImageTk.PhotoImage(poster_image)

            # Poster Label with Border
            self.poster_label.configure(image=photo_image, compound=tk.TOP)
            self.poster_label.image = photo_image

        else:
            messagebox.showinfo("Information", "No poster available.")

    def next_page(self):
        # Increment page number and search for similar movies
        self.page_number += 1
        self.search_movie(self.last_query, "")

    def prev_page(self):
        # Decrement page number and search for similar movies
        if self.page_number > 1:
            self.page_number -= 1
            self.search_movie(self.last_query, "")

    def get_genre_id(self, genre_name):
        # Get the genre ID based on the genre name
        for genre in self.genres:
            if genre == genre_name:
                return genre
        return None

    def clear_widgets(self):
        # Clear all widgets from the window
        self.last_query = ""  # Clear the last query when clearing widgets

        for widget in self.root.winfo_children():
            if widget != self.toggle_button:
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
