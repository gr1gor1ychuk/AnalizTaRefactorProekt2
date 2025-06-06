# Система управління спортивним обладнанням

## Мета проекту
Розробка системи управління спортивним обладнанням з використанням сучасних патернів проектування для забезпечення гнучкості, масштабованості та легкості підтримки коду.

## Використані патерни проектування

### 1. Породжувальні патерни
#### Singleton (Одинак)
**Мета використання**: Забезпечення єдиної точки доступу до інвентарю обладнання.

**Реалізація**: `EquipmentInventory`
```python
class EquipmentInventory:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Переваги**:
- Гарантує єдину точку доступу до інвентарю
- Запобігає створенню множинних екземплярів
- Централізує управління станом інвентарю

### 2. Структурні патерни
#### Decorator (Декоратор)
**Мета використання**: Динамічне додавання функціональності до обладнання (гарантія, страхування, обслуговування).

**Реалізація**: `EquipmentDecorator` та його нащадки
```python
class EquipmentDecorator(Equipment):
    def __init__(self, equipment: Equipment):
        self._equipment = equipment
        
    def get_price(self) -> float:
        return self._equipment.get_price()
```

**Переваги**:
- Гнучке розширення функціональності
- Дотримання принципу відкритості/закритості
- Комбінування різних послуг

### 3. Поведінкові патерни
#### Chain of Responsibility (Ланцюг відповідальності)
**Мета використання**: Послідовна обробка замовлень через різні етапи валідації та виконання.

**Реалізація**: `OrderProcessor` та його нащадки
```python
class OrderProcessor(ABC):
    def set_next(self, processor: 'OrderProcessor'):
        self._next_processor = processor
        return processor

    def process(self, order: Order) -> bool:
        if self._validate(order):
            return self._next_processor.process(order) if self._next_processor else True
        return False
```

**Переваги**:
- Розділення відповідальності між обробниками
- Гнучка зміна послідовності обробки
- Легке додавання нових обробників

#### Strategy (Стратегія)
**Мета використання**: Реалізація різних стратегій ціноутворення.

**Реалізація**: `PricingStrategy` та його реалізації
```python
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, equipment: Equipment, quantity: int = 1, **kwargs) -> float:
        pass
```

**Переваги**:
- Гнучка зміна алгоритмів ціноутворення
- Ізоляція алгоритмів один від одного
- Легке додавання нових стратегій

## Принципи проектування SOLID

1. **Single Responsibility Principle (SRP)**
   - Кожен клас має єдину відповідальність
   - Приклад: `EquipmentSpecs` відповідає лише за характеристики обладнання

2. **Open/Closed Principle (OCP)**
   - Розширення функціональності без зміни існуючого коду
   - Приклад: Додавання нових декораторів обладнання

3. **Liskov Substitution Principle (LSP)**
   - Підкласи можуть замінювати базові класи
   - Приклад: Всі стратегії ціноутворення взаємозамінні

4. **Interface Segregation Principle (ISP)**
   - Клієнти не повинні залежати від інтерфейсів, які вони не використовують
   - Приклад: Розділення інтерфейсів для різних типів обробників замовлень

5. **Dependency Inversion Principle (DIP)**
   - Залежність від абстракцій, а не від конкретних реалізацій
   - Приклад: Використання абстрактних класів для стратегій та обробників

## Тестування
Проект включає понад 100+ модульних тестів, що покривають:
- Валідацію вхідних даних
- Коректність роботи патернів
- Граничні випадки
- Інтеграційні сценарії

Приклади тестів:
```python
def test_seasonal_pricing():
    strategy = SeasonalPricingStrategy(discount_percent=20.0)
    price = strategy.calculate_price(equipment, quantity=1)
    assert price == expected_price

def test_order_processing_chain():
    chain = OrderProcessorChain()
    result = chain.process_order(order)
    assert result == True
```

## Масштабованість та розширення
Проект спроектований для легкого розширення:
1. Додавання нових типів обладнання
2. Впровадження нових стратегій ціноутворення
3. Розширення ланцюга обробки замовлень
4. Додавання нових декораторів послуг

## Покриття коду
- Загальне покриття: 82%
- Покриття бізнес-логіки: >90%
- Покриття патернів проектування: >95%

## Структура проекту
```
src/
├── api/              # FastAPI endpoints
├── models/           # Domain models
├── patterns/         # Design patterns implementation
└── static/          # Frontend files

tests/
├── test_api.py
├── test_models.py
└── test_patterns.py
```

## Запуск проекту
```bash
# Встановлення залежностей
pip install -r requirements.txt

# Запуск сервера
uvicorn src.api.main:app --reload

# Запуск тестів
python -m pytest
```

## Висновки
Проект демонструє ефективне використання патернів проектування для створення гнучкої та масштабованої системи управління спортивним обладнанням. Використані патерни забезпечують:
- Чітку структуру коду
- Легкість модифікації та розширення
- Високу тестованість
- Відповідність принципам SOLID
