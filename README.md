# RecipeMakerWebApp
- Dominic Barrera (@bdom26)
- Frances Belleza (@francesbelleza)

## Video Link To Our Project
**we used canva for our video**
[canva video](https://www.canva.com/design/DAGnTqoB424/fbBEOV3IIsvRNi6HXebdPA/watch?utm_content=DAGnTqoB424&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h33d1a31042)

## How to Run this Program <Dom>
### 1. Make sure you have the following prerequisites
- Python3.8+ installed on your machine/laptop/computer
- Git
- terminal: linux, command Line, etc. <br/>  
**Note: The syntax underneath each bullet point below must be copied & 
pasted into your terminal.**

### 2. Clone the repository
  - open your terminal
  - clone this repo:
     ```
     git clone https://github.com/francesbelleza/recipeMakerWebApp.git
  - move into the directory of this project:
      ```
      cd recipeMakerWebApp

### 3. Create & activate a virtual environment
  -  make a new virtual environment folder:
      ```
      python3 -m venv venv
  - activate your virtual environment:
     ```
     source venv/bin/active
  - you should now see (venv) in front of your prompt, please refer to the picture below: <br/>  
    ![](/images/prompt.png "venv prompt example")

### 3. Install all dependencies
   - install necessary dependencies:
     ```
     pip install -r requirements.txt

### 4. Check configurations
- make sure config.py & app.db is in your root folder

### 5. Run the app
- run the application using _either_ of the two commands:
    ```
    flask run
- OR
    ```
    python3 run.py
- then type the following url into your browser of choice:
    ```
    http://127.0.0.1:5000/

### 6. Navigate the application
- navigate the application
- to exit simply exit the web browser or in your terminal press ``control`` and 
the letter ``c`` at the same time


## Requirements Implemented
- user registration (implemented by Frances)
- user login (implemented by Frances)
- user logout (implemented by Frances)
- create recipe (implemented by Frances)
- Edit recipe (implemented by Dominic)
- View recipe (implemented by Dominic)
- Delete recipe (implemented by Dominic)
- search recipe (implemented by Frances)
- rate recipe (implemented by Frances)
- comment (implemented by Frances)
- view user profile (implemented by Frances)

## Ethical Implications <Frances>
In building this web application from an engineer’s perspective, 
we have a few key ethical and professional responsibilities to address. 
First, data privacy: users entrust us with personal details (names, emails) 
and their in-app activity. It’s important to clearly explain what we collect, 
why we collect it, and whether any third parties might access that information. 
Being upfront about data sharing builds trust and helps users feel secure. Secondly, 
professional responsibility means writing clean, maintainable code and keeping documentation 
current. That way, anyone joining the project can quickly understand its structure and contribute 
without confusion or frustration.
<br/>
<br/>
Engineering decisions can be visible through society in both obvious and subtle ways. 
Take social media as an example: it can foster creativity and community, yet studies from Yale 
Medicine note that overstimulating the brain’s reward centers can mirror addiction pathways. 
That dual nature reminds us to think through potential downsides when designing new features. 
<br/>
<br/>
Finally, engineering solutions extend far beyond lines of code; they shape economies, environments, 
and societies in both big and small ways. A well-built feature can streamline everyday tasks, create 
new business opportunities, or connect people across continents, but it can also centralize/overuse 
resources, widen inequalities, or create unintended environmental strain. That means when we design our
app’s functionality, from data storage to recommendation engines, we should be mindful of who benefits, 
who might be left out, and how can we minimize waste. 
<br/>
<br/>
*citation:* <br/>
Katella, K. (2024, June 17). How social media affects your teen’s mental health: A parent’s guide. Yale Medicine. 
https://www.yalemedicine.org/news/social-media-teen-mental-health-a-parents-guide
