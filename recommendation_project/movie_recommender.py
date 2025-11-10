"""
Simple Movie Recommendation System
A basic content-based recommendation system using Python
"""

import numpy as np
from collections import defaultdict

class MovieRecommender:
    def __init__(self):
        # Sample movie database
        self.movies = {
            1: {"title": "The Matrix", "genre": "Sci-Fi", "year": 1999, "tags": ["action", "philosophy"]},
            2: {"title": "Inception", "genre": "Sci-Fi", "year": 2010, "tags": ["mind-bending", "action"]},
            3: {"title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "tags": ["hope", "friendship"]},
            4: {"title": "Pulp Fiction", "genre": "Crime", "year": 1994, "tags": ["non-linear", "crime"]},
            5: {"title": "The Dark Knight", "genre": "Action", "year": 2008, "tags": ["superhero", "crime"]},
            6: {"title": "Forrest Gump", "genre": "Drama", "year": 1994, "tags": ["inspirational", "historical"]},
            7: {"title": "Interstellar", "genre": "Sci-Fi", "year": 2014, "tags": ["space", "family"]},
            8: {"title": "Parasite", "genre": "Thriller", "year": 2019, "tags": ["social", "dark-comedy"]},
        }
        
        self.user_ratings = {}  # Stores user ratings: {movie_id: rating}
        
    def display_movies(self):
        """Display all available movies"""
        print("\n" + "="*60)
        print("AVAILABLE MOVIES")
        print("="*60)
        for movie_id, movie in self.movies.items():
            print(f"{movie_id}. {movie['title']} ({movie['year']})")
            print(f"   Genre: {movie['genre']}")
            print(f"   Tags: {', '.join(movie['tags'])}")
            print()
    
    def rate_movie(self, movie_id, rating):
        """Rate a movie (1-5 scale)"""
        if movie_id in self.movies:
            self.user_ratings[movie_id] = rating
            print(f"Rated '{self.movies[movie_id]['title']}' with {rating} stars")
            return True
        else:
            print("Movie not found")
            return False
    
    def calculate_similarity(self, movie1_id, movie2_id):
        """Calculate similarity score between two movies"""
        movie1 = self.movies[movie1_id]
        movie2 = self.movies[movie2_id]
        
        score = 0
        
        # Genre matching (3 points)
        if movie1['genre'] == movie2['genre']:
            score += 3
        
        # Tag matching (2 points per common tag)
        common_tags = set(movie1['tags']) & set(movie2['tags'])
        score += len(common_tags) * 2
        
        # Year proximity (1 point if within 5 years)
        if abs(movie1['year'] - movie2['year']) <= 5:
            score += 1
        
        return score
    
    def get_recommendations(self, num_recommendations=3):
        """Generate movie recommendations based on user ratings"""
        if not self.user_ratings:
            print("\nNo ratings yet! Please rate some movies first.")
            return []
        
        # Calculate scores for unrated movies
        scores = {}
        
        for movie_id in self.movies.keys():
            # Skip already rated movies
            if movie_id in self.user_ratings:
                continue
            
            # Calculate weighted score based on user's ratings
            total_score = 0
            for rated_id, rating in self.user_ratings.items():
                similarity = self.calculate_similarity(movie_id, rated_id)
                # Weight similarity by user rating (1-5)
                total_score += similarity * rating
            
            scores[movie_id] = total_score
        
        # Sort by score and get top N recommendations
        sorted_movies = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_recommendations = sorted_movies[:num_recommendations]
        
        return top_recommendations
    
    def display_recommendations(self):
        """Display personalized recommendations"""
        recommendations = self.get_recommendations()

        if not recommendations:
            return

        print("\n" + "="*60)
        print("RECOMMENDED FOR YOU")
        print("="*60)
        
        for i, (movie_id, score) in enumerate(recommendations, 1):
            movie = self.movies[movie_id]
            print(f"{i}. {movie['title']} ({movie['year']})")
            print(f"   Genre: {movie['genre']}")
            print(f"   Match Score: {score:.1f}")
            print(f"   Tags: {', '.join(movie['tags'])}")
            print()
    
    def show_user_profile(self):
        """Display user's rating profile"""
        if not self.user_ratings:
            print("\nNo ratings yet!")
            return
        
        print("\n" + "="*60)
        print("YOUR RATINGS")
        print("="*60)
        
        for movie_id, rating in self.user_ratings.items():
            movie = self.movies[movie_id]
            stars = "*" * rating + "-" * (5 - rating)
            print(f"{movie['title']}: {stars} ({rating}/5)")

        # Show genre preferences
        genre_counts = defaultdict(int)
        for movie_id, rating in self.user_ratings.items():
            if rating >= 4:  # Count only high ratings
                genre_counts[self.movies[movie_id]['genre']] += 1

        if genre_counts:
            favorite_genre = max(genre_counts.items(), key=lambda x: x[1])[0]
            print(f"\nYou seem to enjoy {favorite_genre} movies!")


def main():
    """Main program loop"""
    recommender = MovieRecommender()
    
    print("="*60)
    print("SIMPLE MOVIE RECOMMENDATION SYSTEM")
    print("="*60)
    print("This system learns your preferences and recommends movies!")
    
    while True:
        print("\n" + "-"*60)
        print("MENU")
        print("-"*60)
        print("1. View all movies")
        print("2. Rate a movie")
        print("3. Get recommendations")
        print("4. View your profile")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            recommender.display_movies()
        
        elif choice == '2':
            try:
                movie_id = int(input("Enter movie ID to rate (1-8): "))
                rating = int(input("Enter rating (1-5 stars): "))
                
                if 1 <= rating <= 5:
                    recommender.rate_movie(movie_id, rating)
                else:
                    print("Rating must be between 1 and 5")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
        
        elif choice == '3':
            recommender.display_recommendations()
        
        elif choice == '4':
            recommender.show_user_profile()
        
        elif choice == '5':
            print("\nThanks for using the Movie Recommender!")
            print("="*60)
            break

        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()