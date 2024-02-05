from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

df = pd.DataFrame({
    "Title": [],
    "OriginalName": [],
    "Sinopse": [],
    "Gender": [],
    "StreamOptions": [],
    "Temporadas": [],
    "ImageName": []
})


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install()) #instala versão atual do chrome drive
driver = webdriver.Chrome(service=service, options=chrome_options) #cria uma instancia do navegador

url = r"file:///C:/Users/ferna/Downloads/Justwatch/Netflix/Netflix%20Brasil%20-%20melhores%20filmes%20e%20s%C3%A9ries%20online%20do%20JustWatch.html"

driver.get(url)

# Endereço de cada item
xpath = """//*[@id="base"]/div[3]/div/div[1]/div/div[1]/div/div[$]/a"""

name = []
streamList = []
sinopseList = []
genderList = []
contentType = []
contentTypeList = []
originalName = []
originalNamesList = []
imageFileList = []
urlList = []


# Função que verifica se tem título original e adiciona à lista
def getOriginalName(verificaOriginal):
    if verificaOriginal is not None:
        try:
            originalName = driver.find_element(By. XPATH, """//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/h3""")
            return originalName.text.replace("Título Original: ", "")
        except:
            return None

# Função que verifica se é filme ou serie e mostra quantas temporadas tema serie
def getTemporada(verificaSerie):
    if verificaSerie is not None:
        try:
            temporadas = driver.find_element(By. CLASS_NAME, "subheading")
            return temporadas.text
        except:
            return ("Filme")
        
# Remove as quebras de linha da sinopseList e evita erros no json
def remove_newlines(sinopseList):
    for i in range(len(sinopseList)):
        sinopseList[i] = sinopseList[i].strip("\n")
    return sinopseList

# Clica em cada pagina e extrai os dados
current_value = 1905
loop_number = 0

for i in range(1905, 1960):
    try:
        new_xpath = xpath.replace("div[$]", f"div[{current_value}]")

        # Usa o novo XPath para encontrar o elemento
        element = WebDriverWait(driver, 12).until(
            EC.element_to_be_clickable((By.XPATH, new_xpath))
        ) 
        element.click()
        print("step_1")
        current_value += 1
        loop_number = current_value
        findTitle = driver.find_element(By.TAG_NAME, value="h1")
        title = findTitle.text
        name.append(title)
        print("step_2")
        # Função que verifica se é filme ou serie e mostra quantas temporadas tema serie
        verificaOriginal = driver.find_element(By.CLASS_NAME, "title-block__container")
        
        if verificaOriginal is not None and verificaOriginal.is_displayed():
            
            nomeOriginal = getOriginalName(verificaOriginal)

            unique_original_names = set()
            if nomeOriginal is not None:
                unique_original_names.add(nomeOriginal)
                originalName = unique_original_names.pop()
            else:
                unique_original_names.add("Não tem")               
        else:
            originalName = "Não tem"
        
        originalNamesList.append(originalName)    
        print("step_3")
        # Gera a lista de streaming disponivel

        streams = driver.find_elements(By.CSS_SELECTOR, "div.buybox-row__offers a img.offer__icon")

        streamOptions = []
        print("step_4")
            # Extrai o "alt" da imagem e salva como texto em uma lista
        unique_alt_texts = set()  # usa o set para converter em um unico objeto sem repetição
        for stream in streams:
            alt_text = stream.get_attribute("alt")
            unique_alt_texts.add(alt_text)
        streamOptions = list(unique_alt_texts)  # coverte novamente em lista
        
        streamList.append(streamOptions)
        print("step_5")
        # Localiza a sinopse e adiciona em uma lista
        try:
            sinopse = driver.find_element(By.CSS_SELECTOR, "div[data-v-1a296691]").text.replace('SINOPSE', '').replace('"',"'")
            
        except:
            sinopse = driver.find_element(By.CSS_SELECTOR, "div[data-v-7fe7d05a]").text.replace('SINOPSE', '').replace('"',"'")
            

        if sinopse is not None:
            sinopseList.append(sinopse)
        else:
            sinopseList.append("Não tem")
        print("step_6")
        # Localiza os generos e adiciona em uma lista
        genders = driver.find_element(By. XPATH, """//*[@id="base"]/div[2]/div/div[1]/div/aside/div[1]/div[3]/div[3]/div""").get_attribute("innerHTML").replace("&amp;", "&").split(",")
        genderList.append(genders)
        print("step_7")
        # Verifica se é filme ou serie e mostra quantas temporadas tema serie
        
        verificaSerie = driver.find_element(By. CLASS_NAME, "jw-info-box__container-content")
        temporada = getTemporada(verificaSerie)
        
        unique_content_types = set()
        if temporada is not None:
            unique_content_types.add(temporada)
        else:
            unique_content_types.add("Filme")
        
        contentType = unique_content_types.pop()

        contentTypeList.append(contentType)
        print("step_8")
        
        # Cria uma lista com o nome do arquivo da imagem de capa
        try:
            imageLink = driver.find_element(By. XPATH, """//*[@id="base"]/div[2]/div/div[1]/div/aside/div[1]/div[1]/picture/source[1]""").get_attribute("data-srcset")
            imageName = imageLink.rsplit("/", 1)
            imageFileList.append(imageName[-1])
            print("step_9")
        except NoSuchElementException:
            imageName = "Não tem"
            imageFileList.append(imageName)

        driver.implicitly_wait(1)
        print("step_10")
        sinopseList = remove_newlines(sinopseList)
        print("step_11")

        # Cria uma lista com a url

        urlContent = driver.current_url
        urlList.append(urlContent)

    except NoSuchElementException:  # Exceção se o elemento não for encontrado
        print(current_value)
        break  # Termina o loop quando não houver mais itens
        

    # Retorna no terminal as listas

    print(current_value, title, originalName, sinopse, genders, streamOptions, temporada, imageName[-1], urlContent)

    driver.back()

driver.quit()

print(name)
print(originalNamesList)
print(sinopseList)
print(genderList)
print(streamList)
print(contentTypeList)
print(imageFileList)
print(urlList)



# Cria o dataframe do pandas e gera o csv e json
df = pd.DataFrame(data=[name, originalNamesList, sinopseList, genderList, streamList, contentTypeList, imageFileList, urlList], index=["Title", "OriginalName", "Sinopse", "Gender", "StreamOptions", "Temporadas", "ImageName", "URL"],)
df = df.transpose()
df.to_json("dataFrame23.json")
df.to_csv("dataFrame23.csv")
