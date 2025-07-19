import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QPushButton
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# UR5 DH Parameters
a = np.array([0, -0.425, -0.392, 0, 0, 0])
d = np.array([0.089, 0, 0, 0.109, 0.095, 0.082])
alpha = np.array([np.pi/2, 0, 0, np.pi/2, -np.pi/2, 0])
theta_default = np.zeros(6)

# DH 변환 행렬 함수
def dh_transform(theta, d, a, alpha):
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0,              np.sin(alpha),                np.cos(alpha),               d],
        [0,              0,                            0,                           1]
    ])

# Forward Kinematics 계산
def forward_kinematics(theta_list, a, d, alpha):
    T = np.eye(4)
    positions = [T[:3, 3]]
    for i in range(6):
        T_i = dh_transform(np.deg2rad(theta_list[i]), d[i], a[i], alpha[i])
        T = T @ T_i
        positions.append(T[:3, 3])
    return np.array(positions)

# PyQt5 시뮬레이터 GUI 클래스
class UR5Simulator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UR5 Forward Kinematics Simulator")
        self.setGeometry(100, 100, 1000, 800)

        self.a = a
        self.d = d
        self.alpha = alpha
        self.theta = theta_default.copy()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Matplotlib Figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.main_layout.addWidget(self.canvas)

        # 슬라이더 UI
        self.sliders = []
        for i in range(6):
            row = QHBoxLayout()
            label = QLabel(f"θ{i+1}")
            slider = QSlider(Qt.Horizontal)
            slider.setRange(-180, 180)
            slider.setValue(0)
            slider.valueChanged.connect(self.update_plot)
            row.addWidget(label)
            row.addWidget(slider)
            self.main_layout.addLayout(row)
            self.sliders.append(slider)

        # 스냅샷 저장 버튼
        self.snapshot_btn = QPushButton("📸 스냅샷 저장")
        self.snapshot_btn.clicked.connect(self.save_snapshot)
        self.main_layout.addWidget(self.snapshot_btn)

        self.update_plot()

    def update_plot(self):
        self.theta = np.array([s.value() for s in self.sliders])
        positions = forward_kinematics(self.theta, self.a, self.d, self.alpha)

        self.ax.clear()
        self.ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], '-o', color='blue', linewidth=3)
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_zlim(0, 1.5)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.set_title("UR5 Forward Kinematics")

        self.canvas.draw()

    def save_snapshot(self):
        self.figure.savefig("ur5_gui_snapshot.png")
        print("✅ 스냅샷 저장 완료: ur5_gui_snapshot.png")

# 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UR5Simulator()
    window.show()
    sys.exit(app.exec_())
