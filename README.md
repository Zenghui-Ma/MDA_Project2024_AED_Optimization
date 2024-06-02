# AED Optimization Project for Modern Data Analytics Course
## Introduction
In this project, a machine learning model was built to predict survival rates for out-of-hospital cardiac arrest using intervention, hospital and AED information. Additionally, a web application was developed via Dash and Plotly to visualize the survival information with relation to locations of AEDs and hospitals, and to enable users to interactively add new AEDs to explore AED optimization possibilities.
## Usage
### Remote Access
The app has been deployed on Heroko, users can simply access the APP via the link below:

[https://mdamainpage-26dd5ba1b110.herokuapp.com](https://mdamainpage-26dd5ba1b110.herokuapp.com)

or via this QR code:

![QR Code](assets/heroku_app_qr.png)


### Local Installment
Alternatively, users can access the app locally. Please first clone the repository and open the files, and then run the command below to install all the required packages listed in `requirements.txt`.
```
python -m pip install -r requirements.txt
```
## Repository Structure
```
├── CSS
├── __pycache__
│   ├── aed_location_existed.cpython-310.pyc
│   └── find_nearest_aed_center.cpython-310.pyc
├── aed_location_existed.py
├── aed_survival_pipeline.pkl
├── app.py
├── app1.py
├── app2.py
├── app3.py
├── assets 
│   ├── aed_new.png
│   ├── aed_new.webp
│   ├── aed_old.png
│   ├── green_person.png
│   ├── red_person.png
│   └── slider.css
├── data   # data files
│   ├── AED_locations.xlsx
│   ├── hospitals.xlsx
│   ├── intervention_all.xlsx
│   └── intervention_all0528.xlsx
├── find_nearest_aed_center.py
├── fonts # fonts files
├── machinelearning_model 
│   └── kmeans_model.pkl
├── model.py 
├── mortality_with_new_AED.py 
├── page1.py 
├── pages 
├── preprocess # pre-processing and model-building files
│   ├── Building_model.ipynb
│   └── preprocessing.ipynb
├── structure.txt  # repository structure
├── temp.py
└── test.ipynb

9 directories, 28 files
```
