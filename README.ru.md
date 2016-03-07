Лабороторная работа по предотвращению несанкционированного доступа на базе нейронной сети.

* Необходим интернет для получения данных для обучения ([см. tools](backend/nn/tools/__init__.py))
* Используется до 2GB оперативной памяти
* Используемыe ресуры указаны в [README.md](README.md)

## Запуск

### Клиент
Необходим nodejs
* `npm install -g gulp bower`
* `cd frontend && bash deploy.sh` 

### Сервер
*`pip install scapy` - установить скапи(под рутом)
*`sudo python scripts/sniff.py` - сниффинг пакетов
* [Установить PyBrain](http://pybrain.org/docs/index.html#installation)
* `cd backend && python setup.py`
* `python app.py` - с NSL-KDD сетом
* или `python app.py --v2` - с KDD99
* открыть localhost:8000

### Scapy
* `cd scripts`
* `sudo python sniff.py`
* Получившийся файл отправьте по форме на клиенте
