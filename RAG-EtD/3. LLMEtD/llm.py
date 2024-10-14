from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
import sys
sys.path.append('..')
sys.path.append('../..')
from env_loader import GetEnv
from QwenLLM import Qwen
import json
import os

with open("../../data/json/CK.json", "r") as f:
    CK = json.load(f)

TargetClassName = ["Web基础","《统万城》导读"]
PossibleCourses = [
  '高级语言程序设计',
  'C语言程序设计',
  'C++语言程序设计基础',
  '微积分',
  '组合数学',
  'Web安全实践',
  '网络安全概述',
  '工程热力学（下）',
  'Python 交互式程序设计导论',
  '界面设计导论',
  '微积分——极限理论与一元函数',
  '动态几何'
]

#Above is the data that should be loaded after 1/2 Steps.

TargetClassKP = []

PossibleCoursesWithSameKP = {}

for TC in TargetClassName:
    TCCK = CK[TC]
    for kp in TCCK:
        if kp not in TargetClassKP:
            TargetClassKP.append(kp)
    

for course in PossibleCourses:
    for kp in CK[course]:
        if kp in TargetClassKP:
            if course not in PossibleCoursesWithSameKP:
                PossibleCoursesWithSameKP[course] = []
            PossibleCoursesWithSameKP[course].append(kp)

ClassesWithKnoeledgePointsAndNumbers = ""
for course in PossibleCourses:
    ClassesWithKnoeledgePointsAndNumbers += "{}（理由：有{}门已选择课程中{}个知识点和该课程相同，分别是：{}）\n".format(
        course,
        len(PossibleCoursesWithSameKP[course]),
        len(CK[course]),
        "、".join(CK[course])
)
#Use Chinese because the model was fine-tuned with Chinese data.
PROMPT = """
现在，你已经选择了{}，接下来我将给你列举10门课程，每门课程都会给出相关的知识点，请去除最不相关的4门课程。
{}
""".format(
    "、".join(TargetClassName),
    ClassesWithKnoeledgePointsAndNumbers
)
LLM_PATH = GetEnv("llm_path")
llm = Qwen()
llm.load_model(LLM_PATH)
llm.set_stream_callbackers([print])

