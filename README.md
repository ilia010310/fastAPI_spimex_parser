# Микросервисное приложение: API для данных собранных с spimex.com


### ссылка на <a href=https://spimex.com/markets/oil_products/trades/results/>сайт</a>
### ccылка на <a href="https://github.com/ilia010310/async_parser_spimex">асинхронный парсер</a>

---

#### Функции для реализации: *
-   get_last_trading_dates – список дат последних торговых дней (фильтрация по кол-ву последних торговых дней).

- get_dynamics – список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date).
- get_trading_results – список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)


* Какие параметры должны быть обязательные, а какие нет, необходимо определить самостоятельно и обосновать.
* Необходимо организовать кэширование запросов (Redis) таким образом, чтобы они хранились до 14:11, а после происходил сброс всего кэша.
