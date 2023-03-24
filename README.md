# PIC16B Group Project -- Visualizing The Zillow Home Distribution
### By: Ryan, Emily, Aram, and Jun


## Description
The goal of this project was for users to understand the distribution of homes for sale on Zillow. Typically, prospective home buyers and sellers go to Zillow to find similar homes in order to gain an understanding of a given house's value. Our project would give users a better understanding as it would explain the entire housing market for a given city. This includes geographic visualizations, histograms and scatterplots, and a predictive model that works with user data. We decided to limit our focus to the top ten major cities in the United States: Los Angeles, San Antonio, Phileadelphia, San Diego, Houston, Dallas, Phoenix, New York, Chicago, and San Jose. Using the api, we were able to obtain information on 1500 homes for each city with 30 features.  

## Instructions
1) Clone the repository and unzip it. In the command prompt, navigate to PIC16B_Group_Project>tutorial_zillow>flask and run the command "flask run." Note: You may need to install some packages like plotly pandas and flask using the pip install command.

2) The first page is a map of the United States with interactive buttons on the ten most populated cities. Simply select the city of interest and it will take you to the next page. 

3) On the geographic visualization page, you will see a scatter plot and heat map for all homes we have obtained data for. Both of these maps are zoom adjustable and each point provides information when hovered over. At the bottom of the page, we added some filters that can be played around with so you can update the two maps with preferences. You can adjust things like home type, price range, mumber of bedrooms, etc. You should then select the data collection and prediction link on the top of the page. 

4) On the data collection and prediction page, you can now enter in information for a potential home of interest. After entering in number of bathrooms, number of bedrooms, square footage, zip code, and home type, you can click the submit button and see a price prediction on the top of the screen. We added some conditions that you must satisfy when entering in information. Next, you should click on the data visualization page.

5) On the data visualization page, you will be provided with six scatter plots and three histograms with each plot containing a marker to illustrate your entered information. The first three scatter plots show the count of the number of homes compared to bedrooms, bathrooms, and square footage. The next three scatter plots show the median price of homes compared to bedrooms, bathrooms, and square footage. The three histograms show pairwise count plots for the aforementioned features. All of these plots are adjustable as they were coded with Plotly. The goal of this page is for you to understand where your home compares to the rest of the market. The final optional link to select is the view data page. 

6) On the view data page, you can see the dataframe for the selected city with all features listed. You can also change the city of interest with the drop down at the top. 


