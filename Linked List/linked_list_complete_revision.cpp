/*
LINKED LIST — COMPLETE REVISION CODEBOOK (C++17)
================================================
Converted from the supplied Python revision file.

Coverage:
  1. Complexity cheat sheet
  2. Singly linked list + CRUD
  3. Core pointer algorithms
  4. Cycle detection / entry / length / removal
  5. Palindrome, duplicates, rotation, sorting, reorder
  6. Doubly linked list
  7. Circular singly linked list
  8. Generic node-level helpers
  9. Merge two / K sorted lists
 10. Intersection
 11. Advanced interview patterns:
     pair swap, k-group reversal, delete-known-node, add numbers,
     partition, odd-even, zero-sum removal, random-pointer copy,
     multilevel DLL flattening, LRU cache
 12. Construction helpers, tests, placement checklist

Build:
  g++ -std=c++17 -O2 -Wall -Wextra linked_list_complete_revision.cpp -o linked_list

Run tests:
  g++ -std=c++17 -O2 -Wall -Wextra -DRUN_REVISION_TESTS linked_list_complete_revision.cpp -o linked_list_tests
  ./linked_list_tests

Ownership note:
  These educational raw-pointer implementations allocate nodes with new.
  For production code, prefer standard containers or use smart pointers and
  carefully define ownership semantics. Algorithms that rewire lists mutate
  the input lists.
*/

#include <algorithm>
#include <cassert>
#include <cstddef>
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <stdexcept>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using namespace std;

/*
COMPLEXITY CHEAT SHEET
----------------------
Singly list:
  index access/search O(n); prepend O(1); append O(1) with tail;
  delete head O(1); delete tail O(n) generally; reverse O(n);
  middle/cycle detection O(n) time, O(1) extra space.
Doubly list:
  index access/search O(n); prepend/append O(1) with endpoints;
  delete known node O(1); reverse O(n).
Circular list:
  traversal/search O(n); insert/delete after a known node O(1).
Patterns:
  merge two sorted lists O(n+m); merge K lists O(N log K);
  linked-list merge sort O(n log n); Floyd cycle methods O(n), O(1).
*/

// ============================================================
// 1. SINGLY LINKED LIST
// ============================================================

struct SinglyNode {
    int value;
    SinglyNode* next;

    explicit SinglyNode(int value) : value(value), next(nullptr) {}
};

// Forward declarations used by the list class below.
SinglyNode* reverseNodes(SinglyNode* head);
SinglyNode* reverseNodesRecursive(SinglyNode* head);
SinglyNode* mergeSortNodes(SinglyNode* head);
bool detectCycle(SinglyNode* head);
SinglyNode* findCycleEntry(SinglyNode* head);
size_t linkedCycleLength(SinglyNode* head);

class SinglyLinkedList {
public:
    SinglyNode* head = nullptr;
    SinglyNode* tail = nullptr;
    size_t size = 0;

    SinglyLinkedList() = default;

    explicit SinglyLinkedList(const vector<int>& values) {
        for (int value : values) append(value);
    }

    // Disable shallow copying; use clone() or node-level helpers when needed.
    SinglyLinkedList(const SinglyLinkedList&) = delete;
    SinglyLinkedList& operator=(const SinglyLinkedList&) = delete;

    ~SinglyLinkedList() { clear(); }

    vector<int> toVector(size_t limit = numeric_limits<size_t>::max()) const {
        vector<int> result;
        const SinglyNode* current = head;
        size_t count = 0;
        while (current && count < limit) {
            result.push_back(current->value);
            current = current->next;
            ++count;
        }
        return result;
    }

    void display() const {
        const SinglyNode* current = head;
        while (current) {
            cout << current->value << " -> ";
            current = current->next;
        }
        cout << "nullptr\n";
    }

    SinglyNode* prepend(int value) {
        auto* node = new SinglyNode(value);
        node->next = head;
        head = node;
        if (!tail) tail = node;
        ++size;
        return node;
    }

    SinglyNode* append(int value) {
        auto* node = new SinglyNode(value);
        if (!head) {
            head = tail = node;
        } else {
            tail->next = node;
            tail = node;
        }
        ++size;
        return node;
    }

    SinglyNode* insertAt(size_t index, int value) {
        if (index > size) throw out_of_range("Index out of range");
        if (index == 0) return prepend(value);
        if (index == size) return append(value);

        SinglyNode* previous = head;
        for (size_t i = 0; i < index - 1; ++i) previous = previous->next;

        auto* node = new SinglyNode(value);
        node->next = previous->next;
        previous->next = node;
        ++size;
        return node;
    }

    int get(size_t index) const {
        if (index >= size) throw out_of_range("Index out of range");
        const SinglyNode* current = head;
        for (size_t i = 0; i < index; ++i) current = current->next;
        return current->value;
    }

