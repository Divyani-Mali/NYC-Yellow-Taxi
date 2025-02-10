🚖 NYC Taxi Fare Price Prediction  

📌 Project Overview  

This project aims to predict taxi fare prices based on key ride features such as trip distance, passenger count, and payment type. Using machine learning, we analyze historical taxi trip data to build a predictive model that helps estimate fares accurately.

📊 Dataset Description  

1. The dataset consists of taxi ride records with the following key attributes:

2. Passenger Count – Number of passengers in the taxi. 

3. Trip Distance – Distance traveled during the trip (in miles).

4. Payment Type – Method of payment (Card/Cash).

5. Fare Amount – Actual fare paid for the ride.

6. Trip Duration – Time taken for the trip (in minutes).

🛠️ Technologies Used

1. Python (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn)

2. Machine Learning Algorithms (Linear Regression, Decision Trees, Random Forest)

3. Data Visualization (Heatmaps, Histograms)

📈 Model Development  

  Data Preprocessing:

1. Handling missing values and duplicates.

2. Encoding categorical variables (payment type).

3. Feature scaling for better model performance.

4. Exploratory Data Analysis (EDA):

5. Correlation heatmaps to understand feature relationships.

6. Distribution plots for fare amount and trip distance.

    Model Training & Evaluation:

    Implemented Linear Regression.

    Evaluated performance using MAE, MSE, and R² Score.  


Trip distance is the most significant factor in fare prediction.
Card payments tend to have slightly higher fares compared to cash.
Short trips sometimes have unexpectedly high fares due to base charges.

