TEXT_START = '''добро пожаловать в чат виртуального консультанта РГЭУ(РИНХ)!

Меня зовут NeuronLSTM, и я твой виртуальный помощник, созданный специально для того, чтобы помочь тебе найти ответы на все вопросы, связанные с поступлением в вуз.

Не стесняйся задавать вопросы – я здесь для того, чтобы помочь тебе!'''

TEXT_FEEDBACK = '''Спасибо за обратную связь. Благодаря вам, я стану лучше!❤️'''
TEXT_PERMISSION_ERROR = '''Вы не обладаете правами администратора для этой команды'''
TEXT_ADMIN_HELP = '''
Основные команды для работы с нейросетью и датасетом


/showquestions <дата начала> <дата окончания> <реакция на ответ нейросети>	Выводит вопросы абитуриентов с положительной/отрицательной оценкой за определенный период времени
/showtags Выводит все значения тем из датасета
/showpatterns <тема> Выводит все значения шаблонов по теме вопросов из датасета
/showresponses <тема> Выводит все значения ответов по теме из датасета

/trainingnn	Переобучает нейросеть

/addintent <тема> Добавляет тему с пустыми шаблонами вопросов и ответами на вопросы
/delintent <тема> Удаляет тему с пустыми шаблонами вопросов и ответами на вопросы
/editintent <тема> <новое наименование темы> Изменяет тему  с пустыми шаблонами вопросов и ответами на вопросы

/addpattern <тема> <вопрос>	Добавляет шаблоны вопросов для темы
/delpattern <тема> <вопрос>	Удаляет шаблоны вопросов для темы

/addresponse <тема> <ответ> Добавляет ответы для темы
/delresponse <тема> <ответ> Удаляет ответы для темы

/help Выводит список всех команд


Основные команды для работы с правами администратора


/addadmin <ник в Telegram> <номер телефона> <электронная почта> <имя> <фамилия> <отчество>	Добавляет администратора в БД
/deladmin <ник в Telegram>	Удаляет администратора из БД


/help
'''