    int find(int value) const {
        const SinglyNode* current = head;
        int index = 0;
        while (current) {
            if (current->value == value) return index;
            current = current->next;
            ++index;
        }
        return -1;
    }

    int deleteHead() {
        if (!head) return -1;
        SinglyNode* removed = head;
        int value = removed->value;
        head = head->next;
        if (!head) tail = nullptr;
        removed->next = nullptr;
        delete removed;
        --size;
        return value;
    }

    bool deleteValue(int value) {
        if (!head) return false;
        if (head->value == value) {
            deleteHead();
            return true;
        }

        SinglyNode* previous = head;
        SinglyNode* current = head->next;
        while (current) {
            if (current->value == value) {
                previous->next = current->next;
                if (current == tail) tail = previous;
                current->next = nullptr;
                delete current;
                --size;
                return true;
            }
            previous = current;
            current = current->next;
        }
        return false;
    }

    int deleteAt(size_t index) {
        if (index >= size) throw out_of_range("Index out of range");
        if (index == 0) return deleteHead();

        SinglyNode* previous = head;
        for (size_t i = 0; i < index - 1; ++i) previous = previous->next;

        SinglyNode* removed = previous->next;
        previous->next = removed->next;
        if (removed == tail) tail = previous;
        int value = removed->value;
        removed->next = nullptr;
        delete removed;
        --size;
        return value;
    }

    void update(size_t index, int value) {
        if (index >= size) throw out_of_range("Index out of range");
        SinglyNode* current = head;
        for (size_t i = 0; i < index; ++i) current = current->next;
        current->value = value;
    }

    SinglyNode* reverseIterative() {
        SinglyNode* previous = nullptr;
        SinglyNode* current = head;
        tail = head;
        while (current) {
            SinglyNode* next = current->next;
            current->next = previous;
            previous = current;
            current = next;
        }
        head = previous;
        return head;
    }

    SinglyNode* reverseRecursive() {
        tail = head;
        head = reverseNodesRecursive(head);
        return head;
    }

    SinglyNode* middleNode() const {
        SinglyNode* slow = head;
        SinglyNode* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow; // second middle for even length
    }

    SinglyNode* nthFromEnd(size_t n) const {
        if (n == 0) throw invalid_argument("n must be positive");
        SinglyNode* fast = head;
        SinglyNode* slow = head;
        for (size_t i = 0; i < n; ++i) {
            if (!fast) throw out_of_range("n exceeds list length");
            fast = fast->next;
        }
        while (fast) {
            slow = slow->next;
            fast = fast->next;
        }
        return slow;
    }

    int removeNthFromEnd(size_t n) {
        if (n == 0 || n > size) throw out_of_range("Invalid n");
        SinglyNode dummy(0);
        dummy.next = head;
        SinglyNode* fast = &dummy;
        SinglyNode* slow = &dummy;

        for (size_t i = 0; i <= n; ++i) {
            if (!fast) throw out_of_range("n exceeds list length");
            fast = fast->next;
        }
        while (fast) {
            slow = slow->next;
            fast = fast->next;
        }

        SinglyNode* removed = slow->next;
        int value = removed->value;
        slow->next = removed->next;
        if (removed == tail) tail = (slow == &dummy ? nullptr : slow);
        head = dummy.next;
        removed->next = nullptr;
        delete removed;
        --size;
        return value;
    }

    bool hasCycle() const { return detectCycle(head); }
    SinglyNode* cycleEntry() const { return findCycleEntry(head); }
    size_t cycleLength() const { return linkedCycleLength(head); }

    bool removeCycle() {
        SinglyNode* entry = findCycleEntry(head);
        if (!entry) return false;
        SinglyNode* current = entry;
        while (current->next != entry) current = current->next;
        current->next = nullptr;
        tail = current;
        return true;
    }

    bool isPalindrome() {
        if (!head || !head->next) return true;

        SinglyNode* slow = head;
        SinglyNode* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }

