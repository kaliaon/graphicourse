#!/usr/bin/env python
"""
Comprehensive script to populate the database with lesson data, including detailed quiz structures
and correct answers for open-ended questions.

This script should be run from the project root directory using:
python populate_lessons_comprehensive.py

It replaces all other population scripts with a single consolidated solution.
"""

import os
import django
import random
import sys
import io

# Set stdout to use utf-8 encoding to avoid WinUnicodeError
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courses_platform.settings')
django.setup()

from courses.models import Course, Lesson, Test, Question, Choice, QuestionType
from django.db import connection

def create_quiz_questions(title, subject, num_questions=3):
    """Create natural quiz questions for a lesson with correct answers for open-ended questions."""
    questions = []
    
    # Define realistic questions based on the subject
    realistic_questions = {
        "Растрлық және векторлық графиканың негіздері": [
            {
                "text": "Растрлық графика нені негізге алады?",
                "type": "multiple_choice",
                "explanation": "Растрлық графика пиксельдер деп аталатын кішкентай нүктелердің жиынтығынан тұрады. Әр пиксельдің өз түсі мен орны болады.",
                "choices": [
                    {"text": "Векторлық формулаларды", "is_correct": False},
                    {"text": "Геометриялық объектілерді", "is_correct": False},
                    {"text": "Пиксельдер жиынтығын", "is_correct": True},
                    {"text": "Үшөлшемді модельдерді", "is_correct": False}
                ]
            },
            {
                "text": "Қай графика түрі масштабтағанда сапасын жоғалтпайды?",
                "type": "multiple_choice",
                "explanation": "Векторлық графика математикалық формулаларға негізделгендіктен, оны кез келген өлшемге дейін сапасын жоғалтпай үлкейтуге болады.",
                "choices": [
                    {"text": "Растрлық", "is_correct": False},
                    {"text": "Векторлық", "is_correct": True},
                    {"text": "Фото", "is_correct": False},
                    {"text": "Анимациялық", "is_correct": False}
                ]
            },
            {
                "text": "Берілген екі суреттің қайсысы растрлық, қайсысы векторлық екенін анықтаңыз және таңдау себебін қысқаша түсіндіріңіз.",
                "type": "open_ended",
                "explanation": "Растрлық графика пиксельдерге негізделген (фотолар), ал векторлық графика формулаларға негізделген (логотиптер).",
                "correct_answer": "Растрлық сурет пиксельдерден тұрады және үлкейткенде сапасын жоғалтады (фотосуреттер). Векторлық сурет математикалық формулалардан тұрады және үлкейткенде сапасын сақтайды (логотиптер, сызбалар)."
            }
        ],
        "Түстер модельдері және түспен жұмыс істеу принциптері": [
            {
                "text": "Қай түстер моделі экранда бейнелеу үшін қолданылады?",
                "type": "multiple_choice",
                "explanation": "RGB (Red, Green, Blue) моделі экрандарда жарық сәулелерін қосу арқылы түстерді қалыптастыру үшін қолданылады.",
                "choices": [
                    {"text": "CMYK", "is_correct": False},
                    {"text": "HSV", "is_correct": False},
                    {"text": "RGB", "is_correct": True},
                    {"text": "LAB", "is_correct": False}
                ]
            },
            {
                "text": "CMYK моделі қандай принципке негізделген?",
                "type": "multiple_choice",
                "explanation": "CMYK - субтрактивті модель. Ол ақ қағаздан шағылысатын жарықты бояулар арқылы азайту (субтракция) принципіне негізделген.",
                "choices": [
                    {"text": "Аддитивті", "is_correct": False},
                    {"text": "Геометриялық", "is_correct": False},
                    {"text": "Субтрактивті", "is_correct": True},
                    {"text": "Кеңістіктік", "is_correct": False}
                ]
            },
            {
                "text": "RGB және CMYK модельдерінің негізгі айырмашылығын түсіндіріңіз және олардың қолданылу салаларын атаңыз.",
                "type": "open_ended",
                "explanation": "RGB - экрандарға арналған аддитивті модель, CMYK - баспа өнімдеріне арналған субтрактивті модель.",
                "correct_answer": "RGB - бұл жарық қосу арқылы түстерді қалыптастыратын аддитивті модель, ол экрандар мен мониторлар үшін қолданылады. CMYK - бұл бояуларды араластыру арқылы жарықты азайтатын субтрактивті модель, ол баспа өнімдері үшін қолданылады."
            }
        ],
        "Геометриялық түрлендірулер және графикалық объектілер": [
            {
                "text": "Объектінің өлшемін өзгертуге арналған түрлендіру қайсы?",
                "type": "multiple_choice",
                "explanation": "Масштабтау (Scaling) объектінің барлық нүктелерінің координаталарын белгілі бір коэффициентке көбейту арқылы оның өлшемін өзгертеді.",
                "choices": [
                    {"text": "Орын ауыстыру", "is_correct": False},
                    {"text": "Айналдыру", "is_correct": False},
                    {"text": "Масштабтау", "is_correct": True},
                    {"text": "Көлеңкелеу", "is_correct": False}
                ]
            },
            {
                "text": "Айналдыру операциясы нені өзгертеді?",
                "type": "multiple_choice",
                "explanation": "Айналдыру (Rotation) объектіні белгілі бір нүктеден (орталықтан) белгілі бір бұрышқа бұру арқылы оның бағытын өзгертеді.",
                "choices": [
                    {"text": "Түсін", "is_correct": False},
                    {"text": "Құрылымын", "is_correct": False},
                    {"text": "Бағытын", "is_correct": True},
                    {"text": "Файл көлемін", "is_correct": False}
                ]
            },
            {
                "text": "Үш негізгі геометриялық түрлендіруді атаңыз және олардың әрқайсысының мақсатын қысқаша түсіндіріңіз.",
                "type": "open_ended",
                "explanation": "Орын ауыстыру - жылжыту, Масштабтау - өлшемді өзгерту, Айналдыру - бағытты өзгерту.",
                "correct_answer": "1) Орын ауыстыру - объектіні жылжыту арқылы оның орналасуын реттейді; 2) Масштабтау - объектінің өлшемін үлкейту немесе кішірейту арқылы оның көлемін басқарады; 3) Айналдыру - объектіні бұру арқылы оның бағытын өзгертеді."
            }
        ],
        "Үшөлшемді графиканың негізгі ұғымдары": [
            {
                "text": "Үшөлшемді графикада қанша координата осі қолданылады?",
                "type": "multiple_choice",
                "explanation": "3D графикада кеңістікті анықтау үшін үш өзара перпендикуляр ось қолданылады: X (ені), Y (биіктігі) және Z (тереңдігі).",
                "choices": [
                    {"text": "Бір", "is_correct": False},
                    {"text": "Екі", "is_correct": False},
                    {"text": "Үш", "is_correct": True},
                    {"text": "Төрт", "is_correct": False}
                ]
            },
            {
                "text": "Камера ұғымы нені анықтайды?",
                "type": "multiple_choice",
                "explanation": "Камера виртуалды кеңістікте бақылаушының орнын және қарау бағытын анықтайды, яғни көрініс бұрышын белгілейді.",
                "choices": [
                    {"text": "Объектінің түсін", "is_correct": False},
                    {"text": "Файл көлемін", "is_correct": False},
                    {"text": "Көрініс бұрышын", "is_correct": True},
                    {"text": "Пиксель санын", "is_correct": False}
                ]
            },
            {
                "text": "Үшөлшемді объектінің құрылымын сипаттайтын негізгі үш элементті (нүкте, қабырға, бет) түсіндіріңіз.",
                "type": "open_ended",
                "explanation": "Нүкте - координата, Қабырға - қосу сызығы, Бет - жазықтық бөлігі.",
                "correct_answer": "1) Нүкте (Vertex) - объектінің кеңістіктегі координатасы; 2) Қабырға (Edge) - екі нүктені қосатын сызық; 3) Бет (Face/Polygon) - қабырғалармен шектелген жазықтық бөлігі. Осы үш элементтің жиынтығы 3D модельдің геометриялық пішінін құрайды."
            }
        ],
        "Жарықтандыру және визуализация негіздері": [
            {
                "text": "Нүктелік жарық (Point Light) қалай таралады?",
                "type": "multiple_choice",
                "explanation": "Нүктелік жарық (Point Light) жарық көзінен барлық бағытқа (360 градус) тең дәрежеде таралады, шам немесе от сияқты.",
                "choices": [
                    {"text": "Тек бір бағытқа", "is_correct": False},
                    {"text": "Параллель сәулелермен", "is_correct": False},
                    {"text": "Барлық бағытқа", "is_correct": True},
                    {"text": "Тек төмен қарай", "is_correct": False}
                ]
            },
            {
                "text": "Визуализация (Рендеринг) дегеніміз не?",
                "type": "multiple_choice",
                "explanation": "Рендеринг - 3D модельден дайын 2D кескін немесе бейнеесептеу процесі. Ол барлық жарық, материал және камера параметрлерін есепке алады.",
                "choices": [
                    {"text": "Модельді жасау", "is_correct": False},
                    {"text": "Көріністі экранда бейнелеу (есептеу)", "is_correct": True},
                    {"text": "Объектіні айналдыру", "is_correct": False},
                    {"text": "Түсті таңдау", "is_correct": False}
                ]
            },
            {
                "text": "Шашыраңқы жарық (Ambient Light) нені анықтайды?",
                "type": "open_ended",
                "explanation": "Ambient Light сахнаның ең төменгі жарық деңгейін анықтайды және көлеңкелердің өте қараңғы болмауын қамтамасыз етеді.",
                "correct_answer": "Шашыраңқы жарық сахнаның жалпы жарық деңгейін анықтайды. Ол ешқандай бағытсыз, бүкіл кеңістікті біркелкі жарықтандырады және көлеңкелердің тым қараңғы болмауын қамтамасыз етеді."
            }
        ],
        "Үлкен деректер массивтерін өңдеу және талдау технологиялары": [
            {
                "text": "Үлкен деректердің 3V қасиеттерін түсіндіріңіз.",
                "type": "open_ended",
                "correct_answer": "Үлкен деректердің 3V қасиеттері: 1) Volume (Көлем) - үлкен көлемдегі деректер; 2) Velocity (Жылдамдық) - деректердің жоғары жылдамдықпен өндірілуі және өңделуі; 3) Variety (Әртүрлілік) - құрылымдалған, жартылай құрылымдалған және құрылымдалмаған деректердің алуан түрлі форматтары."
            },
            {
                "text": "Hadoop фреймворкінің негізгі компоненттерін сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "Hadoop фреймворкінің негізгі компоненттері: 1) HDFS (Hadoop Distributed File System) - деректерді үлестірілген сақтау жүйесі; 2) MapReduce - үлкен деректерді параллельді өңдеу үшін бағдарламалау моделі; 3) YARN (Yet Another Resource Negotiator) - ресурстарды басқару платформасы; 4) Hadoop Common - басқа Hadoop модульдеріне ортақ утилиталар."
            },
            {
                "text": "MapReduce парадигмасының негізгі кезеңдері қандай?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Құру, өңдеу және визуализациялау",
                        "is_correct": False
                    },
                    {
                        "text": "Map, Shuffle және Reduce",
                        "is_correct": True
                    },
                    {
                        "text": "Жүктеу, талдау және сақтау",
                        "is_correct": False
                    },
                    {
                        "text": "Құрылымдау, тазалау және түрлендіру",
                        "is_correct": False
                    }
                ]
            },
            {
                "text": "Hadoop және Apache Spark арасындағы негізгі айырмашылық қандай?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Оларда архитектуралық айырмашылықтар жоқ",
                        "is_correct": False
                    },
                    {
                        "text": "Hadoop тек жадыда өңдеуді қолданады, ал Spark диск арқылы жұмыс істейді",
                        "is_correct": False
                    },
                    {
                        "text": "Spark тек құрылымдалған деректермен жұмыс істейді, ал Hadoop тек құрылымдалмаған деректермен",
                        "is_correct": False
                    },
                    {
                        "text": "Spark жадыда өңдеуді қолданады, ал Hadoop диск арқылы жұмыс істейді",
                        "is_correct": True
                    }
                ]
            }
        ],
        "Үлестірілген жүйелердің архитектурасы": [
            {
                "text": "Үлестірілген жүйе архитектурасын жобалау кезінде ескерілетін факторларды атаңыз.",
                "type": "open_ended",
                "correct_answer": "Үлестірілген жүйе архитектурасын жобалау кезінде ескерілетін факторлар: 1) Масштабталу - жүйенің өсуіне дайын болу; 2) Қолжетімділік - жүйе компоненттерінің істен шыққан жағдайда жұмыс істеуді жалғастыру қабілеті; 3) Өнімділік - төмен кідіріс пен жоғары өткізу қабілеті; 4) Қауіпсіздік - аутентификация, авторизация, шифрлау; 5) Үйлесімділік - әртүрлі технологиялармен жұмыс істеу мүмкіндігі; 6) Басқарылатындық - мониторинг, журналдау және конфигурация."
            },
            {
                "text": "Үлестірілген жүйе архитектурасының негізгі түрлерін сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "Үлестірілген жүйе архитектурасының негізгі түрлері: 1) Клиент-сервер архитектурасы - клиенттер серверлерге сұраныс жібереді және жауап алады; 2) Peer-to-peer (P2P) архитектурасы - барлық түйіндер тең құқылы және ресурстарды бөліседі; 3) Үш деңгейлі архитектура - презентация деңгейі, бизнес-логика деңгейі және деректер деңгейі; 4) Микросервистік архитектура - жүйе бір-бірімен әрекеттесетін шағын, тәуелсіз қызметтерден тұрады; 5) Service-Oriented Architecture (SOA) - қызметтер стандартталған интерфейстер арқылы байланысады."
            },
            {
                "text": "Үлестірілген жүйелерде қандай қауіпсіздік механизмдері қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Аутентификация, авторизация, шифрлау және аудит",
                        "is_correct": True
                    },
                    {
                        "text": "Тек биометриялық тексеру",
                        "is_correct": False
                    },
                    {
                        "text": "Желілік мониторинг және бейне бақылау",
                        "is_correct": False
                    },
                    {
                        "text": "Физикалық кіруді бақылау және құжаттарды сақтау",
                        "is_correct": False
                    }
                ]
            },
            {
                "text": "Үлестірілген деректер базасында (distributed database) қандай деректер репликация стратегиялары қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Толық репликация, толық емес репликация және синхронды/асинхронды репликация",
                        "is_correct": True
                    },
                    {
                        "text": "Тек қана batch репликация",
                        "is_correct": False
                    },
                    {
                        "text": "Деректерді үлестірілген базаларда репликациялау мүмкін емес",
                        "is_correct": False
                    },
                    {
                        "text": "Тек бір бағытты репликация",
                        "is_correct": False
                    }
                ]
            }
        ],
        "Үлкен деректермен жұмыс": [
            {
                "text": "PySpark экожүйесінің негізгі компоненттерін сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "PySpark экожүйесінің негізгі компоненттері: 1) Spark Core - негізгі функционалдылық, RDD интерфейсі; 2) Spark SQL - құрылымдық деректерді өңдеу; 3) MLlib - машиналық оқыту; 4) GraphX - графтармен жұмыс; 5) Structured Streaming - нақты уақыттағы деректер ағындарын өңдеу. Бұл компоненттер үлкен деректерді параллельді өңдеу, талдау, машиналық оқыту модельдерін құру және графтық талдау үшін қолданылады."
            },
            {
                "text": "Үлкен деректерді өңдеу кезінде қандай архитектуралық шешімдер қолданылады?",
                "type": "open_ended",
                "correct_answer": "Үлкен деректерді өңдеу архитектурасы: 1) Lambda архитектурасы - batch және stream өңдеуді біріктіреді; 2) Kappa архитектурасы - барлық деректерді ағын ретінде өңдейді; 3) Үлестірілген файлдық жүйелер (HDFS, S3); 4) NoSQL дерекқорлары (MongoDB, Cassandra); 5) Деректерді өңдеу құралдары (Spark, Flink); 6) Ресурстарды басқару (YARN, Kubernetes); 7) Деректерді орталықтандыру (Data Lake, Data Warehouse)."
            },
            {
                "text": "Жадыда өңдеу (in-memory processing) технологиясының артықшылықтары қандай?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Жоғары өнімділік, төмен кідіріс және итеративті алгоритмдерді тиімді орындау",
                        "is_correct": True
                    },
                    {
                        "text": "Аз жад қолданымы және төмен процессор жүктемесі",
                        "is_correct": False
                    },
                    {
                        "text": "Жоғары қауіпсіздік және шифрлау",
                        "is_correct": False
                    },
                    {
                        "text": "Деректердің тұрақты сақталуы және резервтік көшірмелер",
                        "is_correct": False
                    }
                ]
            },
            {
                "text": "Big Data 4V қасиеттері қандай?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Volume, Velocity, Variety, Veracity",
                        "is_correct": True
                    },
                    {
                        "text": "Visibility, Validation, Value, Visualization",
                        "is_correct": False
                    },
                    {
                        "text": "Virtual, Vector, Variable, Volatile",
                        "is_correct": False
                    },
                    {
                        "text": "Vocabulary, Variance, Verification, Vendibility",
                        "is_correct": False
                    }
                ]
            }
        ],
        "PySpark көмегімен деректерді талдауға кіріспе": [
            {
                "text": "SparkSession-ді құру және конфигурациялау процесін сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "SparkSession құру: 1) SparkSession.builder.appName('AppName') - қолданба атауын орнату; 2) config() арқылы параметрлерді орнату (мысалы, .config('spark.executor.memory', '2g')); 3) getOrCreate() әдісін шақыру сессияны құрады немесе бар болса қайтарады. Мысал: spark = SparkSession.builder.appName('MyApp').config('spark.executor.memory', '2g').getOrCreate()"
            },
            {
                "text": "PySpark көмегімен құрылымдық деректерді жүктеу және оқу әдістерін сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "PySpark-та деректерді жүктеу әдістері: 1) CSV: spark.read.csv('path', header=True, inferSchema=True); 2) JSON: spark.read.json('path'); 3) Parquet: spark.read.parquet('path'); 4) JDBC: spark.read.format('jdbc').options(параметрлер).load(); 5) Сүзгілер қолдану: dataframe.filter(condition); 6) Бағандар таңдау: dataframe.select('column1', 'column2')."
            },
            {
                "text": "DataFrame және RDD арасындағы негізгі айырмашылықтар қандай?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "RDD құрылымсыз, төменгі деңгейлі API, DataFrame құрылымдық, жоғары деңгейлі API",
                        "is_correct": True
                    },
                    {
                        "text": "RDD көп ресурсты қажет етеді, DataFrame аз ресурсты қажет етеді",
                        "is_correct": False
                    },
                    {
                        "text": "RDD SQL запростарын қолдайды, DataFrame тек Python кодын қолдайды",
                        "is_correct": False
                    },
                    {
                        "text": "RDD жаңа Spark нұсқаларында ғана қол жетімді, DataFrame ескі нұсқаларда",
                        "is_correct": False
                    }
                ]
            },
            {
                "text": "PySpark-та деректерді жазу үшін қандай әдістер қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "execute(), commit(), save()",
                        "is_correct": False
                    },
                    {
                        "text": "write.csv(), write.json(), write.parquet()",
                        "is_correct": True
                    },
                    {
                        "text": "output(), export(), dump()",
                        "is_correct": False
                    },
                    {
                        "text": "saveToCSV(), saveToJSON(), saveToParquet()",
                        "is_correct": False
                    }
                ]
            }
        ],
        "Деректерді өңдеу": [
            {
                "text": "RDD-мен жұмыс істеу кезіндегі негізгі операцияларды сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "RDD-мен жұмыс істеу кезіндегі негізгі операциялар: 1) Трансформациялар (map, filter, flatMap, union, join) - жаңа RDD жасайды. Мысалы, rdd.map(lambda x: x*2) әр элементті 2-ге көбейтеді; 2) Әрекеттер (actions) (count, collect, reduce, saveAsTextFile) - нәтижелерді қайтарады. Мысалы, rdd.count() элементтер санын қайтарады; 3) Кэштеу (persist, cache) - жадыда сақтау, мысалы rdd.cache() арқылы; 4) Партицияға бөлу (repartition, coalesce) - деректерді қайта ұйымдастыру."
            },
            {
                "text": "PySpark-та mapPartitions және map арасындағы айырмашылық неде?",
                "type": "open_ended",
                "correct_answer": "map және mapPartitions арасындағы айырмашылық: map әр элементке функцияны жеке қолданады, ал mapPartitions толық партицияға функцияны қолданады. mapPartitions әдісі итератор алып, итератор қайтарады және деректерді топпен өңдеу қажет болған кезде өнімділікті жақсартады, бірақ жады қолданымы тұрғысынан тиімді жоспарлауды қажет етеді."
            },
            {
                "text": "RDD-да reduceByKey және groupByKey функцияларының арасындағы өнімділік айырмашылығы неде?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "reduceByKey деректерді бөлгеннен кейін агрегациялайды, groupByKey барлық деректерді бөліп, содан кейін оларды топтастырады",
                        "is_correct": True
                    },
                    {
                        "text": "reduceByKey тек сандық деректермен жұмыс істейді, groupByKey барлық дерек түрлерімен жұмыс істейді",
                        "is_correct": False
                    },
                    {
                        "text": "reduceByKey кем дегенде екі аргументті қажет етеді, groupByKey тек бірді қажет етеді",
                        "is_correct": False
                    },
                    {
                        "text": "reduceByKey деректерді автоматты түрде сұрыптайды, groupByKey сұрыптамайды",
                        "is_correct": False
                    }
                ]
            },
            {
                "text": "PySpark-та қандай түрлендіру (transformation) және әрекет (action) амалдарының арасындағы айырмашылық?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Түрлендірулер құрылымдалған деректермен жұмыс істейді, әрекеттер құрылымданбаған деректермен жұмыс істейді",
                        "is_correct": False
                    },
                    {
                        "text": "Түрлендірулер жаңа RDD/DataFrame жасайды және кейінге қалдырылады, әрекеттер нәтижелерді қайтарады және орындалады",
                        "is_correct": True
                    },
                    {
                        "text": "Түрлендірулер тек Spark SQL-де қолданылады, әрекеттер RDD API-де қолданылады",
                        "is_correct": False
                    },
                    {
                        "text": "Түрлендірулер тек Python функцияларын қабылдайды, әрекеттер барлық тілдердегі функцияларды қабылдайды",
                        "is_correct": False
                    }
                ]
            }
        ],
        "Spark құрылымдық ағыны": [
            {
                "text": "Spark Structured Streaming қосымшасын құру процесін сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "Spark Structured Streaming қосымшасын құру процесі: 1) SparkSession объектісін құру; 2) Ағынды деректер көзін анықтау (readStream көмегімен, мысалы, Kafka, файлдар, сокеттер); 3) Деректерді өңдеу үшін трансформациялар қолдану (select, where, groupBy және т.б.); 4) Нәтижелерді жазу үшін writeStream конфигурациясын анықтау (outputMode, triggerInterval, checkpointLocation); 5) start() әдісімен ағынды өңдеуді бастау; 6) awaitTermination() әдісімен жұмысты аяқтауды күту. Мысалы: spark.readStream.format('kafka').option('subscribe', 'topic1').load().writeStream.format('console').start().awaitTermination()"
            },
            {
                "text": "Spark Streaming және Structured Streaming арасындағы айырмашылықтарды сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "Spark Streaming және Structured Streaming арасындағы айырмашылықтар: 1) Spark Streaming RDD-ға негізделген, ал Structured Streaming DataFrame/Dataset API-ге негізделген; 2) Spark Streaming микро-батчтарда жұмыс істейді, ал Structured Streaming оңтайландырылған incremental query жоспарын қолданады; 3) Structured Streaming жоғары деңгейлі семантиканы қамтиды (SQL сұраулары, аналитикалық функциялар); 4) Structured Streaming end-to-end exactly-once кепілдіктерін ұсынады; 5) Structured Streaming event-time өңдеуді, кеш келген деректерді және watermarking-ті қолдайды."
            },
            {
                "text": "Structured Streaming қолданатын output режимдері қандай?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "complete, update, append",
                        "is_correct": True
                    },
                    {
                        "text": "full, incremental, snapshot",
                        "is_correct": False
                    },
                    {
                        "text": "streaming, batching, hybrid",
                        "is_correct": False
                    },
                    {
                        "text": "continuous, discrete, periodic",
                        "is_correct": False
                    }
                ]
            },
            {
                "text": "Spark Streaming-те watermarking не үшін қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Ескірген деректерді шектеу және құрылымдарды оңтайландыру үшін",
                        "is_correct": False
                    },
                    {
                        "text": "Деректер ағынының көлемін бақылау үшін",
                        "is_correct": False
                    },
                    {
                        "text": "Кеш келген деректермен жұмыс істеу және жадыны оңтайландыру үшін",
                        "is_correct": True
                    },
                    {
                        "text": "Деректерді шифрлау үшін қолданылатын қауіпсіздік әдісі",
                        "is_correct": False
                    }
                ]
            }
        ],
        "PySpark көмегімен MySQL-ге қосылу": [
            {
                "text": "PySpark-тан MySQL-ге қосылу конфигурациясын сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "PySpark-тан MySQL-ге қосылу конфигурациясы келесі параметрлерді қамтиды: 1) url - JDBC URL мекенжайы; 2) driver - JDBC драйвер класы; 3) dbtable - MySQL таблица атауы; 4) user және password - аутентификация деректері. Мысал: df = spark.read.format('jdbc').options(url='jdbc:mysql://localhost:3306/mydatabase', driver='com.mysql.cj.jdbc.Driver', dbtable='users', user='username', password='secretpassword').load()"
            },
            {
                "text": "PySpark және MySQL арасында деректерді қалай тасымалдауға болады?",
                "type": "open_ended",
                "correct_answer": "PySpark және MySQL арасында деректерді тасымалдау: 1) MySQL-ден оқу: spark.read.format('jdbc').options(параметрлер).load(); 2) MySQL-ге жазу: dataframe.write.format('jdbc').options(параметрлер).mode('append/overwrite').save(); 3) Партиция бойынша оқу: options параметрлерінде partitionColumn, lowerBound, upperBound, numPartitions қосу; 4) Сүзілген деректерді оқу: options параметрінде query немесе dbtable мен predicates көрсету."
            },
            {
                "text": "PySpark JDBC қосылымдарын масштабтау үшін қандай техникалар қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Қосылымдарды пулинг және деректерді партициялау арқылы оқу",
                        "is_correct": True
                    },
                    {
                        "text": "Барлық деректерді бір транзакцияда оқу",
                        "is_correct": False
                    },
                    {
                        "text": "Деректерді тек кэштен оқу",
                        "is_correct": False
                    },
                    {
                        "text": "MySQL-ді PySpark кластерінде жергілікті іске қосу",
                        "is_correct": False
                    }
                ]
            },
            {
                "text": "PySpark-та SQL сұрауын тікелей орындау үшін қандай функция қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "executeSQL()",
                        "is_correct": False
                    },
                    {
                        "text": "spark.sql()",
                        "is_correct": True
                    },
                    {
                        "text": "runQuery()",
                        "is_correct": False
                    },
                    {
                        "text": "connection.execute()",
                        "is_correct": False
                    }
                ]
            }
        ],
        "Airflow. Workflows": [
            {
                "text": "Airflow көмегімен workflow құру процесін сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "Airflow көмегімен workflow құру: 1) DAG объектісін құру (dag_id, schedule_interval, default_args параметрлерімен); 2) Операторларды анықтау (PythonOperator, BashOperator, SparkSubmitOperator және т.б.); 3) Тапсырмалар арасындағы тәуелділіктерді орнату (>> немесе set_upstream/set_downstream әдістері арқылы); 4) DAG файлын Airflow dags қалтасына орналастыру; 5) Airflow веб-интерфейсі арқылы DAG іске қосу және мониторинг жүргізу. Мысалы: with DAG('data_processing', schedule_interval='@daily') as dag: extract = BashOperator(task_id='extract', bash_command='python extract.py'); transform = PythonOperator(task_id='transform', python_callable=transform_function); load = BashOperator(task_id='load', bash_command='python load.py'); extract >> transform >> load"
            },
            {
                "text": "Apache Airflow-да DAG дегеніміз не және оның негізгі қасиеттерін сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "Apache Airflow-да DAG (Directed Acyclic Graph) - бұл тапсырмаларды (tasks) және олардың арасындағы тәуелділіктерді көрсететін бағытталған ациклдік граф. Негізгі қасиеттері: 1) dag_id - DAG-тің бірегей идентификаторы; 2) description - DAG сипаттамасы; 3) schedule_interval - DAG орындалу жиілігі (cron expression немесе timedelta); 4) start_date - DAG орындалуының басталу уақыты; 5) default_args - барлық тапсырмалар үшін әдепкі параметрлер; 6) catchup - өткізіп алынған орындауларды қуып жетеді ме; 7) max_active_runs - бір уақытта орындалатын DAG нұсқаларының максималды саны."
            },
            {
                "text": "Airflow-да бір тапсырма орындалғаннан кейін басқа тапсырманы орындау үшін қандай әдістер қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "first_task.execute_next(second_task)",
                        "is_correct": False
                    },
                    {
                        "text": "first_task >> second_task немесе second_task.set_upstream(first_task)",
                        "is_correct": True
                    },
                    {
                        "text": "first_task.forward_to(second_task)",
                        "is_correct": False
                    },
                    {
                        "text": "DAG.connect(first_task, second_task)",
                        "is_correct": False
                    }
                ]
            },
            {
                "text": "Airflow-дың sensor операторлары не үшін қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Желіні мониторинг жасау үшін",
                        "is_correct": False
                    },
                    {
                        "text": "Тек температура мен ылғалдылық деректерін жинау үшін",
                        "is_correct": False
                    },
                    {
                        "text": "Белгілі бір жағдайды күту (файлдың пайда болуы, мерзімнің жетуі) үшін",
                        "is_correct": True
                    },
                    {
                        "text": "Тек Airflow UI-де табло көрсету үшін",
                        "is_correct": False
                    }
                ]
            }
        ],
        "MLlib: Машиналық оқыту кітапханасы": [
            {
                "text": "MLlib-те машиналық оқыту жұмыс ағынының (ML workflow) негізгі кезеңдерін сипаттаңыз.",
                "type": "open_ended",
                "correct_answer": "MLlib-те машиналық оқыту жұмыс ағынының (ML workflow) негізгі кезеңдері: 1) Деректерді жүктеу (spark.read немесе textFile арқылы); 2) Ерекшеліктерді дайындау (VectorAssembler, StringIndexer, OneHotEncoder және т.б. трансформерлерді қолдану); 3) Деректерді оқыту және тест жиындарына бөлу (randomSplit әдісі); 4) Модельді таңдау және параметрлерді орнату (LogisticRegression, RandomForestClassifier және т.б.); 5) Pipeline құру; 6) Модельді оқыту (fit() әдісі); 7) Болжамдар жасау (transform() әдісі); 8) Модельді бағалау (BinaryClassificationEvaluator немесе MulticlassClassificationEvaluator); 9) Гиперпараметрлерді оңтайландыру (CrossValidator, ParamGridBuilder). Мысалы, pipeline = Pipeline(stages=[indexer, encoder, assembler, classifier]); model = pipeline.fit(trainData); predictions = model.transform(testData); evaluator.evaluate(predictions)"
            },
            {
                "text": "Spark ML Pipeline дегеніміз не және оның қандай артықшылықтары бар?",
                "type": "open_ended",
                "correct_answer": "Spark ML Pipeline - бұл машиналық оқыту жұмыс ағынын құру және орындауға арналған жоғары деңгейлі API. Артықшылықтары: 1) Деректерді дайындау, модельді құру, бағалау кезеңдерін біріктіру; 2) Бірнеше кезеңдерді қамтитын күрделі жұмыс ағындарын ұйымдастыру; 3) Модельдерді сақтау және жүктеу мүмкіндігі; 4) Параметрлерді оңтайландыру (GridSearch, CrossValidation); 5) Бір дәйекті жұмыс ағынында әртүрлі алгоритмдерді біріктіру; 6) Код құрылымын жақсарту және қайта қолдану. Мысалы, pipeline = Pipeline(stages=[tokenizer, hashingTF, lr]); pipelineModel = pipeline.fit(trainingData)"
            },
            {
                "text": "PySpark MLlib-те Cross Validation не үшін қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "Деректерді тазалау және дайындау",
                        "is_correct": False
                    },
                    {
                        "text": "Модельдің гиперпараметрлерін оңтайландыру және овerfitting-ті болдырмау",
                        "is_correct": True
                    },
                    {
                        "text": "Деректерді визуализациялау",
                        "is_correct": False
                    },
                    {
                        "text": "Модельді өндіріске енгізу",
                        "is_correct": False
                    }
                ]
            },
            {
                "text": "MLlib-те қандай функциялар ерекшеліктерді масштабтау үшін қолданылады?",
                "type": "multiple_choice",
                "choices": [
                    {
                        "text": "StandardScaler, MinMaxScaler, MaxAbsScaler, Normalizer",
                        "is_correct": True
                    },
                    {
                        "text": "StringScaler, NumericScaler, VectorScaler",
                        "is_correct": False
                    },
                    {
                        "text": "ColumnScaler, RowScaler, FullScaler",
                        "is_correct": False
                    },
                    {
                        "text": "LevelScaler, RatioScaler, ProportionScaler",
                        "is_correct": False
                    }
                ]
            }
        ],
        "Жарықтандыру және визуализация негіздері": [
            {
                "text": "Жарықтандырудың негізгі мақсаты қандай?",
                "type": "multiple_choice",
                "choices": [
                    {"text": "Файл көлемін азайту", "is_correct": False},
                    {"text": "Көріністі шынайы көрсету", "is_correct": True},
                    {"text": "Модель санын көбейту", "is_correct": False},
                    {"text": "Координаталарды өзгерту", "is_correct": False}
                ]
            },
            {
                "text": "Визуализация ұғымы нені білдіреді?",
                "type": "multiple_choice",
                "choices": [
                    {"text": "Объектіні салу", "is_correct": False},
                    {"text": "Түсті таңдау", "is_correct": False},
                    {"text": "Соңғы көріністі экранда бейнелеу", "is_correct": True},
                    {"text": "Геометриялық түрлендіру", "is_correct": False}
                ]
            },
            {
                "text": "3D графикадағы жарық көздерінің негізгі үш түрін атаңыз және олардың айырмашылығын түсіндіріңіз.",
                "type": "open_ended",
                "correct_answer": "1) Бағытталған жарық (Directional) - шексіз қашықтықтан параллель сәулелер ретінде түседі (күн сияқты); 2) Нүктелік жарық (Point) - бір нүктеден барлық бағытқа тарайды (шам сияқты); 3) Шашыраңқы жарық (Ambient) - бүкіл сахнаны біркелкі жарықтандырады."
            }
        ]
    }
    
    # Add more subject questions...
    
    # If we have predefined questions for this subject, use them
    if subject in realistic_questions and realistic_questions[subject]:
        # Use up to num_questions questions from our predefined set
        available_questions = realistic_questions[subject][:num_questions]
        
        for i, q_data in enumerate(available_questions, 1):
            question = {
                "id": f"q{i}",
                "text": q_data["text"],
                "type": q_data["type"],
                "points": random.choice([1, 2, 3]),
                "order": i,
                "explanation": q_data.get("explanation", "")
            }
            
            # Add choices for multiple choice questions
            if q_data["type"] == "multiple_choice":
                choices = []
                correct_index = None
                
                for j, choice in enumerate(q_data["choices"], 1):
                    choices.append({
                        "id": f"q{i}_c{j}",
                        "text": choice["text"],
                        "is_correct": choice["is_correct"]
                    })
                    if choice["is_correct"]:
                        correct_index = j
                
                question["choices"] = choices
            
            # Add correct answer for open-ended questions
            if q_data["type"] == "open_ended":
                question["correct_answer"] = q_data["correct_answer"]
            
            questions.append(question)
    else:
        # Fallback to generated questions if no predefined questions exist
        for i in range(1, num_questions + 1):
            # Alternate between multiple choice and open-ended questions
            question_type = "multiple_choice" if i % 2 == 0 else "open_ended"
            
            # Generate more natural question text
            if question_type == "multiple_choice":
                question_text = f"{subject} туралы төмендегі тұжырымдардың қайсысы дұрыс?"
            else:
                question_text = f"{subject} бойынша негізгі концепцияларды сипаттаңыз."
            
            question = {
                "id": f"q{i}",
                "text": question_text,
                "type": question_type,
                "points": random.choice([1, 2, 3]),
                "order": i
            }
            
            # Add choices for multiple choice questions
            if question_type == "multiple_choice":
                choices = []
                # Randomly select which choice will be correct
                correct_choice = random.randint(1, 4)
                
                for j in range(1, 5):
                    is_correct = (j == correct_choice)
                    choice_text = f"{subject} бойынша {j}-нұсқа" + (" (дұрыс)" if is_correct else "")
                    
                    choices.append({
                        "id": f"q{i}_c{j}",
                        "text": choice_text,
                        "is_correct": is_correct
                    })
                
                question["choices"] = choices
            else:
                # Add default correct answer for open-ended questions
                question["correct_answer"] = f"{subject} бойынша маңызды концепциялар мен принциптер: 1) Жүйелік архитектура; 2) Деректерді өңдеу; 3) Қауіпсіздік; 4) Масштабталу; 5) Өнімділік оңтайландыру."
            
            questions.append(question)
    
    return questions

