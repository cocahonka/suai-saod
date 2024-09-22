from __future__ import annotations

from typing import Dict, List, Optional, Union

from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab2.stack.not_growable_stack import NotGrowableStack
from lab2.stack.stack import IStack, StackOverflowException
from lab2.stack.stack_linked_list import StackLinkedList


def linked_list() -> None:
    list: DoublyLinkedList[int] = DoublyLinkedList()
    end: str = "\n\n"

    list.add(3)
    list.insert(1, 4)
    list.add_in_head(2)
    list.add_in_head(1)
    list.add_in_tail(5)

    print(list, end=end)

    print(list[0], list[1], list[2])
    print(list.element_at(0), list.element_at(1), list.element_at(2), end=end)

    print(5 in list, 6 in list)
    print(list.contains(5), list.contains(6), end=end)

    print("[" + " -> ".join((str(x) for x in reversed(list))) + "]")
    list.reverse()
    print(list)
    list.reverse()
    print(list, end=end)


def is_valid_braces_sequence(braces: Union[List[str], str]) -> bool:
    braces_list: List[str] = list(braces) if isinstance(braces, str) else braces
    stack: IStack[str] = StackLinkedList()
    matches: Dict[str, str] = {
        ")": "(",
        "}": "{",
        "]": "[",
    }

    for brace in braces_list:
        if brace in ("(", "{", "["):
            stack.push(brace)
            continue

        peek: Optional[str] = stack.pop_or_none()
        if peek is None or matches.get(brace, None) != peek:
            return False

    return stack.is_empty()


def stack() -> None:
    stack: IStack[str] = StackLinkedList()
    stack.push("I")
    stack.push("A")
    stack.push("U")
    stack.push("S")

    while (el := stack.pop_or_none()) is not None:
        print(el, end=" ")
    print()

    not_growable_stack: IStack[str] = NotGrowableStack(StackLinkedList(), 2)
    try:
        not_growable_stack.push("I")
        not_growable_stack.push("A")
        not_growable_stack.push("U")
        not_growable_stack.push("S")
    except StackOverflowException as e:
        print(e)
    finally:
        while (el := not_growable_stack.pop_or_none()) is not None:
            print(el, end=" ")
        print()


def main() -> None:
    end: str = "\n\n"
    pfix: str = "=" * 20

    print(f"{pfix}Linked list demonstrate{pfix}")
    linked_list()
    print(end)

    print(f"{pfix}Stack demonstrate{pfix}")
    stack()
    print(end)


if __name__ == "__main__":
    main()
