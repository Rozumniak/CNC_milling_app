import sqlite3

DB_PATH = "database/milling_data.db"  # шлях до бази даних


def get_feed_A1(material, workbench_power):
    material_map = {
        "Сталь конструкційна Т5К12В": ("Сталь", "T5K10"),
        "Сталь конструкційна Т5К10": ("Сталь", "T5K10"),
        "Сталь конструкційна P18": ("Сталь", "T15K6"),
        "Сталь конструкційна Т15К6": ("Сталь", "T15K6"),
        "Сталь конструкційна Р6М5": ("Сталь", "T15K6"),
        "Сталь конструкційна Т30К4": ("Сталь", "T15K6"),
        "Сталь конструкційна ВК8": ("Сталь", "T15K6"),

        "Сталь загартована Т15К6 HRC 35-50": ("Сталь", "T15K6"),
        "Сталь загартована Т30К4 HRC 35-50": ("Сталь", "T15K6"),
        "Сталь загартована ВК6 HRC 35-50": ("Сталь", "T15K6"),
        "Сталь загартована ВК8 HRC 35-50": ("Сталь", "T15K6"),
        "Сталь загартована ВК4 HRC 51-62": ("Сталь", "T15K6"),
        "Сталь загартована ВК6 HRC 51-62": ("Сталь", "T15K6"),
        "Сталь загартована ВК8 HRC 51-62": ("Сталь", "T15K6"),

        "Чавун ВК8 HRC 35-50": ("Чавун та мідні сплави", "BK8"),
        "Чавун ВК6 HRC 35-50": ("Чавун та мідні сплави", "BK6"),
        "Чавун ВК4 HRC 35-50": ("Чавун та мідні сплави", "BK6"),
        "Чавун ВК3 HRC 35-50": ("Чавун та мідні сплави", "BK6"),
        "Чавун Р18 HRC 51-62": ("Чавун та мідні сплави", "BK6"),
        "Чавун Р6М3 HRC 51-62": ("Чавун та мідні сплави", "BK6"),

        "Мідь або алюніній Р6М5 HRC 35-50": ("Чавун та мідні сплави", "BK6"),
        "Мідь або алюніній ВК4 HRC 35-50": ("Чавун та мідні сплави", "BK6"),
        "Мідь або алюніній ВК6 HRC 35-50": ("Чавун та мідні сплави", "BK6"),
        "Мідь або алюніній 9ХС HRC 35-50": ("Чавун та мідні сплави", "BK6"),
        "Мідь або алюніній ХВГ HRC 51-62": ("Чавун та мідні сплави", "BK6"),
        "Мідь або алюніній У12А HRC 51-62": ("Чавун та мідні сплави", "BK6"),
    }

    if material in material_map:
        material, carbide_type = material_map[material]
    else:
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
       SELECT feed_min
       FROM A1_feeds
       WHERE machine_power = ? AND material = ? AND carbide_type = ?
       """
    cursor.execute(query, (workbench_power, material, carbide_type))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None

def get_feed_A2(material, workbench_power_less, workbench_power_mid, workbench_power_more, tooth_size_large, tooth_size_small, tool_type):
    material_category_map = {
        "Сталь конструкційна Т5К12В": "Сталь",
        "Сталь конструкційна Т5К10": "Сталь",
        "Сталь конструкційна P18": "Сталь",
        "Сталь конструкційна Т15К6": "Сталь",
        "Сталь конструкційна Р6М5": "Сталь",
        "Сталь конструкційна Т30К4": "Сталь",
        "Сталь конструкційна ВК8": "Сталь",
        "Сталь загартована Т15К6 HRC 35-50": "Сталь",
        "Сталь загартована Т30К4 HRC 35-50": "Сталь",
        "Сталь загартована ВК6 HRC 35-50": "Сталь",
        "Сталь загартована ВК8 HRC 35-50": "Сталь",
        "Сталь загартована ВК4 HRC 51-62": "Сталь",
        "Сталь загартована ВК6 HRC 51-62": "Сталь",
        "Сталь загартована ВК8 HRC 51-62": "Сталь",

        "Чавун ВК8 HRC 35-50": "Чавун та мідні сплави",
        "Чавун ВК6 HRC 35-50": "Чавун та мідні сплави",
        "Чавун ВК4 HRC 35-50": "Чавун та мідні сплави",
        "Чавун ВК3 HRC 35-50": "Чавун та мідні сплави",
        "Чавун Р18 HRC 51-62": "Чавун та мідні сплави",
        "Чавун Р6М3 HRC 51-62": "Чавун та мідні сплави",

        "Мідь або алюніній Р6М5 HRC 35-50": "Чавун та мідні сплави",
        "Мідь або алюніній ВК4 HRC 35-50": "Чавун та мідні сплави",
        "Мідь або алюніній ВК6 HRC 35-50": "Чавун та мідні сплави",
        "Мідь або алюніній 9ХС HRC 35-50": "Чавун та мідні сплави",
        "Мідь або алюніній ХВГ HRC 51-62": "Чавун та мідні сплави",
        "Мідь або алюніній У12А HRC 51-62": "Чавун та мідні сплави",
    }

    if material in material_category_map:
        material = material_category_map[material]
    else:
        return None

    cutter_type_map = {
        "Торцева": "Торцеві і дискові",
        "Дискова": "Торцеві і дискові",
        "Циліндрична": "Циліндрові",
    }

    if tool_type in cutter_type_map:
        tool_type = cutter_type_map[tool_type]
    else:
        return None

    if workbench_power_less: workbench_power = "<5"
    elif workbench_power_mid: workbench_power = "5-10"
    elif workbench_power_more: workbench_power = ">10"

    if tooth_size_large: tooth_size = "Великі"
    elif tooth_size_small: tooth_size = "Дрібні"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
       SELECT feed_min
       FROM A2_feeds
       WHERE machine_power = ? AND tooth_size = ? AND cutter_type = ? AND material = ?
       """
    cursor.execute(query, (workbench_power, tooth_size, tool_type, material))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None