def flush_database():
    """Flush database tables related to courses and questions."""
    print("Flushing existing course data...")
    
    # Delete data in reverse order of dependencies
    Choice.objects.all().delete()
    Question.objects.all().delete()
    Test.objects.all().delete()
    Lesson.objects.all().delete()
    Course.objects.all().delete()
    
    print("Database flushed successfully.")

def create_course_with_lessons():
    """Create a course and add lessons to it with detailed quiz data including correct answers."""
    # Create the course
    course, created = Course.objects.get_or_create(
        name="Растрлық және векторлық графика",
        defaults={
            'description': "Растрлық және векторлық графиканың теориялық негіздері, олардың айырмашылықтары және қолданылу салалары."
        }
    )
    
    if created:
        print(f"Created new course: {course.name}")
    else:
        print(f"Using existing course: {course.name}")
    
    # Define the lessons data
    lessons_data = [
        {
            "title": "Растрлық және векторлық графиканың негіздері",
            "short_description": "Пиксель VS Вектор",
            "description": """
<div class="lesson-content">
    <h3>1. Беттің жалпы мақсаты</h3>
    <p>Бұл тақырып бетінің негізгі мақсаты – білім алушыларға растрлық және векторлық графиканың теориялық негіздерін түсіндіру, олардың айырмашылықтарын айқындау және компьютерлік графикадағы қолданылу ерекшеліктерін меңгерту. Тақырып студенттің графикалық бейнелердің құрылымын түсінуіне, дұрыс форматты таңдай алуына және болашақта графикалық редакторлармен саналы жұмыс істеуіне негіз қалайды.</p>

    <h3>2. Міндетті мазмұн</h3>
    <h4>2.1 Теориялық мәтін</h4>
    <p>Компьютерлік графикада бейнелерді ұсынудың екі негізгі түрі бар: растрлық және векторлық графика. Растрлық графика нүктелерден (пиксельдерден) тұратын бейнелерді сипаттайды. Әрбір пиксельдің өзіне тән түсі мен орны болады, сондықтан растрлық бейнелер экранда немесе баспа өнімдерінде нақты және шынайы көрініс береді. Алайда растрлық кескіндерді үлкейткен кезде олардың сапасы төмендеп, бейне бұлыңғырланып кетуі мүмкін.</p>
    <p>Векторлық графика геометриялық объектілерге – сызықтар, қисықтар, көпбұрыштар және фигураларға негізделеді. Мұндай бейнелер математикалық формулалар арқылы сипатталатындықтан, оларды кез келген көлемге дейін үлкейту немесе кішірейту кезінде сапасы өзгермейді. Векторлық графика логотиптерді, схемаларды, диаграммаларды және техникалық сызбаларды жасауда кеңінен қолданылады.</p>
    <p>Растрлық және векторлық графиканың әрқайсысының өз артықшылықтары мен қолданылу салалары бар, сондықтан графикалық тапсырманы орындау барысында дұрыс графика түрін таңдау маңызды болып табылады.</p>

    <h4>2.2 Схемалар мен диаграммалар</h4>
    <div class="schema-container">
        <div class="schema-box raster">
            <h5>Растрлық графика</h5>
            <div class="pixel-grid"></div>
            <p>Пиксельдер торы</p>
        </div>
        <div class="schema-box vector">
            <h5>Векторлық графика</h5>
            <div class="vector-shape"></div>
            <p>Геометриялық объектілер</p>
        </div>
    </div>
    <p><i>Бұл схема растрлық бейненің пиксельдер жиынтығынан тұратынын, ал векторлық бейненің математикалық объектілер арқылы құрылатынын көрсетеді.</i></p>

    <h4>2.3 Салыстырмалы кесте</h4>
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Салыстыру параметрі</th>
                <th>Растрлық графика</th>
                <th>Векторлық графика</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Құрылымы</td>
                <td>Пиксельдер</td>
                <td>Геометриялық объектілер</td>
            </tr>
            <tr>
                <td>Масштабтау</td>
                <td>Сапа төмендейді</td>
                <td>Сапа сақталады</td>
            </tr>
            <tr>
                <td>Файл көлемі</td>
                <td>Үлкен болуы мүмкін</td>
                <td>Әдетте шағын</td>
            </tr>
            <tr>
                <td>Қолданылуы</td>
                <td>Фотосурет, сурет</td>
                <td>Логотип, схема</td>
            </tr>
        </tbody>
    </table>

    <h3>4. Қорытынды</h3>
    <p>Бұл тақырыпта растрлық және векторлық графиканың негізгі ұғымдары қарастырылды. Алынған білім келесі тақырыптарда графикалық редакторлармен жұмыс істеу барысында практикалық түрде қолданылады.</p>
</div>
""",
            "video_url": "https://www.youtube.com/embed/fSLIUGZL9Vo", 
            "hours": 1,
            "references": "НӘ: 1-4\nҚӘ: 1-4"
        },
        {
            "title": "Түстер модельдері және түспен жұмыс істеу принциптері",
            "short_description": "Түстер модельдері: RGB және CMYK",
            "description": """
<div class="lesson-content">
    <h3>1. Сабақтың мақсаты</h3>
    <p>Бұл тақырып бетінің негізгі мақсаты – білім алушыларға түстер модельдерінің теориялық негіздерін түсіндіру, түсті сандық ортада бейнелеу тәсілдерін көрсету және компьютерлік графикада түспен жұмыс істеудің базалық принциптерін меңгерту. Тақырып түстердің қалыптасу заңдылықтарын түсінуге, графикалық редакторларда түсті саналы түрде қолдануға және визуалды нәтижені басқаруға бағытталған.</p>

    <h3>2. Теориялық бөлім</h3>
    <p>Түс компьютерлік графиканың негізгі элементтерінің бірі болып табылады және ақпаратты визуалды түрде жеткізуде маңызды рөл атқарады. Сандық ортада түстер арнайы түстер модельдері арқылы сипатталады. Түстер моделі – түсті сандық түрде көрсетуге арналған жүйе болып табылады.</p>
    
    <p>Ең кең таралған түстер модельдерінің бірі – <strong>RGB моделі</strong>. Бұл модель қызыл (Red), жасыл (Green) және көк (Blue) түстердің әртүрлі комбинациялары арқылы түстерді қалыптастырады және экрандарда бейнелеу үшін қолданылады. RGB моделі аддитивті модель болып табылады, яғни негізгі түстерді біріктіру арқылы ашық түстер алынады.</p>
    
    <p>Баспа өнімдерінде жиі қолданылатын түстер моделі – <strong>CMYK</strong>. Бұл модель көгілдір (Cyan), күлгін (Magenta), сары (Yellow) және қара (Key) түстерге негізделген және субтрактивті принцип бойынша жұмыс істейді. CMYK моделі қағазға бояу жағу процесін сипаттайды.</p>

    <p>Түстер модельдерін дұрыс таңдау графикалық жұмыстың нәтижесіне тікелей әсер етеді. Сондықтан экранға арналған және баспаға арналған графиканы әзірлеуде сәйкес түстер моделін қолдану маңызды болып табылады.</p>

    <div class="color-schemas-container">
        <div class="schema-box">
            <h4>RGB (Аддитивті)</h4>
            <div class="circle-diagram rgb-diagram">
                <div class="c c1"></div>
                <div class="c c2"></div>
                <div class="c c3"></div>
                <div class="center-text">White</div>
            </div>
            <p class="schema-desc">“Бұл схема RGB моделінде түстердің жарық арқылы бірігуін көрсетеді.”</p>
        </div>
        <div class="schema-box">
            <h4>CMYK (Субтрактивті)</h4>
            <div class="circle-diagram cmyk-diagram">
                <div class="c c1"></div>
                <div class="c c2"></div>
                <div class="c c3"></div>
                <div class="center-text">Black</div>
            </div>
            <p class="schema-desc">“Бұл схема CMYK моделінде бояулардың сіңірілу принципін көрсетеді.”</p>
        </div>
    </div>

    <h3>3. Салыстырмалы кесте</h3>
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Салыстыру параметрі</th>
                <th>RGB моделі</th>
                <th>CMYK моделі</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Қолданылу саласы</td>
                <td>Экран, монитор</td>
                <td>Баспа өнімдері</td>
            </tr>
            <tr>
                <td>Түстердің қалыптасуы</td>
                <td>Жарық қосу (Аддитивті)</td>
                <td>Бояуды азайту (Субтрактивті)</td>
            </tr>
            <tr>
                <td>Негізгі түстер</td>
                <td>Қызыл, жасыл, көк</td>
                <td>Көгілдір, күлгін, сары, қара</td>
            </tr>
        </tbody>
    </table>

    <div class="practical-task">
        <h3>4. Практикалық тапсырма</h3>
        <p>Берілген сурет үшін қай түстер моделін қолдану тиімді екенін анықтаңыз және таңдауыңызды қысқаша негіздеңіз.</p>
    </div>

    <h3>5. Қорытынды</h3>
    <p>Түстер модельдерімен жұмыс істеу компьютерлік графикадағы маңызды дағдылардың бірі болып табылады. Бұл тақырыпта алынған білім келесі практикалық тапсырмаларда және графикалық редакторларда түспен жұмыс істеу барысында қолданылады.</p>
</div>

<style>
.color-schemas-container {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin: 30px 0;
    flex-wrap: wrap;
}
.schema-box {
    text-align: center;
    background: #f8fafc;
    padding: 20px;
    border-radius: 12px;
    flex: 1;
    min-width: 250px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.circle-diagram {
    width: 150px;
    height: 150px;
    position: relative;
    margin: 20px auto;
}
.circle-diagram .c {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    position: absolute;
}
.rgb-diagram .c { mix-blend-mode: screen; }
.rgb-diagram .c1 { background: red; top: 0; left: 30px; }
.rgb-diagram .c2 { background: #00ff00; bottom: 0; left: 0; }
.rgb-diagram .c3 { background: blue; bottom: 0; right: 0; }

.cmyk-diagram .c { mix-blend-mode: multiply; }
.cmyk-diagram .c1 { background: cyan; top: 0; left: 30px; }
.cmyk-diagram .c2 { background: magenta; bottom: 0; left: 0; }
.cmyk-diagram .c3 { background: yellow; bottom: 0; right: 0; }

.center-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 10px;
    font-weight: bold;
    color: #333;
    pointer-events: none;
    z-index: 10;
}
.schema-desc {
    font-size: 0.85rem;
    color: #64748b;
    font-style: italic;
    margin-top: 15px;
}
.practical-task {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    padding: 15px;
    margin: 20px 0;
    border-radius: 0 8px 8px 0;
}
</style>
""",
            "video_url": "https://www.youtube.com/embed/9hirYMZ7PQc",
            "hours": 1
        },
        {
            "title": "Геометриялық түрлендірулер және графикалық объектілер",
            "short_description": "Орын ауыстыру, масштабтау және айналдыру",
            "description": """
<div class="lesson-content">
    <h3>1. Беттің мақсаты</h3>
    <p>Бұл тақырып бетінің мақсаты – білім алушыларға графикалық объектілерді түрлендірудің негізгі геометриялық тәсілдерін түсіндіру және оларды компьютерлік графикада қолданудың теориялық негіздерін қалыптастыру. Тақырып графикалық объектінің кеңістіктегі орнын, өлшемін және бағытын өзгерту принциптерін меңгертуге бағытталады, сондай-ақ графикалық редакторларда орындалатын практикалық әрекеттердің теориялық негізін қалайды.</p>

    <h3>2. Теориялық бөлім</h3>
    <p>Геометриялық түрлендірулер компьютерлік графикадағы графикалық объектілермен жұмыс істеудің негізгі операцияларының бірі болып табылады. Түрлендірулер объектінің пішінін өзгертпей немесе өзгерте отырып, оның кеңістіктегі орнын, өлшемін және бағытын басқаруға мүмкіндік береді.</p>
    
    <p>Геометриялық түрлендірулердің негізгі түрлеріне <strong>орын ауыстыру, масштабтау және айналдыру</strong> жатады.</p>
    
    <ul>
        <li><strong>Орын ауыстыру</strong> объектіні координаталар жүйесінде белгілі бір бағытта жылжытуды білдіреді.</li>
        <li><strong>Масштабтау</strong> объектінің өлшемін үлкейту немесе кішірейтуге арналған түрлендіру болып табылады.</li>
        <li><strong>Айналдыру</strong> объектіні белгілі бір нүктенің немесе осьтің айналасында бұруды сипаттайды.</li>
    </ul>

    <div class="transform-schemas-container">
        <div class="schema-box">
            <h4>Орын ауыстыру (Translation)</h4>
            <div class="transform-diagram translation-diagram">
                <div class="obj original"></div>
                <div class="arrow">→</div>
                <div class="obj transformed"></div>
            </div>
            <p class="schema-desc">“Орын ауыстыру операциясын координаталар жүйесінде көрсететін схема.”</p>
        </div>
        <div class="schema-box">
            <h4>Масштабтау және айналдыру</h4>
            <div class="transform-diagram scale-rotate-diagram">
                <div class="obj original small"></div>
                <div class="arrow">⟳</div>
                <div class="obj transformed large rotated"></div>
            </div>
            <p class="schema-desc">“Масштабтау және айналдыру түрлендірулерін бейнелейтін диаграмма.”</p>
        </div>
    </div>

    <h3>3. Түрлендірулерді жүйелеу</h3>
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Түрлендіру түрі</th>
                <th>Сипаттамасы</th>
                <th>Қолданылу мақсаты</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Орын ауыстыру</td>
                <td>Объектіні жылжыту</td>
                <td>Орналасуды реттеу</td>
            </tr>
            <tr>
                <td>Масштабтау</td>
                <td>Өлшемді өзгерту</td>
                <td>Көлемді басқару</td>
            </tr>
            <tr>
                <td>Айналдыру</td>
                <td>Бағытын өзгерту</td>
                <td>Композиция құру</td>
            </tr>
        </tbody>
    </table>

    <div class="practical-task">
        <h3>4. Практикалық тапсырма</h3>
        <p>Берілген графикалық объектіге үш түрлі геометриялық түрлендіру қолданып, олардың нәтижесін салыстырыңыз.</p>
    </div>

    <h3>5. Қорытынды</h3>
    <p>Геометриялық түрлендірулер графикалық объектілерді басқарудың негізгі құралы болып табылады. Бұл тақырыпта алынған теориялық білім компьютерлік графикадағы барлық практикалық жұмыстардың негізін құрайды.</p>
</div>

<style>
.transform-schemas-container {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin: 30px 0;
}
.transform-diagram {
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    position: relative;
}
.transform-diagram .obj {
    width: 40px;
    height: 40px;
    border: 2px solid #2563eb;
    background: #dbeafe;
}
.original { opacity: 0.5; border-style: dashed; }
.transformed { opacity: 1; }
.large { transform: scale(1.5); }
.rotated { transform: rotate(45deg); }
.arrow { font-size: 24px; color: #64748b; }
</style>
""",
            "video_url": "https://www.youtube.com/embed/KiANJQnFFIA",
            "hours": 1
        },
        {
            "title": "Үшөлшемді графиканың негізгі ұғымдары",
            "short_description": "3D кеңістік, координаталар және камера",
            "description": """
<div class="lesson-content">
    <h3>1. Сабақтың мақсаты</h3>
    <p>Бұл тақырып бетінің негізгі мақсаты – білім алушыларға үшөлшемді графиканың теориялық негіздерін түсіндіру, кеңістіктік модельдеу ұғымдарын қалыптастыру және 3D объектілермен жұмыс істеудің базалық принциптерін меңгерту. Тақырып студенттердің кеңістіктік ойлауын дамытуға және компьютерлік графиканың келесі күрделі бөлімдерін игеруге дайындық жасауға бағытталған.</p>

    <h3>2. Теориялық бөлім</h3>
    <p>Үшөлшемді графика – объектілерді кеңістікте үш координата осі арқылы (X, Y, Z) бейнелеуге негізделген компьютерлік графика саласы болып табылады. Үшөлшемді графикада объектілер тек жазықтықта емес, тереңдік өлшемін ескере отырып сипатталады.</p>
    
    <p>Үшөлшемді модель – бұл кеңістіктегі объектінің сандық сипаттамасы. Ол геометриялық пішіндерден, нүктелерден (vertices), қабырғалардан (edges) және беттерден (faces) тұрады. Үшөлшемді модельдер нақты объектілерді немесе абстрактілі пішіндерді визуализациялау үшін қолданылады.</p>

    <p>Үшөлшемді графиканың негізгі ұғымдарына координаталар жүйесі, кеңістік, камера және көрініс жатады.</p>
    <ul>
        <li><strong>Координаталар жүйесі</strong> объектінің кеңістіктегі орнын анықтауға мүмкіндік береді.</li>
        <li><strong>Камера</strong> көріністің қай нүктеден және қандай бұрышпен бейнеленетінін белгілейді.</li>
        <li><strong>Көрініс</strong> объектінің экранда қалай көрсетілетінін сипаттайды.</li>
    </ul>

    <div class="threed-schemas-container">
        <div class="schema-box">
            <h4>3D Координаталар жүйесі</h4>
            <div class="threed-diagram coord-system">
                <div class="axis x">X</div>
                <div class="axis y">Y</div>
                <div class="axis z">Z</div>
            </div>
            <p class="schema-desc">“X, Y, Z осьтерінен тұратын үшөлшемді координаталар жүйесін көрсететін схема.”</p>
        </div>
        <div class="schema-box">
            <h4>Объектінің құрылымы</h4>
            <div class="threed-diagram obj-structure">
                <div class="cube-wire">
                    <div class="vertex v1"></div>
                    <div class="edge e1"></div>
                    <div class="face f1">Face</div>
                </div>
            </div>
            <p class="schema-desc">“Үшөлшемді объектінің нүкте–қабырға–бет құрылымын бейнелейтін диаграмма.”</p>
        </div>
    </div>

    <h3>3. Негізгі ұғымдарды жүйелеу</h3>
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Ұғым</th>
                <th>Сипаттамасы</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Үшөлшемді модель</td>
                <td>Кеңістіктегі объектінің сандық бейнесі</td>
            </tr>
            <tr>
                <td>Координаталар жүйесі</td>
                <td>Объектінің орнын анықтайтын жүйе</td>
            </tr>
            <tr>
                <td>Камера</td>
                <td>Көріністі бейнелеу нүктесі</td>
            </tr>
            <tr>
                <td>Көрініс</td>
                <td>Объектінің экранда көрсетілуі</td>
            </tr>
        </tbody>
    </table>

    <div class="practical-task">
        <h3>4. Практикалық тапсырма</h3>
        <p>Берілген үшөлшемді объектінің координаталар жүйесінде қалай орналасқанын сипаттаңыз және оның көрінісін сөзбен түсіндіріңіз.</p>
    </div>

    <h3>5. Қорытынды</h3>
    <p>Үшөлшемді графиканың негізгі ұғымдары графикалық модельдеу мен визуализацияның теориялық негізін құрайды. Бұл тақырыпта алынған білім келесі тақырыптарда күрделі үшөлшемді сахналармен жұмыс істеуге негіз болады.</p>
</div>

<style>
.threed-schemas-container {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin: 30px 0;
}
.threed-diagram {
    height: 150px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f1f5f9;
    border-radius: 8px;
    overflow: hidden;
}
.coord-system .axis {
    position: absolute;
    font-weight: bold;
    font-size: 12px;
}
.coord-system .x { width: 100px; height: 2px; background: red; right: 20px; }
.coord-system .y { height: 100px; width: 2px; background: green; top: 20px; }
.coord-system .z { width: 80px; height: 2px; background: blue; transform: rotate(45deg); }

.obj-structure .cube-wire {
    width: 60px;
    height: 60px;
    border: 2px solid #2563eb;
    position: relative;
    transform: rotateX(-20deg) rotateY(20deg);
}
.obj-structure .vertex {
    width: 6px;
    height: 6px;
    background: orange;
    border-radius: 50%;
    position: absolute;
    top: -3px;
    left: -3px;
}
.obj-structure .face {
    width: 100%;
    height: 100%;
    background: rgba(37, 99, 235, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 8px;
    color: #1e40af;
}
</style>
""",
            "video_url": "https://www.youtube.com/embed/TEAtmCYYKZA",
            "hours": 1
        },
        {
            "title": "Жарықтандыру және визуализация негіздері",
            "short_description": "Жарық көздері, көлеңке және рендеринг",
            "description": """
<div class="lesson-content">
    <h3>1. Беттің мақсаты</h3>
    <p>Бұл тақырып бетінің негізгі мақсаты – білім алушыларға үшөлшемді графикада жарықтандыру мен визуализацияның теориялық негіздерін түсіндіру, көріністің шынайылығын арттыруда жарықтың рөлін ашу және визуалды нәтижені басқарудың негізгі принциптерін меңгерту. Тақырып алдыңғы бөлімдерде қарастырылған үшөлшемді модельдеу ұғымдарын аяқтап, графикалық объектіні толыққанды визуалды өнім ретінде қабылдауға мүмкіндік береді.</p>

    <h3>2. Теориялық бөлім</h3>
    <p>Жарықтандыру – үшөлшемді графикадағы визуализация сапасын анықтайтын негізгі факторлардың бірі болып табылады. Жарық объектінің пішінін, көлемін және кеңістіктегі орнын айқындауға мүмкіндік береді. Дұрыс ұйымдастырылған жарық көріністің шынайылығын арттырып, графикалық объектінің визуалды қабылдануын жақсартады.</p>
    
    <p>Үшөлшемді графикада жарық көздерінің бірнеше негізгі түрі қолданылады:</p>
    <ul>
        <li><strong>Бағытталған жарық (Directional)</strong> – параллель сәулелер, күн жарығы сияқты.</li>
        <li><strong>Нүктелік жарық (Point)</strong> – бір нүктеден барлық бағытқа таралатын жарық.</li>
        <li><strong>Шашыраңқы жарық (Ambient)</strong> – сахнаның жалпы жарық деңгейін анықтайды.</li>
    </ul>

    <p>Визуализация (Рендеринг) – үшөлшемді сахнаны экранда бейнелеу процесі болып табылады. Бұл процесс модель, материал, жарық және камера параметрлерінің өзара байланысына негізделеді.</p>

    <div class="lighting-schemas-container">
        <div class="schema-box">
            <h4>Жарық көздерінің түрлері</h4>
            <div class="light-diagram type-diagram">
                <div class="light-emitter point"></div>
                <div class="light-emitter directional"></div>
            </div>
            <p class="schema-desc">“Жарық көздерінің түрлерін және олардың объектіге әсерін көрсететін схема.”</p>
        </div>
        <div class="schema-box">
            <h4>Жарық пен Көлеңке</h4>
            <div class="light-diagram shadow-diagram">
                <div class="light-source-icon">☀️</div>
                <div class="object-sphere"></div>
                <div class="cast-shadow"></div>
            </div>
            <p class="schema-desc">“Жарық пен көлеңкенің объект пішінін қалай айқындайтынын бейнелейтін диаграмма.”</p>
        </div>
    </div>

    <h3>3. Негізгі ұғымдарды жүйелеу</h3>
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Ұғым</th>
                <th>Сипаттамасы</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Жарық көзі</td>
                <td>Көріністі жарықтандыратын элемент</td>
            </tr>
            <tr>
                <td>Көлеңке</td>
                <td>Жарық түспеген аймақ</td>
            </tr>
            <tr>
                <td>Визуализация</td>
                <td>Көріністі экранда бейнелеу процесі</td>
            </tr>
            <tr>
                <td>Камера</td>
                <td>Көріністі бақылау нүктесі</td>
            </tr>
        </tbody>
    </table>

    <div class="practical-task">
        <h3>4. Практикалық тапсырма</h3>
        <p>Берілген үшөлшемді сахна үшін жарық көзін таңдап, оның көрініске әсерін сипаттаңыз.</p>
    </div>

    <h3>5. Қорытынды</h3>
    <p>Жарықтандыру және визуализация үшөлшемді графиканың соңғы нәтижесін қалыптастыратын маңызды кезең болып табылады. Бұл тақырыпта алынған білім графикалық жобаларды сапалы аяқтауға мүмкіндік береді.</p>
</div>

<style>
.lighting-schemas-container {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin: 30px 0;
}
.light-diagram {
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #1e293b;
    border-radius: 8px;
    position: relative;
    overflow: hidden;
}
.object-sphere {
    width: 60px;
    height: 60px;
    background: radial-gradient(circle at 30% 30%, #3b82f6, #1e3a8a);
    border-radius: 50%;
    z-index: 2;
}
.cast-shadow {
    position: absolute;
    bottom: 30px;
    right: 20px;
    width: 80px;
    height: 20px;
    background: rgba(0,0,0,0.5);
    border-radius: 50%;
    filter: blur(5px);
}
.light-source-icon {
    position: absolute;
    top: 20px;
    left: 20px;
    font-size: 24px;
}
</style>
""",
            "video_url": "https://www.youtube.com/embed/totgO02cv0k",
            "hours": 1
        }
    ]
    
    # Create lessons with detailed quiz data
    created_count = 0
    for i, lesson_data in enumerate(lessons_data, 1):
        # Create more detailed quiz data with actual questions
        num_questions = random.randint(3, 5)
        questions = create_quiz_questions(lesson_data["title"], lesson_data["title"], num_questions)
        
        quiz_data = {
            "title": f"Quiz for {lesson_data['title']}",
            "description": f"This quiz tests your knowledge on {lesson_data['title']}",
            "passing_score": 70,
            "time_limit_minutes": 15,
            "questions": questions,
            "version": "1.0",
            "status": "active"
        }
        
        # Create lesson or update if it exists
        lesson, lesson_created = Lesson.objects.update_or_create(
            course=course,
            title=lesson_data["title"],
            defaults={
                "video_url": lesson_data["video_url"],
                "description": lesson_data.get("description", ""),
                "short_description": lesson_data.get("short_description", ""),
                "quiz": quiz_data,
            }
        )
        
        if lesson_created:
            created_count += 1
            print(f"Created lesson {i}: {lesson.title}")
        else:
            print(f"Updated lesson {i}: {lesson.title}")
        
        # Also create a test for this lesson
        test, test_created = Test.objects.update_or_create(
            lesson=lesson,
            defaults={
                "title": f"Тест: {lesson.title}",
                "description": f"Бұл тест '{lesson.title}' бойынша білімді тексеруге арналған.",
                "passing_score": 70,
                "time_limit": 30
            }
        )
        
        if test_created:
            print(f"  Created test: {test.title}")
        else:
            print(f"  Updated test: {test.title}")
            # Delete existing questions if updating
            Question.objects.filter(test=test).delete()
        
        # Create questions for the test based on the quiz questions
        question_count = 0
        open_ended_count = 0
        
        for q_data in questions:
            question_type = QuestionType.MULTIPLE_CHOICE if q_data["type"] == "multiple_choice" else QuestionType.OPEN_ENDED
            
            # Prepare question parameters
            question_params = {
                "test": test,
                "text": q_data["text"],
                "question_type": question_type,
                "points": q_data["points"],
                "order": q_data["order"],
                "explanation": q_data.get("explanation", "")
            }
            
            # Add correct answer for open-ended questions
            if question_type == QuestionType.OPEN_ENDED:
                open_ended_count += 1
                # Use custom answer if available
                if "custom_answers" in lesson_data and f"open_ended_{open_ended_count}" in lesson_data["custom_answers"]:
                    question_params["correct_answer"] = lesson_data["custom_answers"][f"open_ended_{open_ended_count}"]
                else:
                    # Use the default correct answer from quiz data if available
                    question_params["correct_answer"] = q_data.get("correct_answer", "")
            
            question = Question.objects.create(**question_params)
            question_count += 1
            
            # Add choices for multiple choice questions
            if question_type == QuestionType.MULTIPLE_CHOICE and "choices" in q_data:
                for choice_data in q_data["choices"]:
                    Choice.objects.create(
                        question=question,
                        text=choice_data["text"],
                        is_correct=choice_data["is_correct"]
                    )
        
        print(f"  Created {question_count} questions for test: {test.title}")
    
    print(f"\nSummary: Created/Updated {created_count} lessons with detailed quiz data in course '{course.name}'")

def main():
    """Main function to run the population script."""
    # Always flush for this specific task to ensure clean state
    flush_database()
    
    create_course_with_lessons()
    
    # Verify open-ended questions have correct answers
    check_open_ended_questions()

def check_open_ended_questions():
    """Verify all open-ended questions have correct answers."""
    missing_answers = Question.objects.filter(
        question_type=QuestionType.OPEN_ENDED,
        correct_answer__isnull=True
    )
    
    if missing_answers.exists():
        print(f"\nWarning: Found {missing_answers.count()} open-ended questions missing correct answers:")
        for q in missing_answers:
            print(f"  - ID {q.id}: {q.text[:50]}...")
    else:
        open_ended_count = Question.objects.filter(question_type=QuestionType.OPEN_ENDED).count()
        print(f"\nSuccess: All {open_ended_count} open-ended questions have correct answers.")

if __name__ == "__main__":
    print("Starting comprehensive database population...")
    main()
    print("\nDatabase population completed successfully.")