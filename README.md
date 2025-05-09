# goit-algo2-hw-05

## Task 1

### Description
Test password uniqueness using Bloom Filter

### Input
- Bloom Filter
- List of new passwords to check (strings)

### Output
- Dictionary with password and its status ("вже використаний" or "унікальний")

### Example

```python
existing_passwords = ["password123", "admin123", "qwerty123"]
new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
results = check_password_uniqueness(bloom, new_passwords_to_check)
assert results == {
    "password123": "вже використаний",
    "newpassword": "унікальний",
    "admin123": "вже використаний",
    "guest": "унікальний",
}
```

## Task 2

### Description
Estimate the number of unique IP addresses in a log file using HyperLogLog

### Input
- Log file path

### Output
- Estimated number of unique IP addresses
- Execution time

### Example

```python
data = parse_data(load_data("lms-stage-access.log"))
run_test(data)
```

```python
Результати порівняння:
Метод                          Унікальні IP         Час виконання (сек.)
Точний підрахунок              28                   0.023775
HyperLogLog                    28.023953075428718   3.711224
```
