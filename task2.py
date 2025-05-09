"""
Task 2
Створіть скрипт для порівняння точного
підрахунку унікальних елементів та підрахунку за допомогою HyperLogLog.

"""

import json
import socket
from timeit import timeit
from datasketch import HyperLogLog


def load_data(filename: str) -> list[str]:
    """Load data from file"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []


def parse_log_line(line: str) -> str | None:
    """Parse log line and return IP address"""
    try:
        json_line = json.loads(line)
        return json_line.get("remote_addr")
    except json.JSONDecodeError:
        return None


def is_valid_ip(ip: str) -> bool:
    """Check if IP address is valid"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def parse_data(data: list[str]) -> list[str]:
    """Parse data and return list of IP addresses"""
    ip_list = []
    for line in data:
        ip = parse_log_line(line)
        if ip is not None and is_valid_ip(ip):
            ip_list.append(ip)
    return ip_list


def calculate_cardinality_set(data: list[str]) -> int:
    """Calculate cardinality using set"""
    return len(set(data))


def calculate_cardinality_hyperloglog(data: list[str]) -> int:
    """Calculate cardinality using HyperLogLog"""
    h = HyperLogLog(p=14)
    for d in data:
        h.update(d.encode("utf8"))
    return h.count()


def test_validated_line() -> None:
    """Test validated line"""
    assert parse_log_line("") is None
    print("\033[92m[OK] Test 1 passed\033[0m")
    assert parse_log_line('{"remote_addr": "127.0.0.1"}') == "127.0.0.1"
    print("\033[92m[OK] Test 2 passed\033[0m")
    assert parse_log_line('{"remote_addr": "127.0.0.1"') is None
    print("\033[92m[OK] Test 3 passed\033[0m")
    assert is_valid_ip(parse_log_line('{"remote_addr": "127.0.0.1"}')) is True
    print("\033[92m[OK] Test 4 passed\033[0m")
    assert is_valid_ip(parse_log_line('{"remote_addr": "927.0.0.1"}')) is False
    print("\033[92m[OK] Test 5 passed\033[0m")
    assert is_valid_ip(parse_log_line('{"remote_addr": "127..0.1"}')) is False
    print("\033[92m[OK] Test 6 passed\033[0m")


def run_test(
    data: list[str],
    count: int = 100,
) -> None:
    """Run function."""
    actual_cardinality = calculate_cardinality_set(data)
    estimated_cardinality = calculate_cardinality_hyperloglog(data)
    elapsed_time_set = timeit(lambda: calculate_cardinality_set(data), number=count)
    elapsed_time_hyperloglog = timeit(
        lambda: calculate_cardinality_hyperloglog(data), number=count
    )
    print("\n")
    print("Результати порівняння:")
    print("Метод".ljust(30), "Унікальні IP".ljust(20), "Час виконання (сек.)")
    print(
        "Точний підрахунок".ljust(30),
        f"{actual_cardinality:.6f}".ljust(20),
        f"{elapsed_time_set:.6f}",
    )
    print(
        "HyperLogLog".ljust(30),
        f"{estimated_cardinality:.6f}".ljust(20),
        f"{elapsed_time_hyperloglog:.6f}",
    )


def main():
    """Main function"""
    test_validated_line()
    data = parse_data(load_data("lms-stage-access.log"))
    run_test(data)


if __name__ == "__main__":
    main()
