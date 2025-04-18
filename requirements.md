## Functional Requirements
1. **User Registration:** Allows use to create an account by giving a username, password, and email.
2. **User Login:** Users may able to log in using their registered account.
3. **User Logout:** Users can log out of their account safely.
4. **Create Recipe:** Users may able to create recipes by giving a title, description, and instructions. 
5. **Edit Recipe:** Users may update an existing recipe.
6. **Delete Recipe:** Users may delete their own recipes.
7. **View Recipe:** Everyone may able to see the details of the recipe such as the ingredients and instructions. 
8. **Search Recipe:** Users may search recipes by title or ingredients.
9. **Rate:** Users may give 1-5 stars of a recipe. 
10. **Comment:** Users may able to leave a comment to a recipe. 
11. **View User Profile:** Users can see their own profile and their recipes. 
12. **Edit User Profile:** Users may change their display name, email, and password. 
13. **Save Recipe:** Users may save recipes for a quick access. 
14. **View All Recipes:** Main recipe lists shows all recipes available in the database. 
15. **Filter Recipes:** Users may filter recipes by tags such as 'vegan', 'dessert', etc.

## Non-functional Requirements
1. The program runs on web browsers (Chrome, Safari, etc.)
2. The program implements SQLAlchemy for data scalability.

## User Registration <Dom>
- **Pre-condition:** User is not signed in and does not have an account. 
- **Trigger:** User clicks "Sign up" button on the homepage.
- **Primary Sequence:** 
   1. User access registration page.
   2. User fills out registration page with username, email, and password.
   3. User submits the form.
   4. System validates the data.  
   5. System creates the new username.
   6. System logs the user in and redirects to the homepage.
- **Primary Post-conditions:** User account is now stored in the database. User can now log in.
- **Alternate Sequence:** 
   1. If system cannot validate the data, there will be an error message "Something went wrong. Please try again".
## User login <Dom>
- **Pre-condition:** User must have a valid username and password and must be signed out. 
- **Trigger:** User clicks "log in" button after inputting username and password.
- **Primary Sequence:**
   1. User enters username and password.
   2. User clicks "log in" button.
   3. System validates data.
   4. User gets redirected to homepage.
- **Primary Post-conditions:** User is now authorized and now logged in. 
- **Alternate Sequence:**
   1. User cannot log in.
   2. System will prompt a message "Unable to log in. Please try again".
## User logout <Dom>
- **Pre-condition:** User must be logged in. 
- **Trigger:** User clicks "Log out" button.
- **Primary Sequence:**
   1. User clicks "log out" button.
   2. System ends the session.
   3. User gets redirected to log in page.
- **Primary Post-conditions:** User is logged out and system is clear.
- **Alternate Sequence:**
   1. User fails to log out.
   2. System promps a message "Unable to sign out. Please Try again".
## Create recipe <Dom> 
- **Pre-condition:** User is logged in.
- **Trigger:** User clicks "Create new recipe" button. 
- **Primary Sequence:**
   1. User fills out the recipe creation form with title, description, ingredients, and instruction.
   2. User submits the form.
   3. System verifies the data.
   4. Recipe is now saved to the database belonging to the user.
   5. User gets redirected to the recipe view page. 
- **Primary Post-conditions:** created recipe gets saved to the database and can be seen through recipe view page.
- **Alternate Sequence:**
   1. Cannot create a new recipe. 
   2. System promps a message "Something went wrong, please try again"
## Edit Recipe <Dom>
- **Pre-condition:** User must be logged in and have an existing recipe.
- **Trigger:** User clicks "Edit recipe" button. 
- **Primary Sequence:**
   1. User edits recipe.
   2. User submits the form.
   3. System verifies the data and updates the database. 
   4. User gets redirected to the recipe view page. 
- **Primary Post-conditions:** Recipe is edited and updated through the database and can be seen through the recipe view page. 
- **Alternate Sequence:**
   1. There was no recipe to be found. 
   2. System prompts a message "No recipe to edit".
## Delete Recipe <Dom>
- **Pre-condition:** There must be an existing recipe. 
- **Trigger:** User clicks "delete recipe"
- **Primary Sequence:**
   1. System promps a message "Are you sure you want to delete this?"
   2. User confirms.
   3. System verifies the data. 
   4. System deletes the recipe from the database. 
   5. User is redirected to the recipe view page. 
- **Primary Post-conditions:** Recipe is deleted from the database. 
- **Alternate Sequence:**
   1. User cancels the action.
   2. Recipe does not get deleted. 
## View Recipe <Dom>
- **Pre-condition:** There must be an existing recipe. 
- **Trigger:** User clicks the recipe from searching or directly. 
- **Primary Sequence:**
   1. User searches for recipe from the recipe view page. 
   2. System gathers recipe data. 
   3. Recipe is then shown along with the details. 
- **Primary Post-conditions:** Recipe is shown to the user.
- **Alternate Sequence:**
   1. Recipe is not found
   2. System prompts a message "Recipe cannot be found".
