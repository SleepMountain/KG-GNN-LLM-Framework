import json
import torch
from torch_geometric.data import Data, DataLoader
from GNNBuild import SemanticAwareGNN 
courses_json_path = 'courses.json'
students_json_path = 'students.json'
tokenizer_json_path = 'tokenizer.json'

tokenizer = {}

with open(courses_json_path, 'r') as f:
    courses_data = json.load(f)

with open(students_json_path, 'r') as f:
    students_data = json.load(f)

tokenizer_id = 0
courses_encoder = []
knowledge_points_encoder = []
all_courses = list(courses_data.keys())
all_knowledge_points = []
for course in all_courses:
    tokenizer[tokenizer_id] = course
    tokenizer_id += 1
    courses_encoder.append(tokenizer_id)
    for kp in courses_data[course]:
        if kp not in all_knowledge_points:
            all_knowledge_points.append(kp)
            tokenizer[tokenizer_id] = kp
            tokenizer_id += 1
            courses_encoder.append(tokenizer_id)
            
with open(tokenizer_json_path, 'w') as f:
    json.dump(tokenizer, f)
                

edge_index = []
x = []

for course, kps in courses_data.items():
    course_id = courses_encoder[course]
    for kp in kps:
        kp_id = courses_encoder[kp]
        edge_index.append([course_id, kp_id])
        edge_index.append([kp_id, course_id]) 

edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
x = torch.eye(len(tokenizer)) 


model = SemanticAwareGNN(num_node_features=x.size(1), hidden_channels=64)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.CrossEntropyLoss()

right_same_courses = []
for student in students_data:
    courses = students_data[student]
    tokenizer_courses = []
    for course in courses:
        tokenizer_courses.append(courses_encoder[course])
    right_same_courses.append(tokenizer_courses)
    
data_loader = DataLoader(right_same_courses, batch_size=32, shuffle=True)
for epoch in range(200):
    model.train()
    for data in data_loader: 
        out = model(x, edge_index, data)
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    print(f'Epoch {epoch}, Loss: {loss.item()}')

torch.save(model.state_dict(), 'model.pth')