import torch
from GNNBuild import SemanticAwareGNN 
import json
import numpy as np
model = SemanticAwareGNN(in_channels=10, out_channels=64)  
model.load_state_dict(torch.load("model.pth"))
model.eval()

tokenizer_json_path = 'tokenizer.json'
courses_json_path = 'courses.json'

with open(courses_json_path, 'r') as f:
    courses_data = json.load(f)

with open(tokenizer_json_path, 'r') as f:
    tokenizer = json.load(f)

all_courses = list(courses_data.keys())
all_knowledge_points = [kp for sublist in courses_data.values() for kp in sublist]

example_student_knowledge_points = ['知识点1', '知识点2']
example_kp_ids = [tokenizer[kp] for kp in example_student_knowledge_points]

x = torch.eye(len(all_courses) + len(all_knowledge_points))  
edge_index = []
for kp_id in example_kp_ids:
    for course_id in range(len(all_courses)):
        edge_index.append([course_id, kp_id])
        edge_index.append([kp_id, course_id])  

edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()

with torch.no_grad():
    out = model(x, edge_index, None)  
    predictions = torch.softmax(out, dim=1)

predicted_courses_ids = predictions.topk(10).indices
predicted_courses = [tokenizer[str(course_id)] for course_id in predicted_courses_ids]

print("推荐的课程:", predicted_courses)