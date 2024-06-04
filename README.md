# Framework for the Analysis of Photographic Archival Data of the Kunsthistorisches Institut in Florenz

## Introduction
This framework is designed to help scholars analyze the collection data from the [Photothek](https://www.khi.fi.it/en/photothek/index.php), the photographic archive of the [Kunsthistorisches Institut in Florenz (KHI)](https://www.khi.fi.it/en/index.php). The Photothek houses over 630,000 photographs, with a significant part already digitized and available on the [Digital Photothek](https://photothek.khi.fi.it/) website.

The framework is available as a Jupyter Notebook, an interactive tool where you can directly execute your analyses following the provided instructions. You can launch the notebook using Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AlessandraFa/photo-archive-data-analysis-framework.git/HEAD?labpath=Photo_Data_Analysis_KHI.ipynb)

## Features
### What is this framework?
This framework includes tools for analyzing and visualizing photographic archival data. It is designed to be user-friendly, even for those with limited programming experience.
### Who can use this framework?
This framework is for scholars, researchers, and anyone interested in analyzing the Photothek's collections. It's especially helpful for users with little or no programming knowledge.
### What is Jupyter Notebook?
Jupyter Notebook is a web app that lets you create and share documents with live code, equations, visualizations, and text. It's popular in data science and research.
### Why Use Binder?
Binder is an online platform that allows you to run Jupyter Notebooks in your web browser without needing to install any software. It's a convenient tool for users who want to analyze data interactively.
### What kind of data can I analyse?
You can analyze your own Photothek datasets if you have requested and obtained them from the KHI, or you can use the provided test datasets. The datasets should be in XML format.
### Is it compatible with my device?
Yes, the framework is compatible with Windows, macOS, and Linux. You can also access it through web browsers like Chrome, Firefox, or Safari. However, it's recommended to run the framework on a PC rather than a mobile device.
## Usage
### Using Binder
Run the notebook through Binder without installing anything on your computer:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AlessandraFa/photo-archive-data-analysis-framework.git/HEAD?labpath=Photo_Data_Analysis_KHI.ipynb)
### Running Locally (Optional)
If you prefer to run the notebook on your own computer, follow these steps:
#### Prerequisites
- [Install Python](https://www.python.org/getit/)
- [Install Jupyter](https://jupyter.org/install)
  
#### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/AlessandraFa/photo-archive-data-analysis-framework.git
    ```
2. Go to the project directory:
    ```bash
    cd photo-archive-data-analysis-framework
    ```
3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
4. Start the Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
## Functionalities Overview
- **Data Extraction:** Automatically extract data from XML files.
- **Data Analysis Methods:**  Tools for filtering, sorting, and other analysis tasks.
- **Visualization Tool:** Interactive tools for creating visualizations of different types.
- **File Download** Download the data to your PC in CSV format.
The notebook provides detailed instructions, glossaries, and guides to help you navigate and use the framework effectively.

## Examples
Here, you can find some examples of framework application to analyse and visualise data.

1. You can **filter** your data using the dedicated filtering tool. The following image shows an example of data filtered by artist name "Brunelleschi, Filippo". Each row in the table (which is in DataFrame structure) displays data about a single photograph:

<img src="https://github.com/AlessandraFa/photo-archive-data-analysis-framework/assets/72857617/a8bed09f-e3b0-4ba6-a1a0-9fc4ebb7137e"></img>

2. You can view **individual artwork details** by specifying their unique IDs in the dedicated tool. Details about artwork 07703279 ("Primavera" by Sandro Botticelli) are shown in the following image:

<img src="https://github.com/AlessandraFa/photo-archive-data-analysis-framework/assets/72857617/f9260374-0958-4dda-beb3-507a970e6bc6"></img>

3. By using photograph IDs as input, you can view details about **individual photographs**. The following image shows details for the photograph 3188:

<img src="https://github.com/AlessandraFa/photo-archive-data-analysis-framework/assets/72857617/cf560957-fa63-41d8-9368-4cc8adcccc17"></img>

4. You can create different types of **data visualisation**. The following image shows the artistic genre representation within a photographic collection as a **donut chart**:

<img src="https://github.com/AlessandraFa/photo-archive-data-analysis-framework/assets/72857617/16d5ce2c-3874-4b90-adc1-6823d5c4a850"></img>

5. You can also represent your data through a **bar chart**. The following image shows data about artist representation within a collection:

<img src="https://github.com/AlessandraFa/photo-archive-data-analysis-framework/assets/72857617/a8bf1d91-60af-44e6-b94a-f0de591b5b94"></img>

6. Representing data using a **line chart** is a further option within the framework. The following image shows the distribution of photographs by their date of creation:

<img src="https://github.com/AlessandraFa/photo-archive-data-analysis-framework/assets/72857617/a9b3b700-cb38-42f0-a20a-8ac317d7a314"></img>

## Additional Resources
- Jupyter Notebook Documentation: https://docs.jupyter.org/en/latest/
- Python Documentation: https://docs.python.org/3/
- Pandas Documentation: https://pandas.pydata.org/docs/
- Matplotlib Documentation: https://matplotlib.org/stable/index.html
- Seaborn Documentation: https://seaborn.pydata.org/
- Plotly Documentation: https://plotly.com/graphing-libraries/

## Acknowledgements 
This project owes its realization to the collaboration of the  [Photothek](https://www.khi.fi.it/en/photothek/index.php) of the [Kunsthistorisches Institut in Florenz (KHI)](https://www.khi.fi.it/en/index.php). Their provision of data and permission to access and work with this information made this project come to fruition.

## Support
For assistance or questions please contact [Alessandra Failla](alessandra.failla@hotmail.it).

## License
This project is licensed under the GNU General Public License. See the [LICENSE](LICENSE) file for details.
