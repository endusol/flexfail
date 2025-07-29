# flexfail

[![PyPi](https://img.shields.io/badge/pypi-%23ececec.svg?logo=pypi)](https://pypi.org/project/flexfail/)

[![Tests](https://github.com/endusol/flexfail/actions/workflows/publish-pypi.yaml/badge.svg)](https://github.com/endusol/flexfail/actions/workflows/publish-pypi.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/endusol/flexfail?tab=MIT-1-ov-file)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

**Flexible failures collector with different collecting strategies.**

`flexfail` provides a consistent and reusable way to collect, and handle failures.
Useful in data processing, form validation, and other contexts where soft-failing logic is needed.

---

## Justification

Why? Imagine you're processing a batch of data sent from a user and want to return a meaningful error description
if something goes wrong. Suppose the data contains 3 different errors in separate places. In a naive implementation,
you might return only one error per request. This would force the user to resubmit the request multiple times
to fix everything.

This library aims to make error collection simpler, clearer, and more flexible.

It allows you to collect **all errors in the data at once**, if needed - or just return the **first encountered error**.
You may even choose to **skip invalid values silently**. This behavior is controlled by **predefined error collection
strategies** (see examples below).

Moreover, in our example, user may choose what strategy is more suitable for them.

---

## Installation

```shell
pip install flexfail
```

---

## Usage approaches

Below are examples on how to use the `flexfail` using different approaches.

### Imperative (with context protocol)

```python
from flexfail import ErrorCollector, ErrorCollectorStrategy


data = [10, 20, -30, -44, 50, 'spam']
collector = ErrorCollector(ErrorCollectorStrategy.try_all)

for value in data:
    is_number = isinstance(value, (int, float))
    with collector:  # Just use context to collect errors. As shown here.
        assert is_number, f'Value `{value}` is not a number!'
        assert value >= 0, f'Value `{value}` is below zero!'
    with collector:  # And here.
        if is_number:
            assert value % 10 == 0, f'Value `{value}` is not divisible by 10!'

print(f'Collected {len(collector.errors)} errors:')
for err in collector.errors:
    print(err.data)
```

Results into:

```txt
Collected 4 errors:
Value `-30` is below zero!
Value `-44` is below zero!
Value `-44` is not times 10!
Value `spam` is not a number!
```

### Declarative (with decorators)

```python
from flexfail import ErrorCollector, ErrorCollectorStrategy


error_collector = ErrorCollector(ErrorCollectorStrategy.try_all)


@error_collector  # Just decorate callables with a collector object. As shown here.
def check_positive_number(value):
    assert isinstance(value, (int, float)), f'Value `{value}` is not a number!'
    assert value >= 0, f'Value `{value}` is below zero!'


@error_collector  # And here.
def check_divisible_by_10(value):
    if isinstance(value, (int, float)):
        assert value % 10 == 0, f'Value `{value}` is not divisible by 10!'


data = [10, 20, -30, -44, 50, 'spam']
for value in data:
    check_positive_number(value)
    check_divisible_by_10(value)

print(f'Collected {len(error_collector.errors)} errors:')
for err in error_collector.errors:
    print(err.data)
```

Results into:

```txt
Collected 4 errors:
Value `-30` is below zero!
Value `-44` is below zero!
Value `-44` is not times 10!
Value `spam` is not a number!
```

## Strategies overview

Below is a simple examples of how `flexfail` collects errors using different strategies.

### Strategy `skip`

Force bypass all the errors and not even collect them.

```python
from flexfail import ErrorCollector, ErrorCollectorStrategy
from flexfail.exceptions import FailFastException


error_collector = ErrorCollector(ErrorCollectorStrategy.skip)


@error_collector
def process(value):
    assert isinstance(value, (int, float)), f'Value `{value}` is not a number!'
    assert _ >= 0,  f'Value `{value}` is below zero!'
    print(f'Value `{value}` was successfully processed!')
    return value

data = [10, 20, -30, -44, 50, 'spam']
processed_data = []
try:
    for _ in data:
        processed_value = process(_)
        if processed_value:
            processed_data.append(processed_value)
except FailFastException:
    pass


print(f'Collected {len(error_collector.errors)} errors:')
for _ in error_collector.errors:
    print(_.data)
print(f'Processed data: {processed_data}')
```

Results into:

```txt
Value `10` was successfully processed!
Value `20` was successfully processed!
Value `50` was successfully processed!
Collected 0 errors:
Processed data: [10, 20, 50]
```

### Strategy `fail_fast`

Raise on first error occurs and collect only it.

Replace strategy from previous example to `ErrorCollectorStrategy.fail_fast`.
The same example with new strategy results into:

```txt
Value `10` was successfully processed!
Value `20` was successfully processed!
Collected 1 errors:
Value `-30` is below zero!
Processed data: [10, 20]
```

### Strategy `try_all`

Collect all the errors.

Replace strategy from previous example to `ErrorCollectorStrategy.try_all`.
The same example with new strategy results into:

```txt
Value `10` was successfully processed!
Value `20` was successfully processed!
Value `50` was successfully processed!
Collected 3 errors:
Value `-30` is below zero!
Value `-44` is below zero!
Value `spam` is not a number!
Processed data: [10, 20, 50]
```

## Autowrap

Please, note, by default collectors wraps any caught exception into the
`flexfail.exceptions.FlexFailException` as the `data` property.

If you want to disable this behavior, just set `autowrap` to `False` on collector initialise:

```python
from flexfail import ErrorCollector, ErrorCollectorStrategy

collector = ErrorCollector(strategy=ErrorCollectorStrategy.skip, autowrap=False)
```

This will lead to only `FlexFailException` is caught and any other exceptions are raised as usual.

---

## Would like to support?

![Github-sponsors](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA)
![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)
![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)

