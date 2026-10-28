# content.py - text for the Family Interview guide and the glossary.
# Edit the wording here without touching the page code.

# Questions an SLP can ask a family when building a language history.
# Each question is written in every interview language. {lang} is replaced
# with each language the child hears, named the way that language names it.
# Every version except English is a draft: have a native speaker review it
# before using it with families.

# Interview languages: display name -> code
INTERVIEW_LANGUAGES = {
    "English": "en",
    "Español": "es",
    "Tiếng Việt": "vi",
    "简体中文 (Mandarin)": "zh_s",
    "繁體中文 (Cantonese)": "zh_t",
    "العربية": "ar",
}
RTL_CODES = {"ar"}

INTERVIEW = [
    {"title": {"en": "Language history", "es": "Historia lingüística",
               "vi": "Lịch sử ngôn ngữ", "zh_s": "语言背景", "zh_t": "語言背景",
               "ar": "التاريخ اللغوي"},
     "questions": [
        {"en": "Which languages does your child hear at home?",
         "es": "¿Qué idiomas escucha su hijo o hija en casa?",
         "vi": "Ở nhà, bé nghe những ngôn ngữ nào?",
         "zh_s": "孩子在家里听到哪些语言？",
         "zh_t": "孩子在家裡聽到哪些語言？",
         "ar": "ما اللغات التي يسمعها طفلك في البيت؟"},
        {"en": "Who speaks {lang} with your child?",
         "es": "¿Quién habla {lang} con su hijo o hija?",
         "vi": "Ai nói {lang} với bé?",
         "zh_s": "谁和孩子说{lang}？",
         "zh_t": "誰和孩子說{lang}？",
         "ar": "من يتحدث {lang} مع طفلك؟"},
        {"en": "At what age did your child start hearing {lang}?",
         "es": "¿A qué edad empezó su hijo o hija a escuchar {lang}?",
         "vi": "Bé bắt đầu nghe {lang} từ lúc mấy tuổi?",
         "zh_s": "孩子几岁开始听到{lang}？",
         "zh_t": "孩子幾歲開始聽到{lang}？",
         "ar": "في أي عمر بدأ طفلك يسمع {lang}؟"},
        {"en": "Which language does your child choose when talking with you?",
         "es": "¿Qué idioma elige su hijo o hija cuando habla con usted?",
         "vi": "Khi nói chuyện với anh/chị, bé thường chọn ngôn ngữ nào?",
         "zh_s": "孩子和您说话时会选择哪种语言？",
         "zh_t": "孩子和您說話時會選擇哪種語言？",
         "ar": "ما اللغة التي يختارها طفلك عندما يتحدث معك؟"},
        {"en": "Has the amount of each language at home changed, for example after "
               "starting school?",
         "es": "¿Ha cambiado cuánto se usa cada idioma en casa, por ejemplo, después de "
               "empezar la escuela?",
         "vi": "Lượng sử dụng mỗi ngôn ngữ ở nhà có thay đổi không, ví dụ sau khi bé "
               "bắt đầu đi học?",
         "zh_s": "家里每种语言的使用量有没有变化，比如在孩子上学以后？",
         "zh_t": "家裡每種語言的使用量有沒有變化，例如在孩子上學以後？",
         "ar": "هل تغيّر مقدار استخدام كل لغة في البيت، مثلًا بعد دخول طفلك المدرسة؟"},
     ]},
    {"title": {"en": "A typical week", "es": "Una semana típica",
               "vi": "Một tuần bình thường", "zh_s": "平常的一周", "zh_t": "平常的一週",
               "ar": "أسبوع عادي"},
     "questions": [
        {"en": "Who takes care of your child on weekdays, and which language do they use?",
         "es": "¿Quién cuida a su hijo o hija entre semana y qué idioma usa?",
         "vi": "Vào các ngày trong tuần, ai chăm sóc bé, và người đó dùng ngôn ngữ nào?",
         "zh_s": "平日谁照顾孩子？他们说哪种语言？",
         "zh_t": "平日誰照顧孩子？他們說哪種語言？",
         "ar": "من يعتني بطفلك في أيام الأسبوع، وما اللغة التي يستخدمها؟"},
        {"en": "Which language does your child hear at daycare or school?",
         "es": "¿Qué idioma escucha su hijo o hija en la guardería o en la escuela?",
         "vi": "Ở nhà trẻ hoặc ở trường, bé nghe ngôn ngữ nào?",
         "zh_s": "孩子在托儿所或学校听到哪种语言？",
         "zh_t": "孩子在托兒所或學校聽到哪種語言？",
         "ar": "ما اللغة التي يسمعها طفلك في الحضانة أو المدرسة؟"},
        {"en": "Which language are your child's shows, videos, songs, and books in?",
         "es": "¿En qué idioma son los programas, videos, canciones y libros de su hijo o hija?",
         "vi": "Các chương trình TV, video, bài hát và sách của bé bằng ngôn ngữ nào?",
         "zh_s": "孩子看的节目、视频，听的歌曲和读的书是哪种语言的？",
         "zh_t": "孩子看的節目、影片，聽的歌曲和讀的書是哪種語言的？",
         "ar": "بأي لغة البرامج والفيديوهات والأغاني والكتب التي يتابعها طفلك؟"},
        {"en": "Which language does your child use with siblings, cousins, or friends?",
         "es": "¿Qué idioma usa su hijo o hija con sus hermanos, primos o amigos?",
         "vi": "Bé dùng ngôn ngữ nào khi nói với anh chị em, anh chị em họ hoặc bạn bè?",
         "zh_s": "孩子和兄弟姐妹、表兄弟姐妹或朋友说哪种语言？",
         "zh_t": "孩子和兄弟姊妹、表兄弟姊妹或朋友說哪種語言？",
         "ar": "ما اللغة التي يستخدمها طفلك مع إخوته أو أقاربه أو أصدقائه؟"},
     ]},
    {"title": {"en": "Communication in the home language",
               "es": "Comunicación en el idioma del hogar",
               "vi": "Giao tiếp bằng ngôn ngữ ở nhà", "zh_s": "家庭语言的沟通",
               "zh_t": "家庭語言的溝通", "ar": "التواصل بلغة البيت"},
     "questions": [
        {"en": "Does your child understand what you say in {lang}?",
         "es": "¿Su hijo o hija entiende lo que usted le dice en {lang}?",
         "vi": "Bé có hiểu những gì anh/chị nói bằng {lang} không?",
         "zh_s": "孩子能听懂您用{lang}说的话吗？",
         "zh_t": "孩子能聽懂您用{lang}說的話嗎？",
         "ar": "هل يفهم طفلك ما تقوله له ب{lang}؟"},
        {"en": "Do other family members have concerns about how your child talks in {lang}?",
         "es": "¿Otros familiares se preocupan por cómo habla su hijo o hija en {lang}?",
         "vi": "Những người khác trong gia đình có lo lắng về cách bé nói {lang} không?",
         "zh_s": "其他家人对孩子说{lang}的情况有担心吗？",
         "zh_t": "其他家人對孩子說{lang}的情況有擔心嗎？",
         "ar": "هل لدى أفراد العائلة الآخرين مخاوف بشأن طريقة كلام طفلك ب{lang}؟"},
        {"en": "How does your child communicate compared with children of the same age "
               "in your family or community?",
         "es": "¿Cómo se comunica su hijo o hija en comparación con otros niños de la "
               "misma edad en su familia o comunidad?",
         "vi": "So với các trẻ cùng tuổi trong gia đình hoặc cộng đồng, bé giao tiếp "
               "như thế nào?",
         "zh_s": "和家里或社区里同龄的孩子相比，孩子的沟通情况怎么样？",
         "zh_t": "和家裡或社區裡同齡的孩子相比，孩子的溝通情況怎麼樣？",
         "ar": "كيف يتواصل طفلك مقارنةً بالأطفال في مثل عمره في عائلتك أو مجتمعك؟"},
        {"en": "When did your child say first words, in any language?",
         "es": "¿Cuándo dijo su hijo o hija sus primeras palabras, en cualquier idioma?",
         "vi": "Bé nói những từ đầu tiên lúc nào, bằng bất kỳ ngôn ngữ nào?",
         "zh_s": "孩子什么时候说出第一个词（任何语言）？",
         "zh_t": "孩子什麼時候說出第一個詞（任何語言）？",
         "ar": "متى قال طفلك كلماته الأولى، بأي لغة كانت؟"},
     ]},
    {"title": {"en": "Dialect and background", "es": "Dialecto y antecedentes",
               "vi": "Phương ngữ và hoàn cảnh gia đình", "zh_s": "方言与家庭背景",
               "zh_t": "方言與家庭背景", "ar": "اللهجة والخلفية"},
     "questions": [
        {"en": "Which dialect or region of {lang} does your family speak?",
         "es": "¿Qué dialecto o variante regional de {lang} habla su familia?",
         "vi": "Gia đình anh/chị nói {lang} theo giọng hoặc vùng miền nào?",
         "zh_s": "您家说的是哪种{lang}方言，或哪个地区的口音？",
         "zh_t": "您家說的是哪種{lang}方言，或哪個地區的口音？",
         "ar": "ما لهجة {lang} التي تتحدثها عائلتك، ومن أي منطقة؟"},
        {"en": "Has anyone in the family had difficulty with speech, language, reading, "
               "or hearing?",
         "es": "¿Alguien en la familia ha tenido dificultades con el habla, el lenguaje, "
               "la lectura o la audición?",
         "vi": "Trong gia đình có ai từng gặp khó khăn về phát âm, ngôn ngữ, đọc hoặc "
               "thính lực không?",
         "zh_s": "家里有没有人在说话、语言、阅读或听力方面有过困难？",
         "zh_t": "家裡有沒有人在說話、語言、閱讀或聽力方面有過困難？",
         "ar": "هل واجه أحد في العائلة صعوبات في النطق أو اللغة أو القراءة أو السمع؟"},
        {"en": "Has your child's hearing been checked? When?",
         "es": "¿Le han revisado la audición a su hijo o hija? ¿Cuándo?",
         "vi": "Bé đã được kiểm tra thính lực chưa? Khi nào?",
         "zh_s": "孩子做过听力检查吗？什么时候？",
         "zh_t": "孩子做過聽力檢查嗎？什麼時候？",
         "ar": "هل فُحص سمع طفلك؟ متى؟"},
     ]},
]

