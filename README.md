# Installation

This project uses UV for dependency management. To set up the environment:

```bash
uv venv eleven_env --python=3.12
source eleven_env/bin/activate # Activate it 
uv pip install -e . # Use the pyproject.toml to install dependencies

```

Fetch data [here](https://oneleven-my.sharepoint.com/personal/salah_mahmoudi_eleven-strategy_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fsalah%5Fmahmoudi%5Feleven%2Dstrategy%5Fcom%2FDocuments%2FHackathon%20X%2DHEC%202024%2FEndless%20Line%20Project%2FData&ga=1) and store it inside a *data* folder.

Then, run ``python3 scripts/extract_and_merge_park_data.py`` in your terminal to generate the portaventura_world_data.csv file.

# Analysis and results

Our analysis and results are documented in the [final_notebook](final_notebook.ipynb).

We created a streamlit dashbord to adress the park director's pain points. To access it, run ``python3 scripts/dashboard.py`` in your terminal.
