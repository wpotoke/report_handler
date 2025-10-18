
### Примеры запуска

|EXAMPLE TESTS|EXAMPLE 1|EXAMPLE 2|
|-------------|---------|---------|
| <img width="1465" height="305" alt="изображение" src="https://github.com/user-attachments/assets/f478cda6-a478-4557-b370-16b95a7ba088" /> | <img width="1112" height="186" alt="изображение" src="https://github.com/user-attachments/assets/f4a87c80-e070-486f-9988-1afe6501eafb" /> | <img width="1320" height="207" alt="изображение" src="https://github.com/user-attachments/assets/fec4cc44-f747-4ebd-89c9-d9229083b1f9" /> |

### Как добавить отсчет
В завимисимости от того какого типа расширения ваш входной файл, нам нужно зайти в /core/reader.py и реализовать свой класс [Extfile]Reader(который будет читать входной файл) если новое расширение, после зайти в core/generator.py и создать [ReportNameExt]Generator(класс генератора будет генерировать новый тип отсчета), после создать класс [Type]Render если нужен новый тип вывода отсчета, подключите его в файле main.py и готово.
