import re
from ast import Await

import requests
from aiogram import types
from bs4 import BeautifulSoup

from main import bot


def get_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


class Information:
    # Парсинг 10 перших фото
    def get_photo(soup: BeautifulSoup, a_lot_of: bool) -> list | types.URLInputFile:
        photo = soup.find("div", class_="swiper-wrapper").find_all("img")

        list_src_photo = []
        media_group = []

        for src in photo:
            list_src_photo.append(src.get("src"))

        if len(list_src_photo) > 10:
            del list_src_photo[10:]

        for photo_url in list_src_photo:
            media_group.append(types.InputMediaPhoto(media=photo_url))

        first_photo = types.URLInputFile(str(list_src_photo[0]))

        if not a_lot_of:
            return first_photo

        return media_group

    # Парсинг головної інформації (к-ть кімнат, поверх, площа, Район)
    def get_main_information(soup: BeautifulSoup) -> [str, str, str, str]:
        # constants to check the list "tags"
        need_words_ukrainian = [
            "Кількість кімнат:",
            "Загальна площа:",
            "Поверх:",
            "Поверховість:",
        ]
        need_words_russian = [
            "Количество комнат:",
            "Общая площадь:",
            "Этаж:",
            "Этажность:",
        ]

        checklist = []
        tags = soup.find("ul", class_="css-sfcl1s").find_all("p")

        for need_word in need_words_russian:
            for tag in tags:
                if need_word in tag.text:
                    checklist.append(tag.text)

        for need_word in need_words_ukrainian:
            for tag in tags:
                if need_word in tag.text:
                    checklist.append(tag.text)

        try:
            if len(checklist) != 4:
                rooms = re.search(r"\d+", checklist[0]).group()
                area = re.search(r"\d+", checklist[1]).group()
                find_everything = re.search(r"\d+", checklist[2])
                flour = f"{find_everything.group()}"
            else:
                rooms = re.search(r"\d+", checklist[0]).group()
                area = re.search(r"\d+", checklist[1]).group()
                find_have = re.search(r"\d+", checklist[2])
                find_everything = re.search(r"\d+", checklist[3])
                flour = f"{find_have.group()} з {find_everything.group()}"
        except:
            rooms, area, flour = "", "", ""

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        # we are looking for a district and a city, because
        # if there is no district, then the city is a district

        find = soup.find_all("script")
        pattern_district = re.compile(r'\\"districtName\\":\\"([^\\"]+)\\"')
        pattern_city = re.compile(r'\\"cityName\\":\\"([^\\"]+)\\"')

        for one in find:
            district = pattern_district.search(one.text)
            if district:
                break

        for one in find:
            city = pattern_city.search(one.text)
            if city:
                break

        if district:
            district = district.group(1)
        elif city:
            district = city.group(1)
        else:
            district = ""

        return rooms, flour, area, district

    def get_price(soup: BeautifulSoup) -> [str, str]:
        # parsing price from the page
        price = soup.find("h2", text=re.compile(r".*грн.*"))

        if not price:
            price = soup.find("h2", text=re.compile(r".*\$.*"))

        if not price:
            price = soup.find("h3", text=re.compile(r".*грн.*"))

        if not price:
            price = soup.find("h3", text=re.compile(r".*\$.*"))

        if not price:
            price = soup.find("h4", text=re.compile(r".*грн.*"))

        if not price:
            price = soup.find("h4", text=re.compile(r".*\$.*"))

        if not price:
            return "Суму не знайдено"

        return price.text

    def delete_words(text: str, words_to_remove: list) -> str:
        # Використовуємо регулярний вираз для визначення слова з можливими крапками
        pattern = re.compile(
            r"\b(?:" + "|".join(map(re.escape, words_to_remove)) + r")\b", re.IGNORECASE
        )

        # Замінюємо відповідні слова на порожні рядки
        result = pattern.sub("", text)

        return result

    def get_header(soup: BeautifulSoup) -> [str, str]:
        # parsing caption from the page
        header = soup.find("h4", class_="css-1juynto")

        if not header:
            return None

        return header.text

    def get_caption(soup: BeautifulSoup) -> str:
        # parsing caption from the page
        caption = soup.find("div", class_="css-1t507yq er34gjf0")

        if not caption:
            return "Описание не найдено"

        if len(caption.text) > 800:
            return caption.text[0:800]

        return caption.text

    def create_caption(soup: BeautifulSoup) -> str:
        words = [
            "Від",
            "От",
            "я собственник",
            "я власнник",
            "посредников",
            "своя",
            "свою",
            "риелтор",
            "риелторов",
            "агентство",
            "агент",
            "маклер",
            "посредник",
            "личную",
            "хозяин",
            "собственник",
            "собственника",
            "хозяина",
            "хозяйка",
            "без комиссии",
            "агента",
            "агентства",
            "собственников",
            "посередників",
            "своя",
            "свою",
            "ріелтор",
            "ріелторів",
            "агентство",
            "агент",
            "маклер",
            "посередник",
            "посередник",
            "особисту",
            "власник",
            "власника",
            "власників",
            "хазяїнахазяйка",
            "хазяйка",
            "особисту",
            "без комісії",
            "Без рієлторів",
            "комісій",
            "Без риелторов",
            "комисий",
            "комісіЇ",
            "комисии",
        ]

        caption = Information.delete_words(Information.get_caption(soup), words)
        header = Information.delete_words(Information.get_header(soup), words)

        rooms, flour, area, district = Information.get_main_information(soup)
        money = Information.get_price(soup)

        captions = (
            f"🏡{rooms}к кв\n" f"🏢Поверх: {flour}\n" f"🔑Площа: {area}м2\n" f"📍Район: {district}\n"
        )

        main_caption = f"💳️{money}" f"\n\n{header}\n\n" f"📝Опис:\n{caption}"
        if not rooms != "":
            return main_caption
        return captions + main_caption


# Отримання всіх даних і запуск надсилання
async def get_data(message: types.Message):
    soup: BeautifulSoup = get_url(message.text)
    photo_group = Information.get_photo(soup, True)
    caption = Information.create_caption(soup)

    message_photo = await message.answer_media_group(media=photo_group)
    await bot.edit_message_caption(
        message_id=message_photo[0].message_id,
        chat_id=message.chat.id,
        caption=caption,
        parse_mode="HTML",
    )
