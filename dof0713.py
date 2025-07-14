def calculate_dof(num_links, num_joints, joint_dofs):
    m = 6# 3D 공간에서 링크가 가질 수 있는 최대 자유도는 6
    
    # Grubler's Formula 적용
    F = m * (num_links - num_joints - 1) + sum(joint_dofs)
    
    return F

# 사용자 입력 받기
num_links=int(input("링크의 개수를 입력하세요: "))
num_joints=int(input("조인트의 개수를 입력하세요: "))

# 각 관절이 가지는 자유도 입력 받기
joint_dofs = []
for i in range(num_joints):
    dof = int(input(f"{i + 1}번 관절의 자유도를 입력하세요: "))
    joint_dofs.append(dof)

# 자유도 계산
dof = calculate_dof(num_links, num_joints, joint_dofs)
print(f"계산된 자유도: {dof}")