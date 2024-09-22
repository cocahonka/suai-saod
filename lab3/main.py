from random import randint
from typing import Final, List

from lab3.models.number import Number
from lab3.models.student import Student
from lab3.serializers.ordered_binary_tree_serializer import OrderedBinaryTreeSerializer
from lab3.trees.avl_tree import AVLTree
from lab3.trees.ordered_binary_tree import IOrderedBinaryTree, TraversalType
from lab3.trees.ternary_trie import TernaryTrie, TraverseType
from lab3.trees.trie import ITrie


def _fill_trie_with_random_elements(trie: ITrie[str, int], n: int, word_len: int) -> None:
    def _rand_string(n: int) -> str:
        return "".join(chr(randint(97, 122)) for _ in range(word_len))

    for _ in range(n):
        trie.put(_rand_string(10), randint(0, n))


def ternary_trie() -> None:
    end: Final[str] = "\n\n"
    trie: Final[ITrie[str, int]] = TernaryTrie()
    trie.put("she", 0)
    trie.put("sells", 1)
    trie.put("sea", 2)
    trie.put("shells", 3)
    trie.put("by", 4)
    trie.put("the", 5)
    trie.put("sea", 6)
    trie.put("shore", 7)

    print(f"trie = {trie}")
    print(f"elements count = {len(trie)}", end=end)

    print(f"trie.get('she') = {trie.get('she')}")
    print(f"trie.get('sells') = {trie.get('sells')}")
    print(f"trie.get('sea') = {trie.get('sea')}")
    print(f"trie.get_or_none('shell') = {trie.get_or_none('shell')}", end=end)

    print(f"trie.contains('she') = {trie.contains('she')}")
    print(f"trie.contains('sell') = {trie.contains('sell')}", end=end)

    print(f"trie.keys_with_prefix('sh') = {list(trie.keys_with_prefix('sh'))}")
    print(f"trie.keys_with_prefix('sea') = {list(trie.keys_with_prefix('sea'))}", end=end)

    print(f"trie.longest_prefix_of('shell') = {trie.longest_prefix_of('shell')}")
    print(f"trie.longest_prefix_of('bytheking') = {trie.longest_prefix_of('bytheking')}")
    print(f"trie.longest_prefix_of('shore') = {trie.longest_prefix_of('shore')}", end=end)

    print("trie traversal:")
    print("in order:")
    trie.traverse(lambda key, value: print(f"{key}: {value}", end=" "))
    print(f"{end}pre order:")
    trie.traverse(lambda key, value: print(f"{key}: {value}", end=" "), TraverseType.PRE_ORDER)
    print(f"{end}post order:")
    trie.traverse(lambda key, value: print(f"{key}: {value}", end=" "), TraverseType.POST_ORDER)
    print(end=end)

    trie.delete("she")
    trie.delete("sells")
    trie.delete("sea")
    trie.delete("shells")
    trie.delete("by")

    print(f"trie after deletion = {trie}")

    new_trie: Final[ITrie[str, int]] = TernaryTrie()
    new_trie.put("she", 0)
    new_trie.put("sells", 1)
    new_trie.put("sea", 2)
    new_trie.put("shells", 3)
    new_trie.put("by", 4)

    trie.merge(new_trie)

    print(f"trie after merge = {trie}", end=end)

    number_tree: Final[ITrie[Number, str]] = TernaryTrie()
    number_tree.put(Number(12), "value")
    number_tree.put(Number(123), "apple")
    number_tree.put(Number(1234), "orange")
    number_tree.put(Number(457), "banana")

    print(f"number_tree = {number_tree}")

    print(
        f"number_tree.keys_with_prefix(Number(12)) = {list(number_tree.keys_with_prefix(Number(12)))}",
        end=end,
    )

    trie.clear()
    _fill_trie_with_random_elements(trie, 100, 3)
    print(f"tree after filling with 100 random elements = {trie}")
    print(f"tree contains 100 elements: {len(trie) == 100}")
    print(f"prefix 'a' keys: {list(trie.keys_with_prefix('a'))}")


def avl_tree() -> None:
    end: Final[str] = "\n\n"
    tree: Final[IOrderedBinaryTree[Student]] = AVLTree()
    students: Final[List[Student]] = [
        Student("Мясников Иван Олегович", "4314", 2, 19, 4.7),
        Student("Лодыгина Полина Юрьевна", "3236", 3, 20, 4.88),
        Student("Горелов Марк Андреевич", "3236", 3, 20, 4.6),
        Student("Егоров Егор Егорович ", "1111", 1, 18, 4.1),
        Student("Сидоров Сидор Сидорович", "2222", 2, 19, 4.1),  # not be inserted
        Student("Петров Петр Петрович", "3333", 3, 20, 4.2),
        Student("Иванов Иван Иванович", "4444", 4, 21, 3.2),
        Student("Сергеев Сергей Сергеевич", "5555", 5, 22, 4.7),  # not be inserted
        Student("Александров Александр Александрович", "6666", 6, 23, 3.3),
        Student("Андреев Андрей Андреевич", "7777", 7, 24, 3.4),
        Student("Алексеев Алексей Алексеевич", "8888", 8, 25, 3.43),
        Student("Владимиров Владимир Владимирович", "9999", 9, 26, 2.5),
    ]

    assert len(students) == 12
    print(f"length of students: {len(students)}")

    for student in students:
        tree.insert(student)

    assert len(tree) == 10
    assert students[0] in tree
    assert tree.contains(students[7])  # actually yes, because of the same average grade
    assert Student("", "", 0, 0, 4.7) in tree
    assert Student("", "", 0, 0, 0.0) not in tree

    print(f"length of tree: {len(tree)}")
    print(tree, end=end)

    min_grade_student: Student = tree.find_min()
    print(f"max grade: {tree.find_max()}")
    print(f"min grade: {min_grade_student}", end=end)

    tree.delete(min_grade_student)
    min_grade_student = tree.find_min()
    print(f"min grade after delete: {min_grade_student}")
    print(f"tree after delete\n{tree}", end=end)

    tree.delete(min_grade_student)  # left rotate
    min_grade_student = tree.find_min()
    print(f"min grade after delete 2: {min_grade_student}")
    print(f"tree after delete 2 (left rotated)\n{tree}", end=end)

    print(f"in order traversal")
    for student in tree.generator(TraversalType.IN_ORDER):
        print(student)
    print(end=end)

    print(f"pre order traversal")
    for student in tree.generator(TraversalType.PRE_ORDER):
        print(student)
    print(end=end)

    print(f"post order traversal")
    for student in tree.generator(TraversalType.POST_ORDER):
        print(student)
    print(end=end)

    OrderedBinaryTreeSerializer.save_tree_to_file(tree, "students.json")
    tree.clear()
    print("tree after clear")
    print(tree, end=end)

    OrderedBinaryTreeSerializer.load_tree_from_file(tree, "students.json", Student)
    print("tree after load from file")
    print(tree, end=end)


def main() -> None:
    end: str = "\n\n"
    pfix: str = "=" * 20

    print(f"{pfix}AVL tree demonstrate{pfix}")
    avl_tree()
    print(end)

    print(f"{pfix}Ternary trie demonstrate{pfix}")
    ternary_trie()
    print(end)


if __name__ == "__main__":
    main()
