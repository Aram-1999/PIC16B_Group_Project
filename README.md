# PIC16B_Group_Project

. x X
. x .
. O O

https://apify.com/ 
1) Create free account 
2) Search for the Zillow Real Estate API scraper
3) Enter one of the following cities  

    -"Chicago"  
    -"Huston
    -"Phoenix"
    -"San Diego"
    -"Dallas"
    -"Philadelphia"
    -San Antonio" 
    -"San Jose"
    -"New York" 
    -"Los Angeles" DONE
	
4) Change the type to FOR SALE 
5) Set maximum to 1500 
6) Wait for ~ 30 mins, do not abort. 
7) Download the csv and add it to the datasets folder inside the flask folder 


Tasks:

- Add inputs for year made, home type, zip code (maybe? Would have to be a drop down option), living area  on the data_collection html 
- Create the data_visualizaition html and have it be connected to the data_collection html
- Create database to house all the datasets and create a fourth page view_data html that would be connected to data_visualization html so that users can look at the csv data for their city

*I added query parameters based on which city they clicked which you can see in the html ("?LosAngeles")
So that all our urls keep track of which city we clicked initally. This way we can use request.args on pages 3 and 4 to pull the city information and use it to subset our database  


