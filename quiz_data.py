# Данные викторины "Тотемное животное Московского зоопарка"

QUESTIONS = [
    {
        "id": 1,
        "text": "🗺️ Где вы предпочитаете проводить свободное время?",
        "options": [
            {"text": "В тихом лесу, подальше от людей",
             "points": {"manul": 3, "polar_bear": 0, "penguin": 1, "flamingo": 0, "lynx": 2}},
            {"text": "На вечеринке в центре города",
             "points": {"manul": 0, "polar_bear": 1, "penguin": 3, "flamingo": 2, "lynx": 0}},
            {"text": "У воды — реки, озера или моря",
             "points": {"manul": 0, "polar_bear": 2, "penguin": 3, "flamingo": 1, "lynx": 0}},
            {"text": "Дома под пледом с книгой",
             "points": {"manul": 2, "polar_bear": 0, "penguin": 0, "flamingo": 1, "lynx": 3}},
        ]
    },
    {
        "id": 2,
        "text": "🍣 Ваша любимая еда — это...",
        "options": [
            {"text": "Свежая рыба!", "points": {"manul": 0, "polar_bear": 3, "penguin": 3, "flamingo": 0, "lynx": 1}},
            {"text": "Фрукты и ягоды", "points": {"manul": 1, "polar_bear": 1, "penguin": 0, "flamingo": 2, "lynx": 0}},
            {"text": "Мясо, и только мясо",
             "points": {"manul": 3, "polar_bear": 2, "penguin": 0, "flamingo": 0, "lynx": 3}},
            {"text": "Что угодно, я не привередлив(а)",
             "points": {"manul": 1, "polar_bear": 0, "penguin": 1, "flamingo": 3, "lynx": 1}},
        ]
    },
    {
        "id": 3,
        "text": "🎭 Какой стиль жизни вам ближе?",
        "options": [
            {"text": "Активный и шумный",
             "points": {"manul": 0, "polar_bear": 1, "penguin": 3, "flamingo": 2, "lynx": 1}},
            {"text": "Спокойный и размеренный",
             "points": {"manul": 3, "polar_bear": 0, "penguin": 0, "flamingo": 2, "lynx": 1}},
            {"text": "Одиночество — моё всё",
             "points": {"manul": 3, "polar_bear": 2, "penguin": 0, "flamingo": 0, "lynx": 2}},
            {"text": "Люблю компанию, но по делу",
             "points": {"manul": 1, "polar_bear": 1, "penguin": 1, "flamingo": 3, "lynx": 2}},
        ]
    },
    {
        "id": 4,
        "text": "❄️ Что вы думаете о холодной погоде?",
        "options": [
            {"text": "Обожаю! Мороз и солнце — день чудесный!",
             "points": {"manul": 1, "polar_bear": 3, "penguin": 3, "flamingo": 0, "lynx": 2}},
            {"text": "Терпимо, но не в восторге",
             "points": {"manul": 2, "polar_bear": 1, "penguin": 1, "flamingo": 1, "lynx": 1}},
            {"text": "Ненавижу! Дайте мне тепло!",
             "points": {"manul": 0, "polar_bear": 0, "penguin": 0, "flamingo": 3, "lynx": 0}},
            {"text": "Зависит от настроения",
             "points": {"manul": 2, "polar_bear": 1, "penguin": 1, "flamingo": 1, "lynx": 2}},
        ]
    },
    {
        "id": 5,
        "text": "🦸‍♀️ Ваша суперсила — это...",
        "options": [
            {"text": "Невероятная скрытность и терпение",
             "points": {"manul": 3, "polar_bear": 0, "penguin": 0, "flamingo": 1, "lynx": 2}},
            {"text": "Умение плавать в ледяной воде",
             "points": {"manul": 0, "polar_bear": 3, "penguin": 2, "flamingo": 0, "lynx": 0}},
            {"text": "Способность быть душой компании",
             "points": {"manul": 0, "polar_bear": 1, "penguin": 2, "flamingo": 3, "lynx": 0}},
            {"text": "Прыгучесть и ловкость",
             "points": {"manul": 0, "polar_bear": 0, "penguin": 0, "flamingo": 0, "lynx": 3}},
        ]
    },
    {
        "id": 6,
        "text": "🐾 Настоящий факт: в Московском зоопарке манул Тимофей — настоящая звезда соцсетей. Он любит...",
        "options": [
            {"text": "Спать 20 часов в сутки и делать вид, что всех игнорирует",
             "points": {"manul": 3, "polar_bear": 0, "penguin": 0, "flamingo": 0, "lynx": 1}},
            {"text": "Активно играть с посетителями",
             "points": {"manul": 0, "polar_bear": 1, "penguin": 2, "flamingo": 1, "lynx": 0}},
            {"text": "Позировать для фото",
             "points": {"manul": 1, "polar_bear": 1, "penguin": 1, "flamingo": 3, "lynx": 0}},
            {"text": "Охотиться на снегирей за окном",
             "points": {"manul": 2, "polar_bear": 1, "penguin": 0, "flamingo": 0, "lynx": 3}},
        ]
    }
]