# Labels for the printed interview, in every interview language.
INTERVIEW_LABELS = {
    "heading": {"en": "Family language interview",
                "es": "Entrevista familiar sobre los idiomas",
                "vi": "Phỏng vấn gia đình về ngôn ngữ", "zh_s": "家庭语言访谈",
                "zh_t": "家庭語言訪談", "ar": "مقابلة العائلة حول اللغة"},
    "case": {"en": "Case", "es": "Caso", "vi": "Mã hồ sơ", "zh_s": "个案编号",
             "zh_t": "個案編號", "ar": "رقم الحالة"},
    "date": {"en": "Date", "es": "Fecha", "vi": "Ngày", "zh_s": "日期", "zh_t": "日期",
             "ar": "التاريخ"},
    "interpreter": {"en": "Interpreter used? Yes / No",
                    "es": "¿Se usó intérprete? Sí / No",
                    "vi": "Có dùng thông dịch viên? Có / Không",
                    "zh_s": "是否使用口译员？是 / 否", "zh_t": "是否使用傳譯員？是 / 否",
                    "ar": "هل استُخدم مترجم؟ نعم / لا"},
    "home_language": {"en": "the home language", "es": "el idioma del hogar",
                      "vi": "ngôn ngữ ở nhà", "zh_s": "家庭语言", "zh_t": "家庭語言",
                      "ar": "لغة البيت"},
}

