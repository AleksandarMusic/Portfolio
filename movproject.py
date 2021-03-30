import csv


class MovieCollection():
    def __init__(self, file_name = "movies.csv"):
        self.file_name = file_name
        self.default_keys = ["Title", "Directors", "Year"]
        
    def add(self):
        # Adds new movie to collection.
        title = input("Enter title of movie: ")
        directors = input("Enter directors: ")
        
        while True:
            year = input("Enter year of release: ")

            try:
                int(year)
                print("")
                break
            except ValueError:
                print("Invalid input.")
        
        new_movie = {
            "Title" : title, 
            "Directors" : directors, 
            "Year" : year
        }

        try:
            with open(self.file_name, "a+", newline = "") as mov_file:
                # Opens csv file which has same name as 'self.file_name'. Creates file if does not exist.
                mov_file.seek(0)
                read_mov = csv.reader(mov_file)
                
                try:
                    # If header exists, use header as as fieldnames for DictWriter, then add value from
                    # 'new_movie' to corresponding columns
                    new_keys = next(read_mov)

                    write_mov = csv.DictWriter(mov_file, new_keys)
                    write_mov.writerow(new_movie)
                except StopIteration:
                    # Otherwise, writes 'self.default_keys' into header, then adds values from 'new_movie'
                    # to corresponding columns.
                    write_mov = csv.writer(mov_file)
                    write_mov.writerow(self.default_keys)
                    
                    write_mov = csv.DictWriter(mov_file, self.default_keys)
                    write_mov.writerow(new_movie)

            print(f"{title} added to collection.\n")
        except PermissionError:
            print("Could not add movie. File in use by another process.\n")

    def print_movie(self, row):
        # Prints title, directors, and year of movie contained in row (of csv file) passed in.
        title = "Title: " + row["Title"]
        directors = "Directors: " + row["Directors"]
        year = "Year: " + row["Year"]

        print(title, directors, year, sep = ", ")

    def view_all(self):
        # Displays all movies in collection.
        num_movies = 0

        try:
            with open(self.file_name) as mov_file:
                read_mov = csv.DictReader(mov_file)

                for row in read_mov:
                    self.print_movie(row)
                    num_movies += 1

            print(f"{num_movies} movie(s) in collection.\n")
        except FileNotFoundError:
            print("Collection not found. Add a movie to create collection.\n")

    def search(self):
        # Searches for keyword in titles, directors, or years of movies in collection. Displays results.
        while True:
            category = input("Search for title, directors, or year?: ").title()
            low_category = category.lower()

            if low_category == "title" or low_category == "directors" or low_category == "year":
                break
            else:
                print("Invalid input.")

        search_term = input("Search for: ")
        print("")
        low_search = search_term.lower()
        found_count = 0

        try:
            with open(self.file_name) as mov_file:
                read_mov = csv.DictReader(mov_file)
                row_count = 0

                for row in read_mov:
                    row_count += 1

                    if low_search in row[category].lower():
                        self.print_movie(row)
                        found_count += 1

                if row_count:
                    print(f"{found_count} movie(s) found with {low_category} containing \"{search_term}\".\n")
                else:
                    print("0 movies in collection.\n")

        except FileNotFoundError:
            print("Collection not found. Add a movie to create collection.\n")

    def prompt(self):
        while True:
            task = input("Enter 'a' to add a movie, 'v' to view all movies, 's' to search movies, or 'q' to quit: ").lower()
            print("")

            if task == "a":
                self.add()   
            elif task == "v":
                self.view_all()
            elif task == "s":
                self.search()
            elif task == "q":
                break
            else:
                print("Invalid input. Do not include quotation marks.\n")

def main():
    file_name = input("Enter movie collection filename, or leave blank to use default filename. Enter 'q' to quit: ")
    print("")

    if not file_name:
        my_collection = MovieCollection()
        my_collection.prompt()
    elif file_name != "q":
        my_collection = MovieCollection(file_name)
        my_collection.prompt()

if __name__ == "__main__":
    main()
