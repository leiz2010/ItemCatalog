## Full Stack Nanodegree project 3

11-08-2015  
Lei Zhang

### Project description:
This project is a basic CURD application for a restaurant menu implemented with python Flask framework, and with base code provided by Uacity. In the project the use can view all the menu items for the fictional Yatta Teriyaki resturant at the root page without logging in.  If the user logs in with Facebook or GooglePlus account, the user will be able to delete, edit, and create new menu item for the restaurant.

## To run the project:
1. Install Vagrant and VirtualBox.
2. Launch Vagrant VM in git bash then login.
3. Navigate to catalog directory.
4. Enter python database_setup.py then hit enter.
5. Enter python dummydata.py to create menuwithusers DATABASE with dummy data.
6. Enter python finalProject.py then hit enter.
7. Launch web browser then visit http://localhost:5000 to see Yatta Teriyaki menu page.
8. Click on login to launch the login page with Facebook or GooglePlus.
9. Login with a Facebook or GooglePlus accont.
10. After login the user can edit, delete, or create new item.

### Extra Feature:
XML API endpoint:   
http://localhost:5000/menu/XML  
Open the web browser's console before visiting the link above to see the XML formated data.

##### Instructions for installing Vagrant and VirtualBox:
https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true

#### References:
http://stackoverflow.com/   
http://www.w3schools.com/html/  
https://developers.facebook.com/    
http://www.tutorialrepublic.com/twitter-bootstrap-tutorial/bootstrap-grid-system.php