# How each language's name reads inside a sentence in each interview language.
LANGUAGE_NAMES = {
    "es": {"spanish": "español", "english": "inglés", "vietnamese": "vietnamita",
           "mandarin": "mandarín", "cantonese": "cantonés", "arabic": "árabe",
           "chinese": "chino", "french": "francés", "korean": "coreano",
           "tagalog": "tagalo"},
    "vi": {"vietnamese": "tiếng Việt", "english": "tiếng Anh",
           "spanish": "tiếng Tây Ban Nha", "chinese": "tiếng Trung",
           "mandarin": "tiếng Quan Thoại", "cantonese": "tiếng Quảng Đông",
           "french": "tiếng Pháp", "korean": "tiếng Hàn", "japanese": "tiếng Nhật",
           "tagalog": "tiếng Tagalog", "arabic": "tiếng Ả Rập"},
    "zh_s": {"mandarin": "普通话", "cantonese": "粤语", "chinese": "中文",
             "english": "英语", "spanish": "西班牙语", "vietnamese": "越南语",
             "arabic": "阿拉伯语", "korean": "韩语", "tagalog": "他加禄语"},
    "zh_t": {"mandarin": "普通話", "cantonese": "廣東話", "chinese": "中文",
             "english": "英語", "spanish": "西班牙語", "vietnamese": "越南語",
             "arabic": "阿拉伯語", "korean": "韓語", "tagalog": "他加祿語"},
    "ar": {"arabic": "العربية", "english": "الإنجليزية", "spanish": "الإسبانية",
           "vietnamese": "الفيتنامية", "mandarin": "الصينية الماندرينية",
           "cantonese": "الكانتونية", "chinese": "الصينية", "french": "الفرنسية",
           "korean": "الكورية"},
}