# Данные о животных-тотемах
TOTEM_ANIMALS = {
    "manul": {
        "name": "🐈 Манул (Палласов кот)",
        "description": "Ты — манул! Независимый, мудрый и немного ворчливый. Ты ценишь одиночество и уют, но при этом остаёшься легендой в узких кругах. Как и звёздный манул Тимофей, ты знаешь себе цену и не тратишь энергию на ерунду. Ты — идеальный кандидат в опекуны: твоя забота будет тихой, но надёжной.",
        "fact": "Интересный факт: Манулы — самые пушистые кошки в мире, у них до 9000 волосков на 1 см²!",
        "image": "manul.jpg",
        "opeka_link": "https://moscowzoo.ru/guardianship/manul"
    },
    "polar_bear": {
        "name": "🐻‍❄️ Белый медведь",
        "description": "Ты — белый медведь! Сильный, выносливый и величественный. Тебе нипочём любые испытания, ты способен покорять суровые стихии. В Московском зоопарке белые медведи — настоящие атланты, требующие особой заботы. Твоя мощь и доброта помогут дикой природе!",
        "fact": "Интересный факт: Под белой шерстью белого медведя скрывается чёрная кожа, которая притягивает солнечное тепло!",
        "image": "polar_bear.jpg",
        "opeka_link": "https://moscowzoo.ru/guardianship/polar-bear"
    },
    "penguin": {
        "name": "🐧 Пингвин Гумбольдта",
        "description": "Ты — пингвин Гумбольдта! Общительный, жизнерадостный и командный игрок. Ты любишь быть в центре событий и поддерживать друзей. В Московском зоопарке пингвины каждый день устраивают заплывы и радуют посетителей. Твоя энергичность и забота нужны тем, кто в этом особенно нуждается!",
        "fact": "Интересный факт: Пингвины Гумбольдта умеют издавать звук, похожий на ослиный рёв, чтобы общаться в колонии!",
        "image": "penguin.jpg",
        "opeka_link": "https://moscowzoo.ru/guardianship/penguin"
    },
    "flamingo": {
        "name": "🦩 Фламинго",
        "description": "Ты — фламинго! Элегантный, яркий и немного экстравагантный. Ты притягиваешь взгляды и любишь красоту во всём. Розовые фламинго Московского зоопарка — настоящие аристократы среди птиц. Твоя утончённая душа сможет подарить тепло и заботу тем, кто в этом нуждается!",
        "fact": "Интересный факт: Розовый цвет фламинго — результат их питания креветками и водорослями, богатыми каротином!",
        "image": "flamingo.jpg",
        "opeka_link": "https://moscowzoo.ru/guardianship/flamingo"
    },
    "lynx": {
        "name": "🐆 Рысь",
        "description": "Ты — рысь! Грациозный, ловкий и немного загадочный. Ты умеешь быть незаметным, но когда нужно — проявляешь невероятную силу. Как рысятки Чип и Гайка из Московского зоопарка, ты — охотник по натуре, но мягкий в душе. Твоя помощь будет неоценима для сохранения редких видов!",
        "fact": "Интересный факт: Рыси могут прыгать на расстояние до 4 метров и слышать мышь за 100 метров!",
        "image": "lynx.jpg",
        "opeka_link": "https://moscowzoo.ru/guardianship/lynx"
    }
}


def calculate_totem(user_answers):
    """Подсчёт баллов и определение тотемного животного"""
    scores = {animal: 0 for animal in TOTEM_ANIMALS.keys()}

    for i, answer_points in enumerate(user_answers):
        if i < len(QUESTIONS):
            for animal, points in answer_points.items():
                scores[animal] += points

    # Возвращаем животное с максимальными баллами
    totem = max(scores, key=scores.get)
    return totem, scores