        SinglyNode* secondHalf = reverseNodes(slow);
        SinglyNode* first = head;
        SinglyNode* second = secondHalf;
        bool palindrome = true;
        while (second) {
            if (first->value != second->value) {
                palindrome = false;
                break;
            }
            first = first->next;
            second = second->next;
        }
        reverseNodes(secondHalf); // restore original links
        return palindrome;
    }

    SinglyLinkedList& removeDuplicatesSorted() {
        SinglyNode* current = head;
        while (current && current->next) {
            if (current->value == current->next->value) {
                SinglyNode* duplicate = current->next;
                current->next = duplicate->next;
                if (duplicate == tail) tail = current;
                duplicate->next = nullptr;
                delete duplicate;
                --size;
            } else {
                current = current->next;
            }
        }
        return *this;
    }

    SinglyLinkedList& removeDuplicatesUnsorted() {
        unordered_set<int> seen;
        SinglyNode* current = head;
        SinglyNode* previous = nullptr;
        while (current) {
            if (seen.count(current->value)) {
                SinglyNode* duplicate = current;
                previous->next = current->next;
                if (duplicate == tail) tail = previous;
                current = current->next;
                duplicate->next = nullptr;
                delete duplicate;
                --size;
            } else {
                seen.insert(current->value);
                previous = current;
                current = current->next;
            }
        }
        return *this;
    }

    SinglyLinkedList& rotateRight(long long k) {
        if (!head || !head->next || k == 0) return *this;
        long long normalized = k % static_cast<long long>(size);
        if (normalized < 0) normalized += static_cast<long long>(size);
        if (normalized == 0) return *this;

        tail->next = head;
        size_t stepsToNewTail = size - static_cast<size_t>(normalized);
        SinglyNode* newTail = head;
        for (size_t i = 1; i < stepsToNewTail; ++i) newTail = newTail->next;
        head = newTail->next;
        newTail->next = nullptr;
        tail = newTail;
        return *this;
    }

    SinglyLinkedList& sort() {
        head = mergeSortNodes(head);
        tail = head;
        if (tail) while (tail->next) tail = tail->next;
        return *this;
    }

    SinglyLinkedList& reorder() {
        if (!head || !head->next) return *this;
        SinglyNode* slow = head;
        SinglyNode* fast = head;
        while (fast->next && fast->next->next) {
            slow = slow->next;
            fast = fast->next->next;
        }

        SinglyNode* second = reverseNodes(slow->next);
        slow->next = nullptr;
        SinglyNode* first = head;

        while (second) {
            SinglyNode* firstNext = first->next;
            SinglyNode* secondNext = second->next;
            first->next = second;
            second->next = firstNext;
            first = firstNext;
            second = secondNext;
        }
        tail = head;
        while (tail->next) tail = tail->next;
        return *this;
    }

    void clear() {
        // Avoid an infinite loop if the list happens to be cyclic.
        removeCycle();
        while (head) {
            SinglyNode* next = head->next;
            delete head;
            head = next;
        }
        tail = nullptr;
        size = 0;
    }
};

// ============================================================
// 2. GENERIC SINGLY-LIST NODE HELPERS / POINTER PATTERNS
// ============================================================

SinglyNode* reverseNodes(SinglyNode* head) {
    SinglyNode* previous = nullptr;
    SinglyNode* current = head;
    while (current) {
        SinglyNode* next = current->next;
        current->next = previous;
        previous = current;
        current = next;
    }
    return previous;
}

SinglyNode* reverseNodesRecursive(SinglyNode* head) {
    if (!head || !head->next) return head;
    SinglyNode* newHead = reverseNodesRecursive(head->next);
    head->next->next = head;
    head->next = nullptr;
    return newHead;
}

SinglyNode* getMiddle(SinglyNode* head) {
    SinglyNode* slow = head;
    SinglyNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow; // second middle
}

SinglyNode* getFirstMiddle(SinglyNode* head) {
    if (!head) return nullptr;
    SinglyNode* slow = head;
    SinglyNode* fast = head;
    while (fast->next && fast->next->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow; // first middle for even length
}

SinglyNode* nthFromEnd(SinglyNode* head, size_t n) {
    if (n == 0) throw invalid_argument("n must be positive");
    SinglyNode* fast = head;
    SinglyNode* slow = head;
    for (size_t i = 0; i < n; ++i) {
        if (!fast) return nullptr;
        fast = fast->next;
    }
    while (fast) {
        slow = slow->next;
        fast = fast->next;
    }
    return slow;
}

bool detectCycle(SinglyNode* head) {
    SinglyNode* slow = head;
    SinglyNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}

SinglyNode* getCycleMeetingNode(SinglyNode* head) {
    SinglyNode* slow = head;
    SinglyNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return slow;
    }
    return nullptr;
}

SinglyNode* findCycleEntry(SinglyNode* head) {
    SinglyNode* meeting = getCycleMeetingNode(head);
    if (!meeting) return nullptr;
    SinglyNode* slow = head;
    SinglyNode* fast = meeting;
    while (slow != fast) {
        slow = slow->next;
        fast = fast->next;
    }
    return slow;
}

size_t linkedCycleLength(SinglyNode* head) {
    SinglyNode* meeting = getCycleMeetingNode(head);
    if (!meeting) return 0;
    size_t length = 1;
    SinglyNode* current = meeting->next;
    while (current != meeting) {
        current = current->next;
        ++length;
    }
    return length;
}

bool removeCycle(SinglyNode* head) {
    SinglyNode* entry = findCycleEntry(head);
    if (!entry) return false;
    SinglyNode* current = entry;
    while (current->next != entry) current = current->next;
    current->next = nullptr;
    return true;
}

// ============================================================
// 3. MERGING LINKED LISTS
// ============================================================