def name_in(code, name):
    """A language's name as it reads in a sentence in another language."""
    if code == "en":
        return name
    return LANGUAGE_NAMES.get(code, {}).get(name.strip().lower(), name.strip())


def interview_lines(languages, code="en", with_english=False):
    """The interview as [(section title, [(question, english or None), ...])]."""
    sections = []
    for section in INTERVIEW:
        title = section["title"][code]
        if with_english and code != "en":
            title += f" / {section['title']['en']}"
        lines = []
        for q in section["questions"]:
            langs = languages if (languages and "{lang}" in q["en"]) else [None]
            for lang in langs:
                if lang is None:
                    home = INTERVIEW_LABELS["home_language"]
                    main = q[code].replace("{lang}", home[code])
                    eng = q["en"].replace("{lang}", home["en"])
                else:
                    main = q[code].replace("{lang}", name_in(code, lang))
                    eng = q["en"].replace("{lang}", lang)
                lines.append((main, eng if (with_english and code != "en") else None))
        sections.append((title, lines))
    return sections


# Plain-language definitions of terms used on the site.
GLOSSARY = {
    "CLD": "Culturally and linguistically diverse. Describes people whose culture "
           "or language differs from the majority culture or language around them.",
    "Language difference": "Differences in a child's speech or language that come "
                           "from learning another language or dialect. A difference "
                           "is not a disorder.",
    "Language disorder": "A difficulty understanding or using language that affects "
                         "all of a child's languages, not only the one they hear less.",
    "Receptive language": "Understanding language: what the child takes in when "
                          "others talk.",
    "Expressive language": "Using language: what the child says or signs.",
    "Language exposure": "How much a child hears a language, often measured as a "
                         "percentage of waking hours or hours per week.",
    "Language dominance": "Which language a child knows best at a given time. "
                          "Dominance can shift, for example after the child starts school.",
    "Code-switching": "Moving between two languages within a conversation or a "
                      "sentence. Code-switching is a typical part of bilingual "
                      "language use.",
    "Dialect": "A regional or social variety of a language with its own sounds, "
               "words, or grammar.",
    "Dynamic assessment": "A test-teach-retest approach. The SLP teaches a skill "
                          "and measures how easily the child learns it.",
    "Phonemic inventory": "The set of speech sounds a language uses to tell words apart.",
    "Tone": "A change in pitch that changes a word's meaning. Vietnamese uses tones. "
            "English does not.",
    "Code-mixing": "Using words or grammar from two languages in one sentence. In young "
                   "bilingual children, code-mixing reflects knowledge of both grammars, "
                   "not confusion (Genesee, 2009).",
    "Diglossia": "Two varieties of one language used for different purposes, like Spoken "
                 "Arabic at home and Standard Arabic at school.",
    "Place of articulation": "Where in the mouth a sound is made, such as the lips, the "
                             "gum ridge, or the soft palate.",
    "Age notation": "Speech research writes ages as years;months. 3;6 means 3 years, "
                    "6 months.",
}


# Session phrases for SLPs, by language. (Vietnamese, English)
# Draft wording: not yet reviewed by a native speaker. See REVIEW_STATUS in views.py.
PHRASES = {
    "Vietnamese": [
        ("Xin chào", "Hello"),
        ("Con tên gì?", "What's your name? (to a child)"),
        ("Nhìn nè.", "Look."),
        ("Chỉ cho cô cái ___.", "Show me the ___."),
        ("Nói theo cô: ___.", "Say after me: ___."),
        ("Giỏi lắm!", "Great job!"),
        ("Thử lại nhé.", "Let's try again."),
        ("Mình nghỉ một chút nhé.", "Let's take a short break."),
        ("Xong rồi!", "All done!"),
        ("Cảm ơn con.", "Thank you. (to a child)"),
    ],
}
