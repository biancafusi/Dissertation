
# Exploring Cold Pool Dynamics in MONAN: Insights from Numerical Simulations of Hurricanes

This repository is part of my Master's Degree research, where I gather and organize all the code used throughout my dissertation.

During my Master's, I used the [MONAN system](https://github.com/monanadmin/MONAN-Model) to investigate the influence of cold pools on two hurricanes from the 2024 North Atlantic season: Hurricanes **Beryl** and **Helene**. To evaluate the behavior of this parameterization, I analyzed three key metrics commonly used in the literature: **track**, **intensity**, and **precipitation**.

> The full dissertation PDF will be uploaded here after the defense. A paper based on this research is currently in progress.

---

## Project Structure

Below is an overview of the main folders in this repository:


```
.
├── extra_coding/       # MONAN configuration files for each hurricane case
├── hurricane_helene/          # Scripts to generate domains and cold pool masks (e.g., shapefiles)
├── hurricane_beryl/       # Main simulation scripts and post-processing routines
├── env/             # Conda environment files and package list
└── docs/            # Supporting documentation and notes
```

Feel free to suggest improvements to the structure!

---

## Disclaimer

The codes were written with robustness and modularity in mind, following a standard flow:

namelist + auxiliar codes → main simulation/processing code

However, since this is academic work, some parts may still be optimized or reorganized. Suggestions are very welcome and can be sent to **bih.fusinato@gmail.com**.

---



## Installation

To run the code:

1. Clone this repository:
   ```bash
   git clone https://github.com/biancafusi/your-repo-name.git
   cd your-repo-name

2. (Recommended) Create a Conda environment:

    ```bash
    conda env create --file env/environment.yml

3. Run individual scripts manually following the flow mentioned above.

### Libraries needed

Make sure to check the conda_requirements.yml file for the specific package versions used.
## Author

- [@biancafusi](https://www.github.com/biancafusi)

