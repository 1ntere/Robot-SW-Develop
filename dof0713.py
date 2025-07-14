import tkinter as tk
from tkinter import messagebox

def calculate_dof():
    try:
        num_links = int(entry_links.get())
        num_joints = int(entry_joints.get())
        dof_list_str = entry_dofs.get().split(',')
        joint_dofs = [int(dof.strip()) for dof in dof_list_str]
        
        if len(joint_dofs) != num_joints:
            raise ValueError("관절 수와 자유도 수가 일치하지 않습니다.")
        
        m = 6  # 3D 공간
        F = m * (num_links - num_joints - 1) + sum(joint_dofs)
        label_result.config(text=f"계산된 자유도: {F}")
    
    except Exception as e:
        messagebox.showerror("오류", str(e))

# GUI 창 생성
root = tk.Tk()
root.title("로봇 자유도 계산기")

tk.Label(root, text="링크 수:").grid(row=0, column=0)
entry_links = tk.Entry(root)
entry_links.grid(row=0, column=1)

tk.Label(root, text="관절 수:").grid(row=1, column=0)
entry_joints = tk.Entry(root)
entry_joints.grid(row=1, column=1)

tk.Label(root, text="각 관절 자유도(쉼표로 구분):").grid(row=2, column=0)
entry_dofs = tk.Entry(root)
entry_dofs.grid(row=2, column=1)

btn_calculate = tk.Button(root, text="자유도 계산", command=calculate_dof)
btn_calculate.grid(row=3, columnspan=2, pady=10)

label_result = tk.Label(root, text="계산된 자유도: ")
label_result.grid(row=4, columnspan=2)

root.mainloop()