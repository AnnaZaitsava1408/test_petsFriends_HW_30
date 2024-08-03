import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# pytest -v --driver Chrome --driver-path /C:\chromedriver//chromedriver.exe test_petsFriends_HW_30.py

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome(executable_path='C:\chromedriver//chromedriver.exe')
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()



def test_show_all_my_pets(driver):
    '''Проверяем что мы оказались на странице "Мои питомцы"'''

    # Устанавливаем явное ожидание
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('jkjkh@gmail.com')

    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('555333111')

    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(2)

    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[text()= "Мои питомцы"]')))
    # Переход на строницу "Мои питомцы"
    driver.find_element(By.XPATH, '//a[text()= "Мои питомцы"]').click()


    # Все питомцы
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))
    all_pets = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(':')[1]

    # Количество питомцев
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//table[@class='table table-hover']/tbody/tr")))
    count_pets = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    assert int(all_pets) == len(count_pets)



def test_show_pet_friends(driver):
    '''Проверка карточек питомцев'''

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('jkjkh@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('555333111')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Переход на строницу "Мои питомцы"
    driver.find_element(By.XPATH, '//a[text()= "Мои питомцы"]').click()

    # Устанавливаем неЯвное ожидание
    driver.implicitly_wait(5)

    # Ищем все карточки питомцев на страницу "Мои питомцы"
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    # Находим внутри каждой карточки имя, фото, вид и возраст питомца
    for i in range(len(names)):

        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

def test_all_pets_have_different_names(driver):
   '''Поверяем что на странице со списком моих питомцев, у всех питомцев разные имена'''
   # Вводим email
   driver.find_element(By.ID, 'email').send_keys('jkjkh@gmail.com')
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys('555333111')
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   # Переход на строницу "Мои питомцы"
   driver.find_element(By.XPATH, '//a[text()= "Мои питомцы"]').click()

   element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))
   # Сохраняем в переменную pet_data элементы с данными о питомцах
   pet_data = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

   # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
   # и разделяем по пробелу.Выбераем имена и добавляем их в список pets_name.
   pets_name = []
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      pets_name.append(split_data_pet[0])

   # Перебираем имена и если имя повторяется то прибавляем к счетчику r единицу.
   # Проверяем, если r == 0 то повторяющихся имен нет.
   r = 0
   for i in range(len(pets_name)):
      if pets_name.count(pets_name[i]) > 1:
         r += 1
   assert r == 0
   print(r)
   print(pets_name)


def test_no_duplicate_pets(driver):
    '''Поверяем что на странице со списком моих питомцев нет повторяющихся питомцев'''
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('jkjkh@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('555333111')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Переход на строницу "Мои питомцы"
    driver.find_element(By.XPATH, '//a[text()= "Мои питомцы"]').click()

    # Устанавливаем явное ожидание
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))

    # Сохраняем в переменную pet_data элементы с данными о питомцах
    pet_data = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу.
    list_data = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)

    # Склеиваем имя, возраст и породу, получившиеся склееные слова добавляем в строку
    # и между ними вставляем пробел
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '

    # Получаем список из строки line
    list_line = line.split(' ')

    # Превращаем список в множество
    set_list_line = set(list_line)

    # Находим количество элементов списка и множества
    a = len(list_line)
    b = len(set_list_line)

    # Из количества элементов списка вычитаем количество элементов множества
    result = a - b

    # Если количество элементов == 0 значит карточки с одинаковыми данными отсутствуют
    assert result == 0

def test_photo_availability(driver):
   '''Поверяем что на странице со списком моих питомцев хотя бы у половины питомцев есть фото'''
   # Вводим email
   driver.find_element(By.ID, 'email').send_keys('jkjkh@gmail.com')
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys('555333111')
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   # Переход на строницу "Мои питомцы"
   driver.find_element(By.XPATH, '//a[text()= "Мои питомцы"]').click()

   element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))

   # Сохраняем в переменную ststistic элементы статистики
   statistic = driver.find_elements(By.XPATH, '//div[@class=".col-sm-4 left"]')

   # Сохраняем в переменную images элементы с атрибутом img
   images = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

   # Получаем количество питомцев из данных статистики
   number = statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])

   # Находим половину от количества питомцев
   half = number // 2

   # Находим количество питомцев с фотографией
   number_photos = 0
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         number_photos += 1

   # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
   assert number_photos >= half
   print(f'количество фото: {number_photos}')
   print(f'Половина от числа питомцев: {half}')