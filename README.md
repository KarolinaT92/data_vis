## Virtual Environment Setup
1.Create and activate the virtual environment
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
```

2. Install the required packages
```bash         
pip install -r requirements.txt
```

3. To register the environment as a Jupyter kernel:
```bash
python -m ipykernel install --user --name=[myenv] --display-name "Data visualisation (myenv)"
```

## Paths to data files setup
This project uses a `.env` file to store the locations of all dataset files.
First, create a `.env` file in the root directory of the project by copying the provided `.env.example` file.
Then, replace the placeholder paths with the actual paths to your data files. 

For example:
```plaintext
POSTINGS_CSV_PATH=real/path/to/your/postings.csv
```