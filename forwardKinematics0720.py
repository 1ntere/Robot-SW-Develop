import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

# UR5 DH Parameters (Standard DH)
a = np.array([0, -0.425, -0.392, 0, 0, 0])                 # a_i
d = np.array([0.089, 0, 0, 0.109, 0.095, 0.082])           # d_i
alpha = np.array([np.pi/2, 0, 0, np.pi/2, -np.pi/2, 0])    # alpha_i
theta_default = np.zeros(6)                                # initial joint angles

# DH 변환 행렬 함수
def dh_transform(theta, d, a, alpha):
    """DH 파라미터로 변환 행렬 생성"""
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0,              np.sin(alpha),                np.cos(alpha),               d],
        [0,              0,                            0,                           1]
    ])

# Forward Kinematics 계산 함수
def forward_kinematics(theta_list, a, d, alpha):
    """Joint 각도를 받아 End-effector 위치 계산"""
    T = np.eye(4)
    positions = [T[:3, 3]]  # 시작점 (base)

    for i in range(6):
        T_i = dh_transform(np.deg2rad(theta_list[i]), d[i], a[i], alpha[i])
        T = T @ T_i
        positions.append(T[:3, 3])  # 각 관절 위치 저장

    return np.array(positions)

# 로봇팔 그리기
def plot_robot(positions, ax):
    ax.clear()
    ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], '-o', linewidth=3, markersize=6, color='blue')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(0, 1.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('UR5 Forward Kinematics')
    ax.grid(True)

# 시뮬레이터 실행
def run_simulator():
    # 초기 설정
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(left=0.2, bottom=0.4)

    theta = theta_default.copy()
    positions = forward_kinematics(theta, a, d, alpha)
    plot_robot(positions, ax)

    # 슬라이더 설정
    sliders = []
    axcolor = 'lightgoldenrodyellow'

    for i in range(6):
        ax_slider = plt.axes([0.2, 0.05 + i*0.05, 0.65, 0.03], facecolor=axcolor)
        slider = Slider(ax_slider, f'θ{i+1} (deg)', -180, 180, valinit=theta[i])
        sliders.append(slider)

    # 업데이트 함수
    def update(val):
        theta_vals = [s.val for s in sliders]
        positions = forward_kinematics(theta_vals, a, d, alpha)
        plot_robot(positions, ax)
        fig.canvas.draw_idle()

    # 슬라이더 이벤트 연결
    for s in sliders:
        s.on_changed(update)

    plt.show()

# 실행
if __name__ == '__main__':
    run_simulator()
