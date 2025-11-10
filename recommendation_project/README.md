# Simple Movie Recommendation System

A command-line movie recommender using content-based filtering.

## Installation
```bash
python movie_recommender.py
```

## Usage
1. View movies
2. Rate some movies (1-5 stars)
3. Get personalized recommendations

## Features
- Content-based filtering algorithm
- Genre and tag matching
- User preference learning
```

**3. requirements.txt:**
```
numpy>=1.20.0
```

### Create ZIP Archive:
```
movie-recommender/
├── movie_recommender.py
├── README.md
├── requirements.txt
└── report.pdf (export the report as PDF)
```

### Create GitHub Repository:
1. Go to github.com → New Repository
2. Name it "movie-recommender"
3. Upload these files
4. Update the GitHub URL in the report

## Key Features:

**Super simple** - Single Python file, no database
**No web dependencies** - Just command-line
**Working algorithm** - Real content-based filtering
**Complete report** - All requirements met
**Ready to submit** - Just update GitHub URL

## How It Works:
```
User rates movies → System calculates similarity → 
Weights by ratings → Ranks recommendations → 
Shows top 3 matches