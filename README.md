Here’s your updated set of instructions with details on generating and adding a Gemini API key to `app.py` before running the application:  

---

# Diet Plan & Recipe Generator Web App  
This web app generates personalized diet plans based on user preferences and health conditions. It also allows users to retrieve detailed recipes for dishes.  

## Instructions to Use  

### Step 1: Install Required Packages  
Make sure you have Python installed, then run the following commands to install the necessary packages:  
```bash  
pip install Flask  
pip install requests  
pip install flask-cors  
```  

### Step 2: Generate a Gemini API Key  
To enable the app to retrieve detailed recipes and nutritional data, you need to generate a Gemini API key:  
1. Visit the [Gemini API website](https://www.gemini.com/api).  
2. Create an account or log in.  
3. Navigate to the "API Key" section in your account settings.  
4. Generate a new API key and copy it.  

### Step 3: Add API Key to `app.py`  
1. Open the `app.py` file in a text editor.  
2. Locate the placeholder section for the API key (e.g., `GEMINI_API_KEY = "your_gemini_api_key_here"`).  
3. Replace `"your_gemini_api_key_here"` with the API key you generated. It should look like this:  
   ```python  
   GEMINI_API_KEY = "your_actual_gemini_api_key"  
   ```
4. Update GEMINI_MODEL_NAME and GEMINI_API_URL if wanted and as required.

### Step 4: Run the Application  
After adding your API key and installing the required packages, run the application with:  
```bash  
python app.py  
```  

### Step 5: Access the Website  
Open the `finalhomescreen.html` file in your browser to use the web app. You can use a Live Server (e.g., in Visual Studio Code) or simply open the file directly in any browser.  

---

## Features  
- **Diet Plan Generation**: Provides personalized meal plans for individuals as well as families based on selected health conditions and preferred cuisines.  

