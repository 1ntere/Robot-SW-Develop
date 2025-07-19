import tkinter as tk
from tkinter import messagebox

def calculate_dof(num_links, num_joints, joint_dofs):
    m = 6  # 3D 공간
    F = m * (num_links - num_joints - 1) + sum(joint_dofs)
    return F

def suggest_design(dof):
    if dof < 6:
        return "❗ 자유도가 부족합니다. 관절 수 또는 자유도를 늘려야 3D 제어가 가능합니다."
    elif dof == 6:
        return "✅ 설계가 적절합니다. 3D 공간에서 위치 및 자세 제어에 필요한 최소 자유도입니다."
    else:
        return "⚠️ 자유도가 과도합니다. 제어 복잡도 및 비용 증가 가능성이 있습니다."

def on_calculate():
    try:
        num_links = int(entry_links.get())
        num_joints = int(entry_joints.get())
        dof_strs = entry_dofs.get().split(',')
        joint_dofs = [int(d.strip()) for d in dof_strs]

        if len(joint_dofs) != num_joints:
            raise ValueError("관절 수와 자유도 항목 수가 일치하지 않습니다.")

        dof = calculate_dof(num_links, num_joints, joint_dofs)
        feedback = suggest_design(dof)

        label_result.config(text=f"계산된 자유도: {dof}")
        label_feedback.config(text=feedback)

    except Exception as e:
        messagebox.showerror("입력 오류", str(e))

# GUI 생성
root = tk.Tk()
root.title("로봇 자유도 계산기 with 설계 피드백")
root.geometry("420x250")

# 입력 필드
tk.Label(root, text="링크 수:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
entry_links = tk.Entry(root, width=30)
entry_links.grid(row=0, column=1)

tk.Label(root, text="관절 수:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_joints = tk.Entry(root, width=30)
entry_joints.grid(row=1, column=1)

tk.Label(root, text="각 관절 자유도 (쉼표로 구분):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_dofs = tk.Entry(root, width=30)
entry_dofs.grid(row=2, column=1)

# 계산 버튼
btn = tk.Button(root, text="자유도 계산", command=on_calculate)
btn.grid(row=3, column=0, columnspan=2, pady=10)

# 결과 출력
label_result = tk.Label(root, text="", fg="black", font=("Arial", 11, "bold"))
label_result.grid(row=4, column=0, columnspan=2)

label_feedback = tk.Label(root, text="", fg="blue", wraplength=400, justify="center")
label_feedback.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
