import sqlite3

DB_PATH = "database/milling_data.db"  # шлях до бази даних

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
tool_type_map = {
    "Торцева": "Торцеві і дискові",
    "Дискова": "Торцеві і дискові",
    "Циліндрична": "Циліндрові фрези"
}
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
       SELECT feed_max
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
       SELECT feed_max
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

def get_feed_A3(material, tool_type, tool_diameter, tool_material):
    material_map = {
        "Сталь конструкційна Т5К12В": "Конструкційна сталь",
        "Сталь конструкційна Т5К10": "Конструкційна сталь",
        "Сталь конструкційна P18": "Конструкційна сталь",
        "Сталь конструкційна Т15К6": "Конструкційна сталь",
        "Сталь конструкційна Р6М5": "Конструкційна сталь",
        "Сталь конструкційна Т30К4": "Конструкційна сталь",
        "Сталь конструкційна ВК8": "Конструкційна сталь",
        "Сталь загартована Т15К6 HRC 35-50": "Конструкційна сталь",
        "Сталь загартована Т30К4 HRC 35-50": "Конструкційна сталь",
        "Сталь загартована ВК6 HRC 35-50": "Конструкційна сталь",
        "Сталь загартована ВК8 HRC 35-50": "Конструкційна сталь",
        "Сталь загартована ВК4 HRC 51-62": "Конструкційна сталь",
        "Сталь загартована ВК6 HRC 51-62": "Конструкційна сталь",
        "Сталь загартована ВК8 HRC 51-62": "Конструкційна сталь",

        "Чавун ВК8 HRC 35-50": "Чавун, мідні та алюмінієві сплави",
        "Чавун ВК6 HRC 35-50": "Чавун, мідні та алюмінієві сплави",
        "Чавун ВК4 HRC 35-50": "Чавун, мідні та алюмінієві сплави",
        "Чавун ВК3 HRC 35-50": "Чавун, мідні та алюмінієві сплави",
        "Чавун Р18 HRC 51-62": "Чавун, мідні та алюмінієві сплави",
        "Чавун Р6М3 HRC 51-62": "Чавун, мідні та алюмінієві сплави",

        "Мідь або алюніній Р6М5 HRC 35-50": "Чавун, мідні та алюмінієві сплави",
        "Мідь або алюніній ВК4 HRC 35-50": "Чавун, мідні та алюмінієві сплави",
        "Мідь або алюніній ВК6 HRC 35-50": "Чавун, мідні та алюмінієві сплави",
        "Мідь або алюніній 9ХС HRC 35-50": "Чавун, мідні та алюмінієві сплави",
        "Мідь або алюніній ХВГ HRC 51-62": "Чавун, мідні та алюмінієві сплави",
        "Мідь або алюніній У12А HRC 51-62": "Чавун, мідні та алюмінієві сплави",
    }
    # Мапінг матеріалу та типу фрези
    material = material_map.get(material)
    tool_type = tool_type_map.get(tool_type)

    if material is None or tool_type is None:
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if tool_type == "Торцеві і дискові":
        # Пошук без урахування діаметра
        query = """
        SELECT feed_max
        FROM A3_finishing_feeds
        WHERE cutter_type = ? AND tool_material = ?
        """
        cursor.execute(query, (tool_type, tool_material))

    elif tool_type == "Циліндрові фрези":
        try:
            diameter = float(tool_diameter)
        except ValueError:
            return None
        query = """
        SELECT feed_max
        FROM A3_finishing_feeds
        WHERE cutter_type = ?
          AND material = ?
          AND CAST(SUBSTR(diameter_range, 1, INSTR(diameter_range, '-') - 1) AS INTEGER) <= ?
          AND CAST(SUBSTR(diameter_range, INSTR(diameter_range, '-') + 1) AS INTEGER) >= ?
        """
        cursor.execute(query, (tool_type, material, diameter, diameter))

    else:
        conn.close()
        return None

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

