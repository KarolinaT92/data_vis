## Overview

This repository contains an interactive Dash-based data visualization application used to explore business data across multiple dimensions such as customers, products, and shipments.
The application is organized into separate tabs, each responsible for a specific domain, and uses shared filters and layout components to keep behavior consistent across the app.

## Virtual Environment Setup
1. Clone the repository:
```bash
git clone https://github.com/KarolinaT92/data_vis.git
cd data_vis
```

2. Create and activate the virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
```

3. Install the required packages:
```bash         
pip install -r requirements.txt
```

4. To register the environment as a Jupyter kernel:
```bash
python -m ipykernel install --user --name=[myenv] --display-name "Data visualisation (myenv)"
```

## Paths to data files setup
This project uses a `.env` file to store the locations of all dataset files.
First, create a `.env` file in the root directory of the project by copying the provided `.env.example` file.
Then, replace the placeholder paths with the actual paths to your data files. 

For example:
```plaintext
PATH=real/path/to/your/data.csv
```
## Running the Application

1. From the project root directory:
```bash
python -m dashApp.app
```

2. Once the server starts, open the app in your browser:
```cpp
http://127.0.0.1:8050/
```