SinglyNode* mergeTwoSortedLists(SinglyNode* first, SinglyNode* second) {
    SinglyNode dummy(0);
    SinglyNode* current = &dummy;

    while (first && second) {
        if (first->value <= second->value) {
            current->next = first;
            first = first->next;
        } else {
            current->next = second;
            second = second->next;
        }
        current = current->next;
    }
    current->next = first ? first : second;
    return dummy.next;
}

SinglyNode* mergeTwoSortedListsRecursive(SinglyNode* first, SinglyNode* second) {
    if (!first) return second;
    if (!second) return first;
    if (first->value <= second->value) {
        first->next = mergeTwoSortedListsRecursive(first->next, second);
        return first;
    }
    second->next = mergeTwoSortedListsRecursive(first, second->next);
    return second;
}

SinglyNode* mergeKSortedLists(vector<SinglyNode*>& lists) {
    if (lists.empty()) return nullptr;
    vector<SinglyNode*> current = lists;
    while (current.size() > 1) {
        vector<SinglyNode*> merged;
        merged.reserve((current.size() + 1) / 2);
        for (size_t i = 0; i < current.size(); i += 2) {
            SinglyNode* other = (i + 1 < current.size()) ? current[i + 1] : nullptr;
            merged.push_back(mergeTwoSortedLists(current[i], other));
        }
        current = move(merged);
    }
    return current.front();
}

// ============================================================
// 4. INTERSECTION OF TWO LINKED LISTS
// ============================================================

SinglyNode* getIntersectionNode(SinglyNode* headA, SinglyNode* headB) {
    SinglyNode* a = headA;
    SinglyNode* b = headB;
    while (a != b) {
        a = a ? a->next : headB;
        b = b ? b->next : headA;
    }
    return a;
}

// ============================================================
// 5. PALINDROME LINKED LIST
// ============================================================

bool isPalindrome(SinglyNode* head) {
    if (!head || !head->next) return true;
    SinglyNode* slow = head;
    SinglyNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }

    SinglyNode* secondHalf = reverseNodes(slow);
    SinglyNode* first = head;
    SinglyNode* second = secondHalf;
    bool result = true;

    while (second) {
        if (first->value != second->value) {
            result = false;
            break;
        }
        first = first->next;
        second = second->next;
    }
    reverseNodes(secondHalf); // restore
    return result;
}

// ============================================================
// 6. ROTATE LIST / REORDER LIST
// ============================================================

SinglyNode* rotateRight(SinglyNode* head, long long k) {
    if (!head || !head->next || k == 0) return head;
    size_t length = 1;
    SinglyNode* tail = head;
    while (tail->next) {
        tail = tail->next;
        ++length;
    }

    long long normalized = k % static_cast<long long>(length);
    if (normalized < 0) normalized += static_cast<long long>(length);
    if (normalized == 0) return head;

    tail->next = head;
    size_t steps = length - static_cast<size_t>(normalized);
    SinglyNode* newTail = head;
    for (size_t i = 1; i < steps; ++i) newTail = newTail->next;
    SinglyNode* newHead = newTail->next;
    newTail->next = nullptr;
    return newHead;
}

