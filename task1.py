"""
Task 1
Створіть функцію для перевірки унікальності паролів
 за допомогою фільтра Блума. Ця функція має визначати,
  чи використовувався пароль раніше,
  без необхідності зберігати самі паролі.
"""

from mmh3 import hash as mmh3_hash


class BloomFilter:
    """Bloom Filter implementation"""

    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        """Add item to the bloom filter"""
        for i in range(self.num_hashes):
            index = mmh3_hash(item + str(i)) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        """Check if item is in the bloom filter"""
        for i in range(self.num_hashes):
            index = mmh3_hash(item + str(i)) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(
    bloom_filter: BloomFilter, passwords: list[str]
) -> dict[str, str]:
    """Check if passwords are unique"""
    for pwd in passwords:
        if pwd is None:
            raise ValueError("All passwords must be non-None")
        if pwd == "":
            raise ValueError("All passwords must be a non-empty strings")
        if not isinstance(pwd, str):
            raise ValueError("All passwords must be strings")
    check_results = {}
    for pwd in passwords:
        if bloom_filter.contains(pwd):
            check_results[pwd] = "вже використаний"
        else:
            check_results[pwd] = "унікальний"
    return check_results


def test_check_password_uniqueness():
    """Test check_password_uniqueness function"""
    bloom = BloomFilter(size=1000, num_hashes=3)
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)
    assert results == {
        "password123": "вже використаний",
        "newpassword": "унікальний",
        "admin123": "вже використаний",
        "guest": "унікальний",
    }
    print("\033[92m[OK] Test 1 passed\033[0m")
    try:
        check_password_uniqueness(bloom, [None])
    except ValueError as e:
        assert str(e) == "All passwords must be non-None"
        print("\033[92m[OK] Test 2 passed\033[0m")
    try:
        check_password_uniqueness(bloom, [""])
    except ValueError as e:
        assert str(e) == "All passwords must be a non-empty strings"
        print("\033[92m[OK] Test 3 passed\033[0m")
    try:
        check_password_uniqueness(bloom, [123])
    except ValueError as e:
        assert str(e) == "All passwords must be strings"
        print("\033[92m[OK] Test 4 passed\033[0m")


def main():
    """Main function"""
    # run test function
    test_check_password_uniqueness()

    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")


if __name__ == "__main__":
    main()
