# Python comprehensions

Comprehensions are a concise Python syntax for building a collection from an iterable in a single expression.

## List comprehension

A list comprehension builds a list. The form is `[expression for item in iterable if condition]`. For example, `[x * x for x in range(5)]` produces `[0, 1, 4, 9, 16]`. The `if` clause is optional and filters items: `[x for x in range(10) if x % 2 == 0]` keeps only even numbers.

## Dict and set comprehensions

A dict comprehension builds a dictionary: `{k: v for k, v in pairs}`. A set comprehension builds a set and removes duplicates: `{x % 3 for x in range(10)}`.

## Generator expression

A generator expression looks like a list comprehension but uses parentheses: `(x * x for x in range(5))`. It does not build the whole list in memory; it yields items lazily, one at a time. This is more memory-efficient for large or infinite sequences, and is preferred when you only iterate once, for example `sum(x * x for x in range(1000000))`.

## When to use which

Use a list comprehension when you need the full list, for example to index it or reuse it. Use a generator expression when you only pass through the data once and want to avoid holding it all in memory. Both are usually clearer and faster than an equivalent explicit `for` loop that appends to a list.
