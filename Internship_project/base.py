from selenium import webdriver
from  selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverMnager
from selenium.webdriver import ChromeOptions
from flask import Flask, render_template, request
from selenium.webdriver.chrome.service import Service
import time
import re
import pytesseract
from PIL import Image

app = Flask(__name__,template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods = ['Get','POST'])
def run_automation():
    if request.method == 'POST' :
        search_key = request.form.get('search_key')
        results= selenium_code(search_key)
        if(results=="Element Not Found"):
             return render_template('index.html',error=f"There was a Error while fetching captcha please 'Restart'")
        return render_template('result.html',results=results)
       

def selenium_code(search_key):
        # s = Service(chromeDriverManager().install())
        chrome_binary_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# Initialize the Chrome webdriver with the path to the Chrome binary using a Service object
        options = ChromeOptions()
        # options.add_argument('headless')
        options.binary_location = chrome_binary_path
        driver = webdriver.Chrome(options=options)
        driver.get("https://vahan.parivahan.gov.in/nrservices/faces/user/citizen/citizenlogin.xhtml")  




        input_field = driver.find_element("name", "TfMOBILENO")
        input_field.send_keys("@username") # ENTER YOUR USERNAME DETAILS


# In[5]:


        driver.find_element("id", "btRtoLogin").click()


# In[6]:


        password_field = driver.find_element("name", "tfPASSWORD")
        password_field.send_keys("@PASSWORD") #ENTER YOUR PASSWORD


# In[7]:


        driver.find_element("id", "btRtoLogin").click()



       
        driver.find_element("name","regn_no1_exact").send_keys(search_key)








        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
  
  
 
  
  
  
        def read_captcha():
         element = driver.find_element("id","vahancaptcha:ref_captcha")
         scrrenshot = element.screenshot_as_png
         with open('canvas.png', 'wb') as f:
               f.write(scrrenshot)

         im = Image.open("canvas.png")
         im = im.convert("P")
         im2 = Image.new("L",im.size,255)
         im = im.convert("P")
         temp = {}
         for x in range(im.size[1]):
               for y in range(im.size[0]):
                   pix = im.getpixel((y,x))
                   temp[pix] = pix
                   if pix == 1: 
                       ph =im2.putpixel((y,x),0)
         im2.save("output.png")
         image = Image.open("output.png")
           # Convert the image to grayscale
         image = image.convert("L")
           # Use pytesseract to extract the text from the image
         captcha_text = pytesseract.image_to_string(image)
         my_captcha = re.sub(r'\W+', '', captcha_text)
         return my_captcha

  
        
            #    from selenium.webdriver.common.by import By
        while(1):
            time.sleep(5)
            my_captcha = read_captcha()
            # my_captcha
            if my_captcha == '':
                driver.find_element("id", "vahancaptcha:btn_Captchaid").click()
            else:
                driver.find_element("name","vahancaptcha:CaptchaID").send_keys(my_captcha)
                try:
                    submit_but =   driver.find_element(By.XPATH, "/html/body/form/div/div[3]/div/div[2]/div/div[1]/div[2]/div[1]/div[5]/div/button").click()
                    break
                except:
                    driver.find_element("id", "vahancaptcha:btn_Captchaid").click()

        time.sleep(5)
        try:
            driver.find_element(By.XPATH,"/html/body/form/div/div[3]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[4]/td/div/span[2]")
            
        except:
            return "Element Not Found"
            

                    
       
        vehicle =   driver.find_element(By.XPATH, '/html/body/form/div/div[3]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[4]/td/div/span[2]')
        vno =   driver.find_element(By.XPATH, '/html/body/form/div/div[3]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[1]/td[1]/div')
        reg_date =   driver.find_element(By.XPATH, '/html/body/form/div/div[3]/div[3]/div[1]/div/div/div/div[2]/div[4]')
        bike_model =   driver.find_element(By.XPATH, '/html/body/form/div/div[3]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[3]/td[1]/div')
        reg_loc =   driver.find_element(By.XPATH, '/html/body/form/div/div[3]/div[3]/div[1]/div/div/div/div[1]/table/tbody/tr[4]/td/div/span[3]')
        
        return {'name':vno.text,'name1':vehicle.text,'name2':bike_model.text,'name3':reg_loc.text,'name4':reg_date.text}
         

        # print("vechiaa number name ",vehicle.text)

  

if __name__ == '__main__':
    app.run(debug=True)






# %%
