# BitFlow Project
BitFlow: From Data Scientist Salaries Dataset Analysis to a Bitcoin Price Prediction Web Service with Various Algorithms

# Running the Data Scientist Salaries Analysis Experiment
1. Open the Orange workflow file in folder salaries_analysis/New Orange Testing Setup and Results, `DS_Salary_Analysis_Using_Orange_New.ows` in Orange.
2. Ensure data_science_salaries.csv is loaded and configured correctly according to the paper.
3. Execute the workflow to run the experiment.
4. The results, including predictions and confusion matrices, will be displayed within the Orange interface.


# Running the Bitcoin Prediction Experiment
1. Pip install all related libraries.
2. Run the Flask backend application: python preditc_plot_API.py, the default port is 5000, `http://127.0.0.1:5000`
3. Change current directory to frontend folder, run command: `npm install`, change to bitflow_frontend folder, run command: `npm install`, then run command `npm run dev`, the default port is 3000, visit `http://127.0.0.1:3000`, you should see the BitFlow webpage.