## Search Recipe<Dom>
- **Pre-condition:** There must be an existing recipe. 
- **Trigger:** User types a title or ingredient in the search bar. 
- **Primary Sequence:**
   1. System recieves the request. 
   2. System finds the recipe from the database. 
   3. User recieves the matching result. 
- **Primary Post-conditions:** Related results are shown to the user. 
- **Alternate Sequence:**
   1. System cannot find the recipe. 
   2. System prompts a message "Recipe cannot be found"


## Rate <Frances>
- **Pre-condition:** Users must be logged into their accounts in order to 
access this.
- **Trigger:** Users click on the "rate" button found on specific recipe's page.
- **Primary Sequence:**
  1. User clicks on the "rate" button found on the recipe's page.
  2. User is redirected by system to a different page, rating form page.
  3. User enters rating of recipe.
  4. User submits rating.
  5. The system saves the rating into the database.
- **Primary Post-conditions:** When the user completes their rating they're redirected
to the original recipe they were looking at. The rating of specific recipe updates.
- **Alternate Sequence:** 
  1. User is not logged into their account.
  2. The system will prompt that they're not logged in.
  3. The system will have a button to login.

## Comment <Frances>
- **Pre-condition:** Users must be logged onto their accounts to use
this feature.
- **Trigger:** They press the comment button underneath the comment text box.
- **Primary Sequence:**
  1. User scrolls down to the "comments" section, specifically to the text box 
  underneath all the comments.
  2. User types in a comment.
  3. User presses the "comment" button.
  4. The system saves the comment into the database.
- **Primary Post-conditions:** The comment is now visible under the "comments" section.
The comments at the top are most recent.
- **Alternate Sequence:** 
  1. User is not logged into their account.
  2. The system will redirect user to an error page "You are not logged in."
  3. In the page will be a button "log in"

## View User Profile <Frances>
- **Pre-condition:** Users must be logged into their accounts in order
to access this feature.
- **Trigger:** User clicks the "view profile" button.
- **Primary Sequence:**
  1. User clicks the "view profile" button.
  2. System redirects user to their profile.
  3. User is able to see their profile information.
  4. User can click the toggle button "submitted recipes" to view their submitted recipes.
- **Primary Post-conditions:** User is able to view their profile.
- **Alternate Sequence:** 
  1. The system is unable to load their information.
  2. System prompts user to refresh the page.

## Edit User Profile <Frances>
- **Pre-condition:** User must be logged into their account to access this feature.
- **Trigger:** User clicks 
- **Primary Sequence:**
  1. User clicks "view profile" button.
  2. System redirects user to their profile.
  3. Users click the "edit profile" button underneath their information.
  4. The system redirects users to an editable form where their information
     (display name, password, email) exists.
  5. User changes any information they'd like.
  6. User presses the "save" button.
- **Primary Post-conditions:** The system redirects user to a "successfully saved" page, 
and also redirects them to their profile.
- **Alternate Sequence:** 
  1. The system was unable to save their changed information.
  2. System prompts them to refresh the page and start the edit process again.

## Save Recipe (Favorite) <Frances>
- **Pre-condition:** User must be logged into their accounts and viewing a specific recipe.
- **Trigger:** User clicks the heart icon at a specific recipe.
- **Primary Sequence:**
  1. User finds a recipe they like; they're viewing that recipe on its specific page.
  2. User clicks the heart icon located next to the recipes name.
  3. The system will show a pop-up with the question, "Would you like to save this to your
  favorites list?"
  4. User will respond yes to save and no to cancel.
- **Primary Post-conditions:** If user clicks yes, the system will respond with a success page: "recipe added to your favorites list."
- **Alternate Sequence:** 
  1. System was unable to save recipe to user's favorites list.
  2. The system will prompt the user to refresh and try again.

## View All Recipes <Frances>
- **Pre-condition:** User must be signed in to their account to access this functionality.
- **Trigger:** User clicks homepage.
- **Primary Sequence:**
  1. User clicks the "homepage" button.
  2. System redirects user to the homepage page.
  3. System shows all recipes available in the database.
- **Primary Post-conditions:** User is able to view all recipes.
- **Alternate Sequence:**
  1. Database is not loading on the homepage.
  2. System prompts an error page, "please refresh."

## Filter Recipes <Frances>
- **Pre-condition:** User must be signed in to their accounts and in the view all recipes page
to access this functionality.
- **Trigger:** User clicks the filter button while viewing all recipes.
- **Primary Sequence:**
  1. User clicks the "homepage" button.
  2. User is viewing all recipes and clicks on the filter button.
  3. User clicks specific tags.
  4. System pulls the recipes connected to those specific tags.
- **Primary Post-conditions:** User is able to view tagged specific recipes.
- **Alternate Sequence:**
  1. User clicks a specific tag.
  2. Recipes tagged with specific tag won't show up.
  3. System prompts an error page, "please refresh."
