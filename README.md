## Основной стек технологий

- Python 3.7

- PostgreSQL 10.6

- Django ~= 2.2

- Django Rest Framework ~= 3.8.2

## Настройка локальной среды разработки на примере Ubuntu 18.04

##### Обновление системы:

```bash
sudo sh -c "apt -y update;apt -y dist-upgrade;apt -y autoremove;apt -y autoclean"
```

##### Установка системных зависимостей:
```bash
sudo apt install python3.7 python3.7-venv postgresql postgis redis-server postfix
```

##### Настройка директории var

В директорию var складывается вся статика, медиа данные, так же в ней располагается виртуальное окружение 
, и логи сторонних сервисов, которые работают с проектом. 

Создаем все необходимые директории, в корне проекта выполняем:
```bash
mkdir var && cd var && mkdir static && mkdir media && mkdir beat && python3.7 -m venv venv && cd ..
```

##### Установка python зависимостей:

Находясь в корне проекта активируйте виртуальное окружение, созданное на прошлом шаге:
```bash
. var/venv/bin/activate
```

Далее устанавливаем зависимости:
```bash
pip install -Ur freeze.txt
```

##### Создание файла с локальными настройками проекта:
```bash
cp src/myagent_backend/settings/local.example.py src/myagent_backend/settings/local.py
```

При необходимости отридоктируйте файл local.py:
- Для отправки почты необходимо задать параметры SMTP.

##### Создание базы данных:
Название базы данных, пользователя и пароль взяты из файла local.py, который был создан на прошлом шаге.
```
sudo -u postgres psql
CREATE DATABASE myagent_backend;
CREATE USER myagent_backend WITH password 'myagent_backend';
GRANT ALL PRIVILEGES ON DATABASE myagent_backend TO myagent_backend;
```

Далее перейдите из корня проекта в директорию src, и выполните миграции:
```
./manage.py migrate
```

##### Запуск Celery:
Celery используется для отправки e-mail и для прочих фоновых задач.

В директории blog_backend/src запускаем celery следующим образом:

```
path_to_project/var/venv/bin/celery -A blog_backend worker --beat -s path_to_project/var/beat/celerybeat-schedule --logfile=path_to_project/var/beat/beat.log --pidfile=path_to_project/var/beat/beat.pid -l info
```