#Using agent because our llm was ready to fine-tuned with structured chat data(aslo agent RAG).
SYSTEM_PROMT = """
现在你是一个选课助手，接下来我将给你列举10门课程，每门课程都会给出选择的理由，请去除最不相关的4门课程。
选择的理由来自原先学生选择的课程，以及原有课程和新课程的相同知识点。
注意，不是越靠后的课程越不相关，请仔细分析理由，比对新课程知识点和目标课程知识点的差异。

你可以使用以下工具: {tool_names}
以上工具的详细使用说明如下：
{tools}
如果你想要输出使用工具，请输出:
{{"action":"工具名","action_input":"工具参数"}}
当你想要输出最终答案时，请输出：
{{"action":"Final Answer","action_input":"(回复给user的内容)"}}

例如：
1. 高级语言程序设计（理由：有3门已选择课程中11个知识点和该课程相同，分别是：C语言程序设计(预处理器、文件操作、联合体、结构体、指针、函数、控制结构)、软件工程(模块化)、Web基础(函数、数据类型、控制结构)）
2. Python 交互式程序设计导论（理由：有7门已选择课程中7个知识点和该课程相同，分别是：系统化产品设计与开发(团队协作)、数学建模(团队协作)、电子信息科学与技术导引(数据结构)、数据结构(数据结构)、Java程序设计(封装)、C语言程序设计(函数)、Web基础(函数)）
3. 中级管理会计（理由：有5门已选择课程中7个知识点和该课程相同，分别是：数据结构(大数据)、新媒体编创(跨文化)、通用学术英语(跨文化)、工程职业伦理(跨文化)、系统化产品设计与开发(风险管理、成本效益分析、预算管理)）
4. 程序设计基础（理由：有4门已选择课程中7个知识点和该课程相同，分别是：数据结构(递归算法、动态规划、查找算法、排序算法)、数学建模(动态规划)、C语言程序设计(结构体)、电子信息科学与技术导引(程序设计)）
5. 商学导论：10节课带你走进商业世界（理由：有4门已选择课程中6个知识点和该课程相同，分别是：新媒体编创(跨文化)、通用学术英语(跨文化)、工程职业伦理(跨文化)、创业启程(人力资源管理、市场营销、财务管理)）
6. C++语言程序设计基础（理由：有4门已选择课程中5个知识点和该课程相同，分别是：Java程序设计(I/O)、C语言程序设计(指针、函数)、Web基础(函数)、电子信息科学与技术导引(程序设计)）
7. 日语与日本文化（理由：有4门已选择课程中5个知识点和该课程相同，分别是：新媒体编创(跨文化)、通用学术英语(跨文化、语言学)、工程职业伦理(跨文化)、汉语文字词汇(语言学)）
8. 创业导引——与创业名家面对面（理由：有3门已选择课程中5个知识点和该课程相同，分别是：创业启程(品牌建设、市场营销)、系统化产品设计与开发(产品设计、团队协作)、数学建模(团队协作)）
9. 思想道德修养与法律基础（中南大学）（理由：有2门已选择课程中5个知识点和该课程相同，分别是：毛泽东思想和中国特色社会主义理论体系概论(中国特色社会主义)、思想道德修养与法律基础(中国特色社会主义、爱国主义、社会主义核心价值观、人生观)）
10. 设计的人因与文化（理由：有4门已选择课程中4个知识点和该课程相同，分别是：新媒体编创(跨文化)、通用学术英语(跨文化)、工程职业伦理(跨文化)、交互设计(用户研究)）

思考：
创业导引——与创业名家面对面：此课程虽然包含了品牌建设、市场营销、产品设计等与创业相关的知识点，但与其他课程相比，它更侧重于创业精神和战略规划的理论学习，而不是技术或编程技能的直接提升。因此，对于追求技术或编程深化的学生而言，它的相关性可能不如其他课程。
中级管理会计：虽然这门课程与已选课程有7个知识点相同，但这些知识点（如大数据、跨文化、风险管理等）更偏向于管理和财务分析，与会计专业知识的联系不如其他课程紧密。因此，相较于其他更偏向技术或编程的课程，中级管理会计的相关性较低。
商学导论：10节课带你走进商业世界：该课程主要介绍商业世界的基础知识，包括人力资源管理、市场营销、财务管理等。尽管这些知识对于理解商业环境很重要，但如果学生的主要目标是加强技术、编程或具体的管理技能，这门课程相较于其他选项可能显得不够专业或深入。
日语与日本文化：尽管有诸多跨文化、语言学知识点与已选课程相同，但是以及选择的跨语言课程主要是英语，考虑到语种的差异远大于知识点，故去除。
思想道德修养与法律基础（中南大学）：尽管与技术、编程或具体专业技能差异较大，但该课能够培养学生的价值观和道德观念，相较于日语这门课还是更适合学生选择。
Python 交互式程序设计导论：Python与Java、C语言差异较大，但考虑到已经去除了课程会计、商学导论、创业指引和日语四门课程，相对比起来相关性强于前四者，故在此情况下不用去除。
C++语言程序设计基础：C与C++还是有一定关系的，考虑到知识点较为接近，不用去除。

输出：
{{"action":"Final Answer","action_input":"3,5,7,8"}}

无论如何，你都应当以JSON的格式输出（只需要输出一次），输出json后请不要输出其他任何文本。现在，请回答user的问题。
"""
BASE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMT),
    ("human", "{input}\n{agent_scratchpad}")
])
agent = create_structured_chat_agent(llm=llm, prompt=BASE_PROMPT,tools=[])
agent_executor = AgentExecutor(agent=agent,tools=[])
ans = agent_executor.invoke({
    "input": PROMPT
})
print(ans["output"])
