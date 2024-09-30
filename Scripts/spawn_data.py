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
            (170, 440),
            (315, 590),
            (265, 325),
            (400, 340),
            (520, 455),
            (750, 425),
        ]

    def spawn_point(self):
        """
        Chọn và trả về một điểm spawn ngẫu nhiên.

        :return: Tọa độ (x, y) của điểm spawn ngẫu nhiên.
        """
        return random.choice(self.spawn_points)
