# AED Optimization Project for Modern Data Analytics Course
## Introduction
In this project, a machine learning model was built to predict survival rates for out-of-hospital cardiac arrest using intervention, hospital and AED information. Additionally, a web application was developed via Dash and Plotly to visualize the survival information with relation to locations of AEDs and hospitals, and to enable users to interactively add new AEDs to explore AED optimization possibilities.
## Usage
### Remote Access
The app has been deployed on Heroko, users can simply access the APP via the link below:

[https://mdamainpage-26dd5ba1b110.herokuapp.com](https://mdamainpage-26dd5ba1b110.herokuapp.com)

or via this QR code:

![QR Code](/pages/assets/heroku_app_qr.png)


### Local Installment
Alternatively, users can access the app locally. Please first clone the repository and open the files, and then run the command below to install all the required packages listed in `requirements.txt`.
```
python -m pip install -r requirements.txt
```
## Repository Structure
```
MDA_Project2024_AED_Optimization/
├── data/
│   ├── file1
│   ├── file2
├── preprocess/
│   ├── file1
│   ├── file2
├── model/
│   ├── aed_survival_pipeline.pkl
│   ├── model.py
├── pages/
│   ├── app7.py
│   ├── page1.py
│   ├── layout.py
│   ├── page2.py
│   ├── main.py
│   ├── assets/
├── deploy/
│   ├── directory_structure.txt
│   ├── structure.py
│   ├── QR_code.py
├── README.md
├── requirements.txt


```
