import random

class SpawnData:
    """
    Lớp quản lý các điểm xuất hiện (spawn) cho zombie.

    Lớp này chứa danh sách các tọa độ mà zombie có thể xuất hiện.
    """

    def __init__(self):
        """
        Khởi tạo lớp SpawnData và thiết lập danh sách các điểm spawn.
        """
        self.spawn_points = [
            (105, 220),
            (165, 170),
            (200, 310),
            (250, 180),
            (325, 250),
            (470, 220),
        ]

    def spawn_point(self):
        """
        Chọn và trả về một điểm spawn ngẫu nhiên.

        :return: Tọa độ (x, y) của điểm spawn ngẫu nhiên.
        """
        return random.choice(self.spawn_points)