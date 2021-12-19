import node
from node import Node
from typing import *


class Snake:
    def __init__(self):
        self.__head = self.__tail = None
        self.__length = 0
        self.__color = None
        self.orientation = None

    def add_new_head(self, new_head: Node):
        """מתודה שמוסיפה חוליה לראש הנחש ומתעדכנת להיות הראש החדש
       אם הנחש עוד לא הוגדר אז כעת הנחש יוגדר באורך 1 וראשו יהיה החוליה שבקלט"""

        if self.__head is None:
            # list was empty - snake didn't build yet
            self.__tail = new_head
        else:  # connect old head to new head
            self.__head.prev = new_head
            new_head.next = self.__head

        # update head
        self.__head = new_head
        self.__length += 1

    def get_head(self) -> Node:
        return self.__head

    def remove_tail(self):
        """מתודה שמוחקת את החוליה האחרונה של הנחש ומתעדכנת באורך בהתאם"""
        self.__tail = self.__tail.prev
        if self.__tail is None:  # list is now empty
            self.__head = None
        else:  # disconnect old tail
            self.__tail.next.prev = None
            self.__tail.next = None
        self.__length -= 1

    def in_crash(self, cell):
        """מתודה המקבלת מיקום של תא(x,y)
        מחזירה True אם התא הוא אחד מחוליות הנחש, False אחרת"""
        return self.crash_helper(self.__head, cell, 0)

    def crash_helper(self, cur, cell, index):
        # שימוש פנימי: פונקציית עזר ל in_crash
        if index >= self.__length:
            return False
        if cur.get_data() == cell:
            return True
        return self.crash_helper(cur.get_next(), cell, index + 1)

    def set_color(self, color: str):
        self.__color = color

    def possible_moves(self):
        """מחזירה על סמך הכיוון הנוכחי של הנחש מהם המהלכים האפשריים"""
        if self.orientation == "Right":
            return ["Down", "Up"]
        if self.orientation == "Left":
            return ["Down", "Up"]
        if self.orientation == "Up":
            return ["Right", "Left"]
        if self.orientation == "Down":
            return ["Right", "Left"]

    def move(self, movekey):
        """פונקציה המקבלת כיוון ומחזירה אמת אם הנחש זז בהצלחה, שקר אחרת"""
        if movekey in self.possible_moves():  # אם הכיוון נמצא ברשימת הכיוונים - נעדכן את הכיוון.
            self.orientation = movekey        # אם לא, נמשיך עם הכיוון הנוכחי
        row_head = self.get_head().get_data()[0]
        col_head = self.get_head().get_data()[1]
        if self.orientation == "Right":
            x = row_head
            y = col_head + 1
        if self.orientation == "Left":
            x = row_head
            y = col_head - 1
        if self.orientation == "Down":
            x = row_head + 1
            y = col_head
        if self.orientation == "Up":
            x = row_head - 1
            y = col_head
        if self.in_crash((x, y)):  # אם הראש העתידי של הנחש יפגע בגופו נחזיר False
            return False
        new_head = Node((x, y))
        self.add_new_head(new_head)
        self.remove_tail()
        return True
s = Snake()
s.orientation = "Up"
head = Node((7,9))
s.add_new_head(head)
print(s.get_head().get_data())
s.move("Right")
print(s.get_head().get_data())
