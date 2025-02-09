#🚖 NYC Taxi Fare Price Prediction  

📌 Project Overview  

This project aims to predict taxi fare prices based on key ride features such as trip distance, passenger count, and payment type. Using machine learning, we analyze historical taxi trip data to build a predictive model that helps estimate fares accurately.

📊 Dataset Description  

The dataset consists of taxi ride records with the following key attributes:

Passenger Count – Number of passengers in the taxi.
Trip Distance – Distance traveled during the trip (in miles).
Payment Type – Method of payment (Card/Cash).
Fare Amount – Actual fare paid for the ride.
Trip Duration – Time taken for the trip (in minutes).
🛠️ Technologies Used
Python (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn)
Machine Learning Algorithms (Linear Regression, Decision Trees, Random Forest)
Data Visualization (Heatmaps, Histograms)

📈 Model Development  

Data Preprocessing:

Handling missing values and duplicates.
Encoding categorical variables (payment type).
Feature scaling for better model performance.
Exploratory Data Analysis (EDA):

Correlation heatmaps to understand feature relationships.
Distribution plots for fare amount and trip distance.
Model Training & Evaluation:

Implemented Linear Regression, Decision Trees, and Random Forest.
Evaluated performance using MAE, MSE, and R² Score.  

🔍 Key Insights
Trip distance is the most significant factor in fare prediction.
Card payments tend to have slightly higher fares compared to cash.
Short trips sometimes have unexpectedly high fares due to base charges.