SinglyNode* reorderList(SinglyNode* head) {
    if (!head || !head->next) return head;
    SinglyNode* slow = head;
    SinglyNode* fast = head;
    while (fast->next && fast->next->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    SinglyNode* second = reverseNodes(slow->next);
    slow->next = nullptr;
    SinglyNode* first = head;
    while (second) {
        SinglyNode* firstNext = first->next;
        SinglyNode* secondNext = second->next;
        first->next = second;
        second->next = firstNext;
        first = firstNext;
        second = secondNext;
    }
    return head;
}

// ============================================================
// 7. LINKED-LIST MERGE SORT
// ============================================================

SinglyNode* mergeSortNodes(SinglyNode* head) {
    if (!head || !head->next) return head;
    SinglyNode* slow = head;
    SinglyNode* fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    SinglyNode* right = slow->next;
    slow->next = nullptr;
    SinglyNode* left = mergeSortNodes(head);
    right = mergeSortNodes(right);
    return mergeTwoSortedLists(left, right);
}

SinglyNode* sortLinkedList(SinglyNode* head) {
    return mergeSortNodes(head);
}

// ============================================================
// 8. DUPLICATE REMOVAL
// ============================================================

SinglyNode* removeDuplicatesSorted(SinglyNode* head) {
    SinglyNode* current = head;
    while (current && current->next) {
        if (current->value == current->next->value) {
            SinglyNode* duplicate = current->next;
            current->next = duplicate->next;
            delete duplicate;
        } else {
            current = current->next;
        }
    }
    return head;
}

SinglyNode* removeDuplicatesUnsortedWithSet(SinglyNode* head) {
    unordered_set<int> seen;
    SinglyNode* current = head;
    SinglyNode* previous = nullptr;
    while (current) {
        if (seen.count(current->value)) {
            SinglyNode* duplicate = current;
            previous->next = current->next;
            current = current->next;
            delete duplicate;
        } else {
            seen.insert(current->value);
            previous = current;
            current = current->next;
        }
    }
    return head;
}

SinglyNode* removeAllDuplicatesSorted(SinglyNode* head) {
    // Remove every value that occurs more than once.
    SinglyNode dummy(0);
    dummy.next = head;
    SinglyNode* previous = &dummy;
    SinglyNode* current = head;

    while (current) {
        bool duplicate = false;
        while (current->next && current->value == current->next->value) {
            duplicate = true;
            SinglyNode* removed = current;
            current = current->next;
            delete removed;
        }
        if (duplicate) {
            SinglyNode* removed = current;
            previous->next = current->next;
            current = current->next;
            delete removed;
        } else {
            previous = current;
            current = current->next;
        }
    }
    return dummy.next;
}

// ============================================================
// 9. SWAP NODES IN PAIRS / REVERSE IN K-GROUPS
// ============================================================

SinglyNode* swapPairs(SinglyNode* head) {
    SinglyNode dummy(0);
    dummy.next = head;
    SinglyNode* previous = &dummy;

    while (previous->next && previous->next->next) {
        SinglyNode* first = previous->next;
        SinglyNode* second = first->next;
        first->next = second->next;
        second->next = first;
        previous->next = second;
        previous = first;
    }
    return dummy.next;
}

SinglyNode* getKthNode(SinglyNode* start, size_t k) {
    SinglyNode* current = start;
    for (size_t i = 0; i < k; ++i) {
        if (!current) return nullptr;
        current = current->next;
    }
    return current;
}

SinglyNode* reverseKGroup(SinglyNode* head, size_t k) {
    if (k <= 1 || !head) return head;
    SinglyNode dummy(0);
    dummy.next = head;
    SinglyNode* groupPrevious = &dummy;

    while (true) {
        SinglyNode* kth = getKthNode(groupPrevious, k);
        if (!kth) break;
        SinglyNode* groupNext = kth->next;

        SinglyNode* previous = groupNext;
        SinglyNode* current = groupPrevious->next;
        while (current != groupNext) {
            SinglyNode* next = current->next;
            current->next = previous;
            previous = current;
            current = next;
        }

        SinglyNode* oldStart = groupPrevious->next;
        groupPrevious->next = kth;
        groupPrevious = oldStart;
    }
    return dummy.next;
}

// ============================================================
// 10. DELETE NODE GIVEN ONLY THAT NODE (NOT TAIL)
// ============================================================

void deleteGivenNode(SinglyNode* node) {
    if (!node || !node->next)
        throw invalid_argument("Cannot delete null or tail node this way");
    SinglyNode* next = node->next;
    node->value = next->value;
    node->next = next->next;
    next->next = nullptr;
    delete next;
}

// ============================================================
// 11. ADD TWO NUMBERS (DIGITS IN REVERSE ORDER)
// ============================================================

SinglyNode* addTwoNumbers(SinglyNode* first, SinglyNode* second) {
    SinglyNode dummy(0);
    SinglyNode* current = &dummy;
    int carry = 0;

    while (first || second || carry) {
        int x = first ? first->value : 0;
        int y = second ? second->value : 0;
        int sum = x + y + carry;
        carry = sum / 10;
        current->next = new SinglyNode(sum % 10);
        current = current->next;
        if (first) first = first->next;
        if (second) second = second->next;
    }
    return dummy.next;
}

// ============================================================
// 12. PARTITION LIST / ODD-EVEN LIST
// ============================================================

SinglyNode* partitionList(SinglyNode* head, int pivot) {
    SinglyNode beforeDummy(0), afterDummy(0);
    SinglyNode* before = &beforeDummy;
    SinglyNode* after = &afterDummy;
    SinglyNode* current = head;

    while (current) {
        SinglyNode* next = current->next;
        current->next = nullptr;
        if (current->value < pivot) {
            before->next = current;
            before = before->next;
        } else {
            after->next = current;
            after = after->next;
        }
        current = next;
    }
    before->next = afterDummy.next;
    return beforeDummy.next;
}

SinglyNode* oddEvenList(SinglyNode* head) {
    if (!head || !head->next) return head;
    SinglyNode* odd = head;
    SinglyNode* even = head->next;
    SinglyNode* evenHead = even;

    while (even && even->next) {
        odd->next = even->next;
        odd = odd->next;
        even->next = odd->next;
        even = even->next;
    }
    odd->next = evenHead;
    return head;
}

// ============================================================
// 13. REMOVE ZERO-SUM CONSECUTIVE NODES
// ============================================================

SinglyNode* removeZeroSumSublists(SinglyNode* head) {
    SinglyNode dummy(0);
    dummy.next = head;
    unordered_map<long long, SinglyNode*> last;
    long long prefix = 0;

    for (SinglyNode* current = &dummy; current; current = current->next) {
        prefix += current->value;
        last[prefix] = current;
    }

    prefix = 0;
    for (SinglyNode* current = &dummy; current; current = current->next) {
        prefix += current->value;
        current->next = last[prefix]->next;
    }
    return dummy.next;
}

// ============================================================
// 14. COPY LIST WITH RANDOM POINTER
// ============================================================

struct RandomNode {
    int value;
    RandomNode* next = nullptr;
    RandomNode* random = nullptr;
    explicit RandomNode(int value) : value(value) {}
};

RandomNode* copyRandomList(RandomNode* head) {
    if (!head) return nullptr;
    unordered_map<RandomNode*, RandomNode*> mapping;
    for (RandomNode* current = head; current; current = current->next)
        mapping[current] = new RandomNode(current->value);

    for (RandomNode* current = head; current; current = current->next) {
        RandomNode* copy = mapping[current];
        copy->next = current->next ? mapping[current->next] : nullptr;
        copy->random = current->random ? mapping[current->random] : nullptr;
    }
    return mapping[head];
}

// ============================================================
// 15. FLATTEN MULTILEVEL DOUBLY LINKED LIST
// ============================================================

struct MultiLevelNode {
    int value;
    MultiLevelNode* prev = nullptr;
    MultiLevelNode* next = nullptr;
    MultiLevelNode* child = nullptr;
    explicit MultiLevelNode(int value) : value(value) {}
};

MultiLevelNode* flattenMultilevelDoublyList(MultiLevelNode* head) {
    if (!head) return nullptr;
    vector<MultiLevelNode*> stack{head};
    MultiLevelNode* previous = nullptr;

    while (!stack.empty()) {
        MultiLevelNode* current = stack.back();
        stack.pop_back();

        if (previous) {
            previous->next = current;
            current->prev = previous;
        }
        if (current->next) stack.push_back(current->next);
        if (current->child) {
            stack.push_back(current->child);
            current->child = nullptr;
        }
        previous = current;
    }
    if (previous) previous->next = nullptr;
    head->prev = nullptr;
    return head;
}

// ============================================================
// 16. LRU CACHE — HASH MAP + DOUBLY LINKED LIST
// ============================================================

class LRUCache {
    struct Node {
        int key;
        int value;
        Node* previous;
        Node* next;
        Node(int key = 0, int value = 0)
            : key(key), value(value), previous(nullptr), next(nullptr) {}
    };

    size_t capacity;
    unordered_map<int, Node*> cache;
    Node left;  // least-recently-used sentinel
    Node right; // most-recently-used sentinel

    void remove(Node* node) {
        node->previous->next = node->next;
        node->next->previous = node->previous;
    }

    void insertRight(Node* node) {
        Node* previous = right.previous;
        previous->next = node;
        node->previous = previous;
        node->next = &right;
        right.previous = node;
    }

public:
    explicit LRUCache(size_t capacity) : capacity(capacity) {
        left.next = &right;
        right.previous = &left;
    }

    LRUCache(const LRUCache&) = delete;
    LRUCache& operator=(const LRUCache&) = delete;

    ~LRUCache() {
        Node* current = left.next;
        while (current != &right) {
            Node* next = current->next;
            delete current;
            current = next;
        }
    }

    int get(int key) {
        auto it = cache.find(key);
        if (it == cache.end()) return -1;
        Node* node = it->second;
        remove(node);
        insertRight(node);
        return node->value;
    }

    void put(int key, int value) {
        auto it = cache.find(key);
        if (it != cache.end()) {
            Node* node = it->second;
            remove(node);
            node->value = value;
            insertRight(node);
            return;
        }

        if (capacity == 0) return;
        Node* node = new Node(key, value);
        cache[key] = node;
        insertRight(node);

        if (cache.size() > capacity) {
            Node* least = left.next;
            remove(least);
            cache.erase(least->key);
            delete least;
        }
    }
};

// ============================================================
// 17. DOUBLY LINKED LIST
// ============================================================

struct DoublyNode {
    int value;
    DoublyNode* previous = nullptr;
    DoublyNode* next = nullptr;
    explicit DoublyNode(int value) : value(value) {}
};

class DoublyLinkedList {
public:
    DoublyNode* head = nullptr;
    DoublyNode* tail = nullptr;
    size_t size = 0;

    DoublyLinkedList() = default;
    explicit DoublyLinkedList(const vector<int>& values) {
        for (int value : values) append(value);
    }
    DoublyLinkedList(const DoublyLinkedList&) = delete;
    DoublyLinkedList& operator=(const DoublyLinkedList&) = delete;
    ~DoublyLinkedList() { clear(); }

    vector<int> toVector() const {
        vector<int> result;
        for (DoublyNode* current = head; current; current = current->next)
            result.push_back(current->value);
        return result;
    }

    vector<int> toReverseVector() const {
        vector<int> result;
        for (DoublyNode* current = tail; current; current = current->previous)
            result.push_back(current->value);
        return result;
    }

    DoublyNode* prepend(int value) {
        auto* node = new DoublyNode(value);
        node->next = head;
        if (head) head->previous = node;
        else tail = node;
        head = node;
        ++size;
        return node;
    }

    DoublyNode* append(int value) {
        auto* node = new DoublyNode(value);
        node->previous = tail;
        if (tail) tail->next = node;
        else head = node;
        tail = node;
        ++size;
        return node;
    }

    DoublyNode* insertAfter(DoublyNode* node, int value) {
        if (!node) throw invalid_argument("node cannot be null");
        auto* added = new DoublyNode(value);
        added->previous = node;
        added->next = node->next;
        if (node->next) node->next->previous = added;
        else tail = added;
        node->next = added;
        ++size;
        return added;
    }

    DoublyNode* insertBefore(DoublyNode* node, int value) {
        if (!node) throw invalid_argument("node cannot be null");
        auto* added = new DoublyNode(value);
        added->next = node;
        added->previous = node->previous;
        if (node->previous) node->previous->next = added;
        else head = added;
        node->previous = added;
        ++size;
        return added;
    }

    int deleteNode(DoublyNode* node) {
        if (!node) throw invalid_argument("node cannot be null");
        if (node->previous) node->previous->next = node->next;
        else head = node->next;
        if (node->next) node->next->previous = node->previous;
        else tail = node->previous;
        int value = node->value;
        node->previous = node->next = nullptr;
        delete node;
        --size;
        return value;
    }

    DoublyNode* find(int value) const {
        for (DoublyNode* current = head; current; current = current->next)
            if (current->value == value) return current;
        return nullptr;
    }

    DoublyLinkedList& reverse() {
        DoublyNode* current = head;
        while (current) {
            swap(current->previous, current->next);
            current = current->previous;
        }
        swap(head, tail);
        return *this;
    }

    void clear() {
        while (head) {
            DoublyNode* next = head->next;
            delete head;
            head = next;
        }
        tail = nullptr;
        size = 0;
    }
};

// ============================================================
// 18. CIRCULAR SINGLY LINKED LIST
// ============================================================

struct CircularNode {
    int value;
    CircularNode* next = nullptr;
    explicit CircularNode(int value) : value(value) {}
};

class CircularLinkedList {
public:
    CircularNode* head = nullptr;
    CircularNode* tail = nullptr;
    size_t size = 0;

    CircularLinkedList() = default;
    explicit CircularLinkedList(const vector<int>& values) {
        for (int value : values) append(value);
    }
    CircularLinkedList(const CircularLinkedList&) = delete;
    CircularLinkedList& operator=(const CircularLinkedList&) = delete;
    ~CircularLinkedList() { clear(); }

    vector<int> toVector() const {
        vector<int> result;
        if (!head) return result;
        CircularNode* current = head;
        do {
            result.push_back(current->value);
            current = current->next;
        } while (current != head);
        return result;
    }

    CircularNode* append(int value) {
        auto* node = new CircularNode(value);
        if (!head) {
            head = tail = node;
            node->next = node;
        } else {
            node->next = head;
            tail->next = node;
            tail = node;
        }
        ++size;
        return node;
    }

    CircularNode* prepend(int value) {
        auto* node = new CircularNode(value);
        if (!head) {
            head = tail = node;
            node->next = node;
        } else {
            node->next = head;
            tail->next = node;
            head = node;
        }
        ++size;
        return node;
    }

    CircularNode* insertAfter(CircularNode* node, int value) {
        if (!node) throw invalid_argument("node cannot be null");
        auto* added = new CircularNode(value);
        added->next = node->next;
        node->next = added;
        if (node == tail) tail = added;
        ++size;
        return added;
    }

    bool deleteValue(int value) {
        if (!head) return false;
        CircularNode* current = head;
        CircularNode* previous = tail;
        do {
            if (current->value == value) {
                if (size == 1) {
                    head = tail = nullptr;
                } else {
                    previous->next = current->next;
                    if (current == head) head = current->next;
                    if (current == tail) tail = previous;
                    tail->next = head;
                }
                current->next = nullptr;
                delete current;
                --size;
                return true;
            }
            previous = current;
            current = current->next;
        } while (current != head);
        return false;
    }

    CircularNode* search(int value) const {
        if (!head) return nullptr;
        CircularNode* current = head;
        do {
            if (current->value == value) return current;
            current = current->next;
        } while (current != head);
        return nullptr;
    }

    void clear() {
        if (!head) return;
        tail->next = nullptr;
        CircularNode* current = head;
        while (current) {
            CircularNode* next = current->next;
            delete current;
            current = next;
        }
        head = tail = nullptr;
        size = 0;
    }
};

// ============================================================
// 19. CONSTRUCTION / DEBUG HELPERS
// ============================================================

SinglyNode* buildSingly(const vector<int>& values) {
    SinglyNode dummy(0);
    SinglyNode* current = &dummy;
    for (int value : values) {
        current->next = new SinglyNode(value);
        current = current->next;
    }
    return dummy.next;
}

vector<int> listFromHead(SinglyNode* head, size_t limit = 100) {
    vector<int> result;
    SinglyNode* current = head;
    size_t count = 0;
    while (current && count < limit) {
        result.push_back(current->value);
        current = current->next;
        ++count;
    }
    if (current) result.push_back(numeric_limits<int>::min()); // cycle/limit marker
    return result;
}

SinglyNode* createCycle(SinglyNode* head, size_t position) {
    if (!head) return head;
    SinglyNode* cycleNode = nullptr;
    SinglyNode* current = head;
    SinglyNode* tail = nullptr;
    size_t index = 0;
    while (current) {
        if (index == position) cycleNode = current;
        tail = current;
        current = current->next;
        ++index;
    }
    if (!cycleNode) throw out_of_range("Invalid cycle position");
    tail->next = cycleNode;
    return head;
}

void deleteLinearList(SinglyNode* head) {
    while (head) {
        SinglyNode* next = head->next;
        delete head;
        head = next;
    }
}

// ============================================================
// 20. INTERVIEW-STYLE TESTS
// ============================================================

void runRevisionTests() {
    {
        SinglyLinkedList list({1, 2, 3, 4, 5});
        assert((list.toVector() == vector<int>{1, 2, 3, 4, 5}));
        assert(list.get(2) == 3);
        assert(list.find(4) == 3);
        list.prepend(0);
        list.append(6);
        list.insertAt(3, 99);
        assert((list.toVector() == vector<int>{0, 1, 2, 99, 3, 4, 5, 6}));
        list.deleteValue(99);
        assert((list.toVector() == vector<int>{0, 1, 2, 3, 4, 5, 6}));
        assert(list.middleNode()->value == 3);
        assert(list.nthFromEnd(1)->value == 6);
        list.reverseIterative();
        assert((list.toVector() == vector<int>{6, 5, 4, 3, 2, 1, 0}));
        list.reverseRecursive();
        assert((list.toVector() == vector<int>{0, 1, 2, 3, 4, 5, 6}));
        list.removeNthFromEnd(1);
        assert((list.toVector() == vector<int>{0, 1, 2, 3, 4, 5}));
    }
    {
        SinglyNode* palindrome = buildSingly({1, 2, 3, 2, 1});
        assert(isPalindrome(palindrome));
        deleteLinearList(palindrome);
    }
    {
        SinglyNode* a = buildSingly({1, 3, 5});
        SinglyNode* b = buildSingly({2, 4, 6});
        SinglyNode* merged = mergeTwoSortedLists(a, b);
        assert((listFromHead(merged) == vector<int>{1, 2, 3, 4, 5, 6}));
        deleteLinearList(merged);
    }
    {
        SinglyNode* cyclic = buildSingly({1, 2, 3, 4, 5});
        createCycle(cyclic, 2);
        assert(detectCycle(cyclic));
        assert(findCycleEntry(cyclic)->value == 3);
        assert(linkedCycleLength(cyclic) == 3);
        assert(removeCycle(cyclic));
        assert(!detectCycle(cyclic));
        deleteLinearList(cyclic);
    }
    {
        DoublyLinkedList list({1, 2, 3});
        assert((list.toVector() == vector<int>{1, 2, 3}));
        assert((list.toReverseVector() == vector<int>{3, 2, 1}));
        list.reverse();
        assert((list.toVector() == vector<int>{3, 2, 1}));
    }
    {
        CircularLinkedList list({1, 2, 3});
        assert((list.toVector() == vector<int>{1, 2, 3}));
        list.deleteValue(1);
        assert((list.toVector() == vector<int>{2, 3}));
    }
    {
        SinglyNode* list = buildSingly({1, 2, 3, 4, 5});
        list = reverseKGroup(list, 2);
        assert((listFromHead(list) == vector<int>{2, 1, 4, 3, 5}));
        deleteLinearList(list);
    }
    {
        SinglyNode* list = buildSingly({1, 2, 3, 4});
        list = swapPairs(list);
        assert((listFromHead(list) == vector<int>{2, 1, 4, 3}));
        deleteLinearList(list);
    }
    {
        LRUCache cache(2);
        cache.put(1, 10);
        cache.put(2, 20);
        assert(cache.get(1) == 10);
        cache.put(3, 30);
        assert(cache.get(2) == -1);
        assert(cache.get(3) == 30);
    }
    cout << "All Linked List revision tests passed!\\n";
}

int main() {
#ifdef RUN_REVISION_TESTS
    runRevisionTests();
#else
    cout << "LINKED LIST — COMPLETE REVISION CODEBOOK (C++17)\\n";
    cout << "Singly / Doubly / Circular / Fast-Slow / Cycle / Merge / Advanced\\n";
    cout << "Compile with -DRUN_REVISION_TESTS to run the verification suite.\\n";
#endif
    return 0;
}
