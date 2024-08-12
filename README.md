# College Recommendation System Using Neural Networks

## Features
- **Desired Major**
- **College Area** (rural to city)
- **Cost Range**
- **Distance from Home**
- **SAT Score**
- **GPA**
- **Acceptance Range**
- **Home Zip Code**

## Data Fetching
- **Source**: National Center for Education Statistics (NCES)
- **Method**: Fetch data using the `requests` library

## Data Wrangling
- **Libraries**: `numpy`, `pandas`, `matplotlib`
- **Tasks**:
  - Normalize data
  - Handle missing values
  - Perform exploratory data analysis

## Neural Network
- **Architecture**: Custom 2-layer Neural Network
- **Implementation**: Built from scratch using `numpy`, linear algebra, and calculus

## Full Stack Implementation
- **Framework**: Flask
- **Purpose**: Provides a user-friendly interface for the recommendation system

## Running the Program
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Run the flask server:
   ```bash 
   python app.py