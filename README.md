# KG-GNN-LLM-Framework

**instruction：** The repository provides partial code support for the paper: "Research on an Intelligent Course Selection Recommendation System for Colleges and Universities Based on Automatic Completion Knowledge Graph Fusion GNN-LLM Collaborative Framework," and is under continuous improvement.

  <h3 align="center">“Research on an Intelligent Course Selection Recommendation System for Colleges and Universities Based on Automatic Completion Knowledge Graph Fusion GNN-LLM Collaborative Framework”</h3>
  <p align="center">
   Zhouxuan Chen · Gang Cen · ShuaiJie Jiang · YuFan Chen 
    <br />
  </p>



## Contents

- Guide
  - Installation
- File Directory Description
- Architecture of Development
- Contributors
  - How to Participate
- Versioning
- License
### Guide

###### Installation

```sh
$git clone https://github.com/SleepMountain/KG-GNN-LLM-Framework.git
$pip install -r requirements.txt
```

### File Directory Description

```
Repository Root 
├──KG
│  ├──neo4j
│  │  ├──C-K-P.py
│  │  ├──S-C.py
│  │  ├──S-C_train.py
│  │  ├──add_AKB.py
│  │  ├──clear.py
│  │  ├──delete_AKB.py
│  │  └──link.py
│  └──prepare_data
│  │  ├──data_spider.py
│  │  └──max_cut.py
├──RAG-EtD
│  ├──1. SimpleSort
│  │  └──sort.js
│  ├──2. GNNPruned
│  │  ├──GNNBuild.py
│  │  ├──inference.py
│  │  └──train.py
│  ├──3. LLMEtD
│  │  └──llm.py
│  ├──QwenLLM.py
│  ├──buildJsonFromCKR.js
│  └──n4j.py
├──data
│  ├──csv
│  │  ├──Course - Knowledge Points - Related Courses.csv
│  │  ├──Student - Course Selection (Edited).csv
│  │  ├──Student - Course Selection (Test Set).csv
│  │  └──Student - Course Selection.csv
│  ├──export
│  │  ├──export4.csv
│  │  └──export5.csv
│  ├──json
│  │  └──CK.json
│  ├──neo4j
│  │  ├──neo4j1.dump
│  │  ├──neo4j2.dump
│  │  ├──neo4j3.dump
│  │  ├──neo4j4.dump
│  │  └──neo4j5.dump
│  └──records
│  │  ├──records1.json
│  │  ├──records2.json
│  │  └──records3.json
├──README.md
├──build_file_dir.js
├──LICENSE
├──env_loader.py
├──package.json
├──.env.example
└──requirements.txt
```

### Architecture of Development 

Please read [README.md](https://github.com/SleepMountain/KG-GNN-LLM-Framework/blob/main/README.md) to review the architecture of this project.。



### Contributors

The developers who have contributed to this project: [ZhouxuanChen](https://github.com/SleepMountain) ; [YufanChen](https://github.com/ChenYFan) ; [ShuaijieJiang](https://github.com/JackComputer553)。



#### How to Participate

Contributions help make the open-source community an amazing place to learn, get inspired, and create. Any contributions you make are **greatly appreciated**.


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



### Versioning

The project uses Git for version control. You can view the currently available versions in the repository.



### Author

3224039710@qq.com

qq:3224039710

 *You can also view all the developers who contributed to this project in the contributors' list.*


### License

[`GNU General Public License v3.0`](LICENSE)