def get_feed_A4(cutting_element, tool_diameter, depth):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT feed_max
        FROM A4_feeds
        WHERE cutter_type = ?
          AND ? BETWEEN diameter_min AND diameter_max
          AND ? BETWEEN depth_min AND depth_max
    """
    cursor.execute(query, (cutting_element, tool_diameter, depth))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

def get_feed_A5(tool_diameter):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
            SELECT feed_min, feed_max
            FROM A5_feeds
            WHERE ? BETWEEN diameter_min AND diameter_max
        """
    cursor.execute(query, (tool_diameter,))
    result = cursor.fetchone()
    conn.close()

    return result if result else None

def get_cutting_speeds_A6(material, material_strength, tool_type, tool_subtype, tool_material, milling_width, depth, feed):
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

        "Чавун ВК8 HRC 35-50": "Чавун",
        "Чавун ВК6 HRC 35-50": "Чавун",
        "Чавун ВК4 HRC 35-50": "Чавун",
        "Чавун ВК3 HRC 35-50": "Чавун",
        "Чавун Р18 HRC 51-62": "Чавун",
        "Чавун Р6М3 HRC 51-62": "Чавун",
    }

    if material in material_category_map:
        material = material_category_map[material]
    else:
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if (material == "Сталь"):
        if (tool_subtype == "Зі вставними ножами"):
            tool_type = "Дискова зі вставними ножами"
        elif (tool_subtype == "З коронками"):
            tool_type = "Кінцева з коронками"
        elif (tool_subtype == "З напаяними пластинами"):
            tool_type = "Кінцева з напаяними пластинами"

        query = """
                   SELECT Cv, q, x, y, u, p, m
                   FROM A6_cutting_speeds
                   WHERE material_type = ? AND cutter_type = ? AND tool_material = ?
               """
        cursor.execute(query, (material, tool_type, tool_material, ))
        result = cursor.fetchone()
        conn.close()

    elif(material == "Чавун" and material_strength < 1500):
        query = """
                           SELECT Cv, q, x, y, u, p, m
                           FROM A6_cutting_speeds
                           WHERE material_type = ? AND hardness = ? AND cutter_type = ? AND tool_material = ?
                       """
        cursor.execute(query, (material, "HB<1500", tool_type, tool_material,))
        result = cursor.fetchone()
        conn.close()

    elif (material == "Чавун" and material_strength > 1500):
        query = """
                               SELECT Cv, q, x, y, u, p, m
                               FROM A6_cutting_speeds
                               WHERE material_type = ? AND hardness = ? AND cutter_type = ? AND tool_material = ?
                           """
        cursor.execute(query, (material, "HB>1500", tool_type, tool_material,))

        result = cursor.fetchone()
        conn.close()

    return result if result else None

def get_tool_life_A8(tool_type, tool_diameter):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
                           SELECT life_minutes
                           FROM tool_life
                           WHERE tool_type = ? AND ? BETWEEN diameter_min AND diameter_max
                       """
    cursor.execute(query, (tool_type, tool_diameter,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_Knv(surface_state):
    if (surface_state == "Без кірки"):
        surface_condition = "Без кірки"
        material = "Прокат"
    elif (surface_state == "Прокат з кіркою"):
        surface_condition = "З кіркою"
        material = "Прокат"
    elif (surface_state == "Поковка з кіркою"):
        surface_condition = "З кіркою"
        material = "Поковка"
    elif (surface_state == "Мідні та алюмінієві сплави з кіркою"):
        surface_condition = "З кіркою"
        material = "Мідні й алюмінієві сплави"
    elif (surface_state == "Сталеві та чавунні відливання з нормальною кіркою"):
        surface_condition = "З кіркою"
        material = "Сталь чавун відливання (нормальний стан)"
    elif (surface_state == "Сталеві та чавунні відливання з забрудненою кіркою"):
        surface_condition = "З кіркою"
        material = "Сталь чавун відливання (забруднений стан)"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
            SELECT Ksh_max
            FROM A10_surface_correction
            WHERE surface_condition = ? AND material = ?              
            """
    cursor.execute(query, (surface_condition, material,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_Kuv(material):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
            SELECT coeff
            FROM tool_material_coeffs
            WHERE material = ?              
            """
    cursor.execute(query, (material,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None