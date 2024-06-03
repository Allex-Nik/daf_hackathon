# DAF PLANNER SYSTEM

## Files

- `API_` - folder with code which extracts the data through api
- `app` - file where we create the framework
- `data` - folder in which we store needed data from apis or external datasets
- `config.py` - configuration file
- `requirements.txt` - file which stores all used libraries 

## How to Run

### Prerequisites

1. **Python 3.10+**: Ensure you have Python 3.7 or later installed.
2. **API Key**: Obtain an API key for the Google Maps API and update the `config.py` file.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Allex-Nik/daf_hackathon
    cd route-planner
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. **API Key**: Ensure your `config.py` file contains your Google Maps API key:
    ```python
    # config.py
    API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'
    ```

### Running the Application

1. **Run the Streamlit app**:
    ```bash
    streamlit run app/main.py  
    ```

2. **Access the app**: Open your web browser and go to `http://localhost:8501`.

### Usage

1. **Enter the Origin and Destination**: Use the sidebar to input the origin and destination of your route.
2. **View the Route**: The app will display the best route on a map.
