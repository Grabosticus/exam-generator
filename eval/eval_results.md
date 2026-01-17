
This document contains **all evaluation artifacts** pasted in the conversation, rewritten as **valid, clean JSON** (no trailing commas, proper quoting, and all multiline strings normalized using `\n` escapes).

---

## AIC — Slide Retrievals: Serverless Computing (@k=5)

~~~json
[
  {
    "text": "Serverless Computing\n18",
    "metadata": {
      "material_type": "slides",
      "topic": "unknown",
      "page_end": 18,
      "chunk_ind": 17,
      "has_images": true,
      "ocr_used": false,
      "char_len": 23,
      "course_id": "1",
      "page_start": 18,
      "ocr_language": "",
      "relevancy_score": 0.5860925912857056
    }
  },
  {
    "text": "Serverless Computing – Developer \nPerspective\n• Provide the piece of business logic you want executed as a function \nand upload it to the cloud provider\n• basically a function (and helper functions)\n• mainstream programming languages supported (e.g., Java, C#, Python)\n• Define mappings for inputs and outputs (from/to other cloud services)\n• e.g., cloud-based storage or cloud-based DBs, messages/queues, monitored events\n• Define metadata, e.g.,:\n• triggers (logical condition when the function should be executed)\n• runtime parameters (e.g., timeouts, memory requirements)\n• failure strategies (what to do on an error - retry, fail?)\n20",
    "metadata": {
      "course_id": "1",
      "has_images": true,
      "material_type": "slides",
      "topic": "unknown",
      "ocr_used": false,
      "char_len": 639,
      "page_end": 20,
      "page_start": 20,
      "ocr_language": "",
      "chunk_ind": 19,
      "relevancy_score": 0.5435346961021423
    }
  },
  {
    "text": "Serverless Computing – Use Cases\n• Functions - Simple and cheaper, if the use case is right\n• (e.g., serving HTTP requests, batch processing, IoT data processing)\n21",
    "metadata": {
      "page_end": 21,
      "material_type": "slides",
      "has_images": true,
      "ocr_used": false,
      "page_start": 21,
      "topic": "unknown",
      "course_id": "1",
      "ocr_language": "",
      "char_len": 165,
      "chunk_ind": 20,
      "relevancy_score": 0.5395837426185608
    }
  },
  {
    "text": "Serverless Computing\n• Serverless Computing – “a cloud computing execution model in which the cloud provider dynamically \nmanages the allocation of machine resources.” (Wikipedia)\n• Serverless does not mean that servers/machines/containers are not deployed \nto execute your code, but the deployment is handled by the cloud provider \ntransparently \n• Typically in the form of Function-as-a-Service (FaaS) combined with Backend-as-a-Service (BaaS)\n• Commercial offerings: AWS Lambda, Google Cloud Functions, Microsoft Azure Functions\n• Open-source alternatives: OpenWhisk, OpenFaaS\n• Notice the trend:\nmanage hardware >> manage VMs >> manage containers >> manage code/logic\n19",
    "metadata": {
      "has_images": true,
      "course_id": "1",
      "char_len": 674,
      "ocr_used": false,
      "page_end": 19,
      "topic": "unknown",
      "chunk_ind": 18,
      "material_type": "slides",
      "ocr_language": "",
      "page_start": 19,
      "relevancy_score": 0.5353929400444031
    }
  },
  {
    "text": "How about vendor lock-in?\n● Use of the platform tools/APIs of a specific vendor makes life easier\n● But is this vendor the most suitable & cost-effective one?\n● How about combining resources/offerings of multiple providers?\n○ Exploit price variations – pick most cost-effective provider for given workload\n○ Expand free tier\n○ Parallel deployment for better scalability/performance\n● New challenges:\n○ Scheduling functions across providers\n○ Duplicate implementations using different SDKs\n○ Cross provider communication may be inefficient\n30\nA.F. Baarzi et al., “On merits and viability of multi-cloud serverless,” Proc. ACM SoCC, 2021.\nT. Larcher et al., “BAASLESS: Backend-as-a-Service (BaaS)-Enabled Workflows in Federated Serverless Infrastructures,” IEEE TCC, 2024.",
    "metadata": {
      "page_start": 30,
      "ocr_used": false,
      "course_id": "1",
      "topic": "unknown",
      "chunk_ind": 29,
      "char_len": 770,
      "has_images": true,
      "ocr_language": "",
      "page_end": 30,
      "material_type": "slides",
      "relevancy_score": 0.5231425166130066
    }
  }
]
~~~

---

## AIC — Old Exam Questions: Cloud Computing (set)

~~~json
[
  {
    "question": "Single-Choice: An IoT application is in charge of continuously collecting data from thousands of environmental sensors distributed over a country, performing some initial filtering of the data to detect faulty sensor readings, and storing them for future processing. Where would you host the data filtering functionality?",
    "question_type": "single-choice",
    "answer_keys": [
      "a. On the cloud",
      "b. At the edge"
    ],
    "metadata": {
      "difficulty": "unknown",
      "question_number": 14,
      "topic": "unknown",
      "chunk_ind": 13,
      "char_len": 372,
      "has_choices": true,
      "page_end": 2,
      "course_id": "1",
      "page_start": 2,
      "ocr_languages_used": "",
      "ocr_used": false,
      "relevancy_score": 0.46298491954803467
    }
  },
  {
    "question": "True or False: Cloud computing is beneficial when considering the use case of batch computational workloads.",
    "question_type": "single-choice",
    "answer_keys": [
      "a. True",
      "b. False"
    ],
    "metadata": {
      "page_end": 2,
      "char_len": 145,
      "page_start": 2,
      "ocr_used": false,
      "has_choices": true,
      "chunk_ind": 9,
      "question_number": 10,
      "ocr_languages_used": "",
      "course_id": "1",
      "topic": "unknown",
      "difficulty": "unknown",
      "relevancy_score": 0.38136374950408936
    }
  },
  {
    "question": "Single-Choice: Consider a cloud provider that offers Function-as-a-Service, where every function is executed in isolation within a Docker container. For a given function, the docker container is deleted if the function has not been invoked for 300 seconds and is re-launched upon the next function invocation. Consider also the following applications. Application A: An IoT device senses a temperature value periodically every 10 minutes and sends this value to a cloud application instance. When the application instance receives it, a serverless function is triggered that performs a sanity check on the temperature value and stores it in a cloud-based key- value store. Assume that each IoT device belongs to a single cloud tenant, who has deployed a dedicated cloud application instance and a dedicated serverless function to serve the requests of this specific IoT device. Application B: A camera placed at a traffic light takes a photo of the license plate of every car that crosses it when the traffic light is green, and uploads it to a cloud application. When a photo is received by the application, a serverless function is triggered that scans the license plate number and stores it in a database. The traffic light follows a cycle of 40 seconds for the green signal and 20 seconds for the red one. During the least busy hours, at least two cars cross the traffic light when it is green. Which application is expected to face more cold-start latencies?",
    "question_type": "single-choice",
    "answer_keys": [
      "a. Application A",
      "b. Application B",
      "Calculation:",
      "Assume a scenario where 3 mobile devices participate in a federated learning task. Before a given training round, the server selects a subset of these devices, which will then perform training on their local data and submit model updates to the server. It is possible that a selected device fails to submit a report at the end of the round (e.g., it may run out of battery during the process, lose its connectivity, etc.). For each device, the probability that it successfully delivers its report in a round is given below:",
      "Device 1: p1 = 0.1",
      "Device 2: p2 = 0.6",
      "Device 3: p3 = 0.4",
      "At the same time, each device has a fixed cost to participate in a round. If selected, the cost of each device is given below:",
      "Device 1: c1 = 10",
      "Device 2: c2 = 2",
      "Device 3: c3 = 20",
      "The server needs to select the subset of devices to participate in the round which minimizes the total cost, under the constraint that the expected number of reports that will be received by the server is at least E = 1. (The total cost is defined as the sum of the costs of all devices that participate in a round. If a device is not selected, it does not contribute to the overall cost.)",
      "Prüfung 2022-12-21 Random Questions from Exam AIC",
      "4",
      "(a) What is the optimal subset of devices that the server should select? Provide your answer in the following format: (X,Y,...). For example, if the server selects devices 1 and 3, your answer should be (1,3), if the server selects device 2 your answer should be (2), etc. If there is no feasible solution, your answer should be (). This format is strict: Do not use whitespace characters in your answer; keep the paretheses.",
      "(b) What is the cost of the optimal solution? Provide a numerical value. If there is no feasible solution, answer with 0.",
      "(c) What is the expected number of reports that the server will receive in this round under the optimal solution? Provide a numerical value. If there is no feasible solution, answer with 0."
    ],
    "metadata": {
      "topic": "unknown",
      "chunk_ind": 16,
      "question_number": 17,
      "course_id": "1",
      "page_end": 3,
      "ocr_used": false,
      "ocr_languages_used": "",
      "has_choices": true,
      "page_start": 3,
      "difficulty": "unknown",
      "char_len": 3652,
      "relevancy_score": 0.3552529811859131
    }
  },
  {
    "question": "Single-Choice: A cancer research institute provides services of DNA (genome) analysis for patients of nearby hospitals. This requires running a genome sequencing analysis on each of the samples independently. Assume that each individual sample analysis can be handled by a single large-memory Amazon EC2 VM instance. The institute’s primary concern is to serve requests for DNA analysis as fast as possible, to return results to hospitals it serves. Based on the provided information, which EC2 instance type would you use to implement the described use-case? Select the one that is most applicable.",
    "question_type": "single-choice",
    "answer_keys": [
      "a. Dedicated",
      "b. Reserved",
      "c. On-demand",
      "d. Spot instance"
    ],
    "metadata": {
      "ocr_used": false,
      "course_id": "1",
      "page_start": 2,
      "topic": "unknown",
      "char_len": 686,
      "ocr_languages_used": "",
      "page_end": 2,
      "has_choices": true,
      "difficulty": "unknown",
      "question_number": 15,
      "chunk_ind": 14,
      "relevancy_score": 0.34654974937438965
    }
  },
  {
    "question": "Single-Choice: Consider an application where IoT devices are equipped with sensors and cameras. When the sensor of the device senses an event, its camera captures a high-definition image and sends it over the network to a server for processing. Sensing events take place with a frequency of 20 per minute on Prüfung 2022-12-21 Random Questions from Exam AIC 3 average, and the size of each transmitted image is 10 MB. Which of the following networking technologies is more appropriate to connect an IoT device?",
    "question_type": "single-choice",
    "answer_keys": [
      "a. LoRaWAN",
      "b. NB-IoT",
      "c. Wi-Fi"
    ],
    "metadata": {
      "ocr_used": false,
      "chunk_ind": 15,
      "question_number": 16,
      "course_id": "1",
      "ocr_languages_used": "",
      "char_len": 566,
      "has_choices": true,
      "topic": "unknown",
      "difficulty": "unknown",
      "page_end": 2,
      "page_start": 2,
      "relevancy_score": 0.3112252950668335
    }
  }
]
~~~

---

## AIC — Generated Exam — Topic: Cloud Computing (serverless questions)

~~~json
{
  "course_id": 1,
  "course_name": "AIC",
  "topics": "cloud computing",
  "n_requested": 5,
  "n_generated": 5,
  "context": {
    "course_material_chunks": 15,
    "old_exam_questions": 15
  },
  "questions": [
    {
      "question": "True or False: In serverless computing, the scale-to-zero principle means that when a function is not being invoked, no virtual resources are allocated and the user is not charged for idle time.",
      "question_type": "single-choice",
      "answer_keys": [
        "a. True",
        "b. False"
      ],
      "metadata": {
        "topic": "Serverless Computing",
        "difficulty": "easy"
      }
    },
    {
      "question": "Single-Choice: A startup company is developing a mobile application that processes user-uploaded images to detect objects. The image processing workload is highly variable - sometimes hundreds of images are uploaded per minute, other times there are no uploads for hours. The processing of each image is independent and takes approximately 30 seconds. Which cloud computing model would be most cost-effective for this use case?",
      "question_type": "single-choice",
      "answer_keys": [
        "a. Virtual Machines with auto-scaling",
        "b. Function-as-a-Service (FaaS)",
        "c. Dedicated servers",
        "d. Reserved instances"
      ],
      "metadata": {
        "topic": "Serverless Computing",
        "difficulty": "medium"
      }
    },
    {
      "question": "Single-Choice: When deploying a serverless function that processes messages from a queue, which of the following metadata configurations is NOT typically required from a developer perspective?",
      "question_type": "single-choice",
      "answer_keys": [
        "a. Trigger conditions for function execution",
        "b. Memory requirements for the function",
        "c. Physical server location and hardware specifications",
        "d. Failure retry strategies"
      ],
      "metadata": {
        "topic": "Serverless Computing",
        "difficulty": "medium"
      }
    },
    {
      "question": "True or False: One of the main challenges of multi-cloud serverless deployments is that cross-provider communication may be inefficient and developers may need to duplicate implementations using different SDKs for each provider.",
      "question_type": "single-choice",
      "answer_keys": [
        "a. True",
        "b. False"
      ],
      "metadata": {
        "topic": "Serverless Computing",
        "difficulty": "easy"
      }
    },
    {
      "question": "Single-Choice: A company is evaluating serverless computing for their application. They are concerned about cold start latencies. Their application receives HTTP requests that trigger a serverless function performing database queries. The function is written in Python and requires 512 MB of memory. Requests arrive randomly throughout the day with gaps of up to 10 minutes between consecutive requests. What is the PRIMARY cause of cold start latency in this scenario?",
      "question_type": "single-choice",
      "answer_keys": [
        "a. The time required to execute the Python code",
        "b. The time required to launch a new VM/container with runtime libraries when the function hasn't been invoked recently",
        "c. The time required to perform database queries",
        "d. The time required to allocate 512 MB of memory"
      ],
      "metadata": {
        "topic": "Serverless Computing",
        "difficulty": "hard"
      }
    }
  ]
}
~~~

---

## AIC — Slide Retrievals: Edge Intelligence / Split Inference (@k=5)

~~~json
[
  {
    "text": "Split Inference  - Is it useful for MEC?\n \n67\n● Yes? No? Maybe?\n● Can we accommodate latency and performance critical applications?\n⇛  Provide constrained mobile clients access to “server-grade DNNs”\n● Offloading works just fine. \n○ Proximity matters? Just install more server grade hardware in proximity\n● Infrastructure continuously improving\n○ Ubiquitous availability of free Wi-Fi, 4G, 5G (Even in less developed \nplaces)\nSplit Inference",
    "metadata": {
      "ocr_language": "",
      "topic": "unknown",
      "char_len": 441,
      "course_id": "1",
      "chunk_ind": 66,
      "page_end": 67,
      "has_images": true,
      "ocr_used": false,
      "material_type": "slides",
      "page_start": 67,
      "relevancy_score": 0.37053728103637695
    }
  },
  {
    "text": "Split Inference  - Artificial Bottleneck Injection\n \n65\nSplit Inference",
    "metadata": {
      "page_start": 65,
      "has_images": true,
      "char_len": 71,
      "topic": "unknown",
      "course_id": "1",
      "material_type": "slides",
      "ocr_used": false,
      "ocr_language": "",
      "chunk_ind": 64,
      "page_end": 65,
      "relevancy_score": 0.3436150550842285
    }
  },
  {
    "text": "Split Inference  - Artificial Bottleneck Injection\n \n64\n● Same primary goal: Distributed load between client and server\n○ But emphasizes data reduction more than split runtimes\n● Modify the head model with:\n○ Quantization \n○ Pruning\n○ Dimensionality Reduction\n⇛ Alleviate reliance on Natural Bottleneck by “injecting” an autoencoder\n● Put some effort into opening the black box\n○ How do we train the injected parameters?\nSplit Inference",
    "metadata": {
      "page_start": 64,
      "ocr_used": false,
      "course_id": "1",
      "has_images": true,
      "material_type": "slides",
      "topic": "unknown",
      "page_end": 64,
      "char_len": 436,
      "chunk_ind": 63,
      "ocr_language": "",
      "relevancy_score": 0.3355265259742737
    }
  },
  {
    "text": "Advanced Internet \nComputing\nWS 2025/2026",
    "metadata": {
      "page_start": 1,
      "ocr_used": false,
      "char_len": 41,
      "material_type": "slides",
      "has_images": true,
      "topic": "unknown",
      "chunk_ind": 0,
      "ocr_language": "",
      "page_end": 1,
      "course_id": "1",
      "relevancy_score": 0.3308699131011963
    }
  },
  {
    "text": "Propaganda\n \n73\n● Yes? No? Maybe? \n● Can we accommodate latency and performance critical applications?\n⇛  Provide constrained mobile clients access to “server-grade DNNs”\n● Offloading works just fine. \n○ Proximity matters? Just install more server grade hardware in proximity\n● Infrastructure continuously improving\n○ Ubiquitous availability of free Wi-Fi, 4G, 5G (Even in less developed \nplaces)\nPropaganda",
    "metadata": {
      "chunk_ind": 72,
      "char_len": 407,
      "has_images": true,
      "course_id": "1",
      "page_end": 73,
      "page_start": 73,
      "ocr_used": false,
      "ocr_language": "",
      "material_type": "slides",
      "topic": "unknown",
      "relevancy_score": 0.32834410667419434
    }
  }
]
~~~

---

## AIC — Old Exam Questions: Edge / FL / MEC mix (@k=5)

~~~json
[
  {
    "question": "Single-Choice: An IoT application is in charge of continuously collecting data from thousands of environmental sensors distributed over a country, performing some initial filtering of the data to detect faulty sensor readings, and storing them for future processing. Where would you host the data filtering functionality?",
    "question_type": "single-choice",
    "answer_keys": [
      "a. On the cloud",
      "b. At the edge"
    ],
    "metadata": {
      "ocr_used": false,
      "page_start": 2,
      "has_choices": true,
      "char_len": 372,
      "topic": "unknown",
      "course_id": "1",
      "question_number": 14,
      "page_end": 2,
      "chunk_ind": 13,
      "ocr_languages_used": "",
      "difficulty": "unknown",
      "relevancy_score": 0.34299880266189575
    }
  },
  {
    "question": "True or False: Within federated machine learning, some private information may be inferred even if devices do not transmit the actual data.",
    "question_type": "single-choice",
    "answer_keys": [
      "a. True",
      "b. False"
    ],
    "metadata": {
      "difficulty": "unknown",
      "char_len": 176,
      "course_id": "1",
      "ocr_used": false,
      "has_choices": true,
      "topic": "unknown",
      "chunk_ind": 4,
      "question_number": 5,
      "page_end": 1,
      "ocr_languages_used": "",
      "page_start": 1,
      "relevancy_score": 0.27775371074676514
    }
  },
  {
    "question": "Single-Choice: A cancer research institute provides services of DNA (genome) analysis for patients of nearby hospitals. This requires running a genome sequencing analysis on each of the samples independently. Assume that each individual sample analysis can be handled by a single large-memory Amazon EC2 VM instance. The institute’s primary concern is to serve requests for DNA analysis as fast as possible, to return results to hospitals it serves. Based on the provided information, which EC2 instance type would you use to implement the described use-case? Select the one that is most applicable.",
    "question_type": "single-choice",
    "answer_keys": [
      "a. Dedicated",
      "b. Reserved",
      "c. On-demand",
      "d. Spot instance"
    ],
    "metadata": {
      "page_start": 2,
      "char_len": 686,
      "topic": "unknown",
      "course_id": "1",
      "chunk_ind": 14,
      "difficulty": "unknown",
      "has_choices": true,
      "question_number": 15,
      "ocr_languages_used": "",
      "page_end": 2,
      "ocr_used": false,
      "relevancy_score": 0.2624462842941284
    }
  },
  {
    "question": "True or False: According to the ETSI standard specifications for Multi-access Edge Computing, when a customer selects to create an application instance via a Customer Facing Service portal, the application package should have already been onboarded.",
    "question_type": "single-choice",
    "answer_keys": [
      "a. True",
      "b. False"
    ],
    "metadata": {
      "chunk_ind": 5,
      "course_id": "1",
      "difficulty": "unknown",
      "page_start": 1,
      "topic": "unknown",
      "char_len": 286,
      "has_choices": true,
      "ocr_languages_used": "",
      "ocr_used": false,
      "page_end": 1,
      "question_number": 6,
      "relevancy_score": 0.2543048858642578
    }
  },
  {
    "question": "True or False: When network neutrality is not enforced, IoT service providers can team up with network operators so that their services' traffic is preferentially treated.",
    "question_type": "single-choice",
    "answer_keys": [
      "a. True",
      "b. False"
    ],
    "metadata": {
      "question_number": 12,
      "char_len": 208,
      "course_id": "1",
      "ocr_languages_used": "",
      "topic": "unknown",
      "difficulty": "unknown",
      "chunk_ind": 11,
      "ocr_used": false,
      "page_start": 2,
      "page_end": 2,
      "has_choices": true,
      "relevancy_score": 0.2389346957206726
    }
  }
]
~~~

---

## AIC — Generated Exam — Topic: Edge Intelligence

~~~json
{
  "course_id": 1,
  "course_name": "AIC",
  "topics": "edge intelligence",
  "n_requested": 5,
  "n_generated": 5,
  "context": {
    "course_material_chunks": 15,
    "old_exam_questions": 15
  },
  "questions": [
    {
      "question": "True or False: In Split Inference, the primary goal of Artificial Bottleneck Injection is to reduce data transfer costs by modifying the head model with techniques such as quantization, pruning, and dimensionality reduction.",
      "question_type": "single-choice",
      "answer_keys": [
        "a. True",
        "b. False"
      ],
      "metadata": {
        "topic": "Split Inference",
        "difficulty": "medium"
      }
    },
    {
      "question": "Single-Choice: In Split Inference for Mobile Edge Computing (MEC), there are two competing concerns that must be balanced. Which of the following best describes these concerns?",
      "question_type": "single-choice",
      "answer_keys": [
        "a. Distribute Load and Reduce Transfer Costs",
        "b. Increase Accuracy and Reduce Latency",
        "c. Maximize Throughput and Minimize Energy Consumption",
        "d. Enhance Security and Improve Privacy"
      ],
      "metadata": {
        "topic": "Split Inference",
        "difficulty": "medium"
      }
    },
    {
      "question": "True or False: In Hierarchical Federated Learning (HFL), edge aggregators communicate with the global server more frequently than individual clients communicate with edge aggregators.",
      "question_type": "single-choice",
      "answer_keys": [
        "a. True",
        "b. False"
      ],
      "metadata": {
        "topic": "Federated Learning",
        "difficulty": "easy"
      }
    },
    {
      "question": "Single-Choice: According to the course material on Split Inference, when there is strong resource asymmetry between the client and server, what primarily determines the usefulness of a split approach?",
      "question_type": "single-choice",
      "answer_keys": [
        "a. The ability to distribute computational load evenly",
        "b. The ability to reduce transfer cost",
        "c. The ability to improve model accuracy",
        "d. The ability to minimize server-side processing"
      ],
      "metadata": {
        "topic": "Split Inference",
        "difficulty": "medium"
      }
    },
    {
      "question": "True or False: In the context of Split Inference, dimensionality reduction is equivalent to compression because both reduce the size of data being transmitted.",
      "question_type": "single-choice",
      "answer_keys": [
        "a. True",
        "b. False"
      ],
      "metadata": {
        "topic": "Split Inference",
        "difficulty": "hard"
      }
    }
  ]
}
~~~

---

## GenAI — Slide Retrievals: Transformer (@k=5)

~~~json
[
  {
    "text": "#2A6495\nA bird's eye view of the\nTransformer Architecture.",
    "metadata": {
      "char_len": 58,
      "page_end": 55,
      "ocr_used": false,
      "ocr_language": "",
      "material_type": "slides",
      "has_images": true,
      "course_id": "3",
      "page_start": 55,
      "topic": "unknown",
      "chunk_ind": 54,
      "relevancy_score": 0.5112266540527344
    }
  },
  {
    "text": "#2A6495\nEncoder Decoder\nEncoder Block(s)\nDecoder Block(s)Model Head",
    "metadata": {
      "course_id": "3",
      "page_end": 61,
      "material_type": "slides",
      "has_images": true,
      "char_len": 67,
      "topic": "unknown",
      "chunk_ind": 60,
      "ocr_used": false,
      "ocr_language": "",
      "page_start": 61,
      "relevancy_score": 0.28765469789505005
    }
  },
  {
    "text": "#2A6495\nThe encoder transforms the input sequence into a \nrich, contextual vector representation that captures\nthe meaning of and relationships between\nelements.\nThe decoder takes the encoded input from the\nencoder and autoregressively generates an output\nsequence token by token, using previously\ngenerated tokens and the context of the encoder to\nproduce a transformed sequence (e.g. a translation\nor summary).",
    "metadata": {
      "course_id": "3",
      "char_len": 412,
      "ocr_language": "",
      "has_images": true,
      "chunk_ind": 56,
      "ocr_used": false,
      "page_start": 57,
      "topic": "unknown",
      "material_type": "slides",
      "page_end": 57,
      "relevancy_score": 0.2851097583770752
    }
  },
  {
    "text": "#2A6495\nEncoder Decoder\nEncoder Block\nDecoder Block",
    "metadata": {
      "ocr_used": false,
      "page_end": 58,
      "page_start": 58,
      "char_len": 51,
      "course_id": "3",
      "topic": "unknown",
      "ocr_language": "",
      "has_images": true,
      "chunk_ind": 57,
      "material_type": "slides",
      "relevancy_score": 0.2797338366508484
    }
  },
  {
    "text": "#2A6495\nted\ntline\ntting\nyl\ntoir\n,\n8%\n5%\n5%\n5%\n2%\n1%\n...\nLLM\nThe cute green dragon trot",
    "metadata": {
      "topic": "unknown",
      "ocr_language": "",
      "material_type": "slides",
      "page_start": 38,
      "char_len": 86,
      "page_end": 38,
      "ocr_used": false,
      "course_id": "3",
      "chunk_ind": 37,
      "has_images": true,
      "relevancy_score": 0.262159526348114
    }
  }
]
~~~

---

## GenAI — Old Exam Questions (mixed Transformer set of 5)

~~~json
[
  {
    "question": "## Frage 13 **What makes the transformer architecture well-suited to sequential data modelling?** ",
    "question_type": "single-choice",
    "answer_keys": [
      "- [ ] a. Other than previous architectures, transformers can generalize across previously unseen",
      "languages without further pretraining.",
      "- [ ] b. Their attention mechanism makes them highly interpretable and transparent, unlike",
      "previous \"black box\" architectures like LSTMs.",
      "- [ ] c. They need little to no training data to learn the highly contextual semantics of sequences",
      "such as language.",
      "- [x] d. They can learn patterns from multiple parts/subsequences of a sequence simultaneously,",
      "rather than processing it sequentially.",
      "- [ ] e. Transformers are speciﬁcally designed to handle ﬁxed-length sequences, enhancing their",
      "performance with sequential data.",
      "---"
    ],
    "metadata": {
      "course_id": "1",
      "question_number": 13,
      "ocr_used": false,
      "has_choices": true,
      "char_len": 833,
      "page_start": 4,
      "ocr_languages_used": "",
      "topic": "unknown",
      "difficulty": "unknown",
      "page_end": 4,
      "chunk_ind": 12,
      "relevancy_score": 0.3656153678894043
    }
  },
  {
    "question": "## Frage 11 **Which statement(s) about positional encoding in transformers is (are) INCORRECT?** ",
    "question_type": "single-choice",
    "answer_keys": [
      "- [ ] a. Positional encodings help to overcome the inherent permutation invariance of the attention",
      "mechanism.",
      "- [ ] b. Positional encodings enrich embedding vectors with information about the position of a",
      "token within its sequence.",
      "- [ ] c. The dimension of the positional encoding vectors scales with the dimension of the",
      "embedding layer.",
      "- [ ] d. It can use sinusoidal functions to encode position information.",
      "- [x] e. Positional encodings have to be learned during the training process.",
      "---"
    ],
    "metadata": {
      "question_number": 11,
      "course_id": "1",
      "chunk_ind": 10,
      "page_start": 3,
      "ocr_languages_used": "",
      "difficulty": "unknown",
      "has_choices": true,
      "ocr_used": false,
      "char_len": 655,
      "topic": "unknown",
      "page_end": 3,
      "relevancy_score": 0.26042163372039795
    }
  },
  {
    "question": "## Frage 12 **What deﬁnes a token in the context of LLMs?** ",
    "question_type": "single-choice",
    "answer_keys": [
      "- [ ] a. The concept of tokens does not have a speciﬁc meaning in the context of LLMs.",
      "- [ ] b. A higher dimensional numerical identiﬁer for the whole sequence.",
      "- [x] c. The atomic unit of language that a model processes. This can be a word, part of a word, or",
      "a character.",
      "- [ ] d. The dense vector representation of the atomic unit of language processed by a transformer.",
      "- [ ] e. The smallest semantic unit of a language, which is always a single character.",
      "---"
    ],
    "metadata": {
      "topic": "unknown",
      "ocr_languages_used": "",
      "char_len": 574,
      "ocr_used": false,
      "difficulty": "unknown",
      "question_number": 12,
      "has_choices": true,
      "page_end": 3,
      "chunk_ind": 11,
      "page_start": 3,
      "course_id": "1",
      "relevancy_score": 0.22505474090576172
    }
  },
  {
    "question": "## Frage 15 **What is the idea behind scaling the dot product QKᵀ in the attention mechanism?** *Attention(Q,K,V) = softmax(QKᵀ/√dₖ)V* ",
    "question_type": "multiple-choice",
    "answer_keys": [
      "- [ ] a. To allow for bidirectional attention ﬂow between tokens by normalizing the distance",
      "between sequence positions.",
      "- [ ] b. To reduce the model's memory footprint during training and inference.",
      "- [ ] c. To dynamically adjust the attention mechanism's output based on its input sequence",
      "length, allowing more evenly spread attention scores.",
      "- [x] d. To prevent attention scores from having extreme values in the softmax, which could lead to",
      "vanishing gradients.",
      "- [x] e. To normalize attention scores by counteracting the potential \"explosion\" of the dot",
      "products in high dimensions, ensuring a smoother softmax distribution.",
      "---"
    ],
    "metadata": {
      "ocr_languages_used": "",
      "chunk_ind": 14,
      "ocr_used": false,
      "difficulty": "unknown",
      "question_number": 15,
      "page_start": 4,
      "page_end": 4,
      "course_id": "1",
      "has_choices": true,
      "char_len": 837,
      "topic": "unknown",
      "relevancy_score": 0.15284985303878784
    }
  },
  {
    "question": "## Frage 1 **What is the purpose of the \"clip\" function in PPO's objective function?** *J(θ):=Et[min(rt(θ)At, clip(rt(θ), 1−ϵ, 1+ϵ)At)]* ",
    "question_type": "single-choice",
    "answer_keys": [
      "- [x] a. To limit the size of policy updates by keeping probability ratios within bounds.",
      "- [ ] b. To speed up the convergence of the optimization process by keeping action distribution",
      "within bounds.",
      "- [ ] c. To reduce memory requirements during training by trimming the policy updates to a ﬁxed",
      "scale.",
      "- [ ] d. To prevent numerical overﬂow during training by keeping probability ratios within bounds.",
      "- [ ] e. To trim the advantage estimates avoiding overly aggressive advantage estimations.",
      "---"
    ],
    "metadata": {
      "has_choices": true,
      "topic": "unknown",
      "page_end": 1,
      "course_id": "1",
      "char_len": 690,
      "difficulty": "unknown",
      "ocr_languages_used": "",
      "question_number": 1,
      "chunk_ind": 0,
      "ocr_used": false,
      "page_start": 1,
      "relevancy_score": 0.14071738719940186
    }
  }
]
~~~

---

## GenAI — Generated Exam — Topic: Transformer

~~~json
{
  "course_id": 1,
  "course_name": "GenAI",
  "topics": "transformer",
  "n_requested": 5,
  "n_generated": 5,
  "context": {
    "course_material_chunks": 15,
    "old_exam_questions": 15
  },
  "questions": [
    {
      "question": "## Question 1 **What is the primary role of the encoder in a Transformer architecture?**",
      "question_type": "single-choice",
      "answer_keys": [
        "a. To autoregressively generate output tokens one at a time based on previously generated tokens.",
        "b. To convert token IDs directly into probability distributions over the vocabulary.",
        "c. To transform the input sequence into a rich, contextual vector representation that captures the meaning and relationships between elements.",
        "d. To apply positional encodings to the output sequence ensuring proper token ordering."
      ],
      "metadata": {
        "topic": "Transformer Architecture",
        "difficulty": "medium"
      }
    },
    {
      "question": "## Question 2 **Which statement(s) about the decoder in an encoder-decoder Transformer is (are) CORRECT?**",
      "question_type": "multiple-choice",
      "answer_keys": [
        "a. The decoder processes the entire output sequence in parallel during training.",
        "b. The decoder generates output tokens autoregressively, using previously generated tokens and the encoder's context.",
        "c. The decoder operates independently from the encoder and does not use its output.",
        "d. The decoder can produce transformed sequences such as translations or summaries."
      ],
      "metadata": {
        "topic": "Transformer Architecture",
        "difficulty": "medium"
      }
    },
    {
      "question": "## Question 3 **What is the relationship between a token and its embedding in the context of LLMs?**",
      "question_type": "single-choice",
      "answer_keys": [
        "a. A token is a dense vector representation, while the embedding is the original text string.",
        "b. A token is assigned a unique ID from the vocabulary, which is then mapped to a dense vector in the embedding layer.",
        "c. Tokens and embeddings are identical concepts referring to the same numerical representation.",
        "d. The embedding dimension must always equal the vocabulary size for proper token representation."
      ],
      "metadata": {
        "topic": "Tokenization and Embeddings",
        "difficulty": "medium"
      }
    },
    {
      "question": "## Question 4 **Why are positional encodings necessary in Transformer architectures? Given the formulas: PE(pos,2i) = sin(pos/10000^(2i/d_model)) and PE(pos,2i+1) = cos(pos/10000^(2i/d_model))**",
      "question_type": "multiple-choice",
      "answer_keys": [
        "a. The embedding layer and attention mechanism are inherently permutation invariant without positional information.",
        "b. Positional encodings allow the model to distinguish between tokens at different positions in the sequence.",
        "c. They are required to reduce the computational complexity of the attention mechanism.",
        "d. The dimension of positional encoding vectors matches the embedding dimension to enable addition."
      ],
      "metadata": {
        "topic": "Positional Encoding",
        "difficulty": "hard"
      }
    },
    {
      "question": "## Question 5 **Consider the tokenization process for the sentence 'The cute green dragon trot ted into the cave' which produces token IDs: [72, 302, 902, 1041, 78, 15, 982, 5, 873]. What can be inferred about the tokenization strategy used?**",
      "question_type": "single-choice",
      "answer_keys": [
        "a. The tokenizer uses character-level tokenization, with each character mapped to a unique ID.",
        "b. The tokenizer uses word-level tokenization, with each complete word mapped to exactly one token.",
        "c. The tokenizer uses subword tokenization, as evidenced by 'trot' and 'ted' being split into separate tokens.",
        "d. The number of tokens always equals the number of words in the input sentence."
      ],
      "metadata": {
        "topic": "Tokenization",
        "difficulty": "medium"
      }
    }
  ]
}
~~~

---

## GenAI — Slide Retrievals: LLM-related (@k=5)

~~~json
[
  {
    "text": "#2A6495\nDiscriminative Models",
    "metadata": {
      "ocr_language": "",
      "char_len": 29,
      "topic": "unknown",
      "course_id": "1",
      "material_type": "slides",
      "page_start": 16,
      "has_images": false,
      "chunk_ind": 15,
      "ocr_used": false,
      "page_end": 16,
      "relevancy_score": 0.4558464288711548
    }
  },
  {
    "text": "#2A6495 The goal of generative language modelling is to capture the “true distribution of language”: 𝑝(𝑋)\nA few definitions:\n• 𝑉 … vocabulary of unique tokens 𝑠𝑖 ∈ 𝑉\n• 𝑛 … maximum sequence length\n• 𝑋 … space of all possible token sequences\n𝑋 = {(𝑠1, 𝑠2, … , 𝑠𝑘)|𝑠𝑖 ∈  𝑉, 0 ≤  𝑘 ≤  𝑛, 𝑘 ∈  ℤ} where 𝑘 is the sequence length\n• 𝑥 ∈ 𝑋 … a particular sequence of tokens\n• The probability of a given sequence 𝑥\n𝑝 𝑥 = 𝑝 𝑠1 ∙ 𝑝 𝑠2 𝑠1) ∙ 𝑝 𝑠3 𝑠1, 𝑠2) ∙ … ∙ 𝑝 𝑠𝑘 𝑠1, … , 𝑠𝑘−1)\n         = 𝑝 𝑠1 ∙ ς𝑖=2\n𝑘 𝑝(𝑠𝑖|𝑠1, … , 𝑠𝑖−1)\nThe probability of a sequence is the product of the probability of the first token and the conditional probabilities of each subsequent token given all previous tokens.",
    "metadata": {
      "topic": "unknown",
      "course_id": "1",
      "ocr_language": "",
      "ocr_used": false,
      "char_len": 680,
      "has_images": false,
      "page_start": 25,
      "chunk_ind": 24,
      "material_type": "slides",
      "page_end": 25,
      "relevancy_score": 0.42272651195526123
    }
  },
  {
    "text": "#2A6495\nA rt i fi c ia l I nt e ll ige n ce\nS u bs y mb oli c  AI\nStatiscial Methods Ensemble \nTechniques Neural Networks …\nGenerative\nModels\nDiscriminative\nModels\nDiffusion\nModels …Sequence\nModels\n…\nSequence Modeling\nTokens",
    "metadata": {
      "has_images": false,
      "topic": "unknown",
      "page_start": 21,
      "material_type": "slides",
      "ocr_used": false,
      "chunk_ind": 20,
      "char_len": 224,
      "course_id": "1",
      "page_end": 21,
      "ocr_language": "",
      "relevancy_score": 0.4086800813674927
    }
  },
  {
    "text": "#2A6495\nA rt i fi c ia l I nt e ll ige n ce\nS u bs y mb oli c  AI\nStatiscial Methods Ensemble \nTechniques Neural Networks …\nGenerative\nModels\nDiscriminative\nModels\nDiffusion\nModels …Sequence\nModels\n…\nSequence Modelling\nEmbeddings",
    "metadata": {
      "ocr_used": false,
      "ocr_language": "",
      "page_start": 28,
      "has_images": false,
      "material_type": "slides",
      "course_id": "1",
      "chunk_ind": 27,
      "topic": "unknown",
      "page_end": 28,
      "char_len": 229,
      "relevancy_score": 0.3989182710647583
    }
  },
  {
    "text": "#2A6495\nGenerative Models\nDiscriminative Models\np(Y|X)\nGenerative Models\np(X, Y) or p(X)",
    "metadata": {
      "char_len": 88,
      "ocr_language": "",
      "ocr_used": false,
      "has_images": true,
      "chunk_ind": 17,
      "material_type": "slides",
      "page_end": 18,
      "page_start": 18,
      "course_id": "1",
      "topic": "unknown",
      "relevancy_score": 0.38038498163223267
    }
  }
]
~~~

---

## GenAI — Old Exam Questions: LLM/KG set of 5

~~~json
[
  {
    "question": "## Frage 13 **What makes the transformer architecture well-suited to sequential data modelling?** ",
    "question_type": "single-choice",
    "answer_keys": [
      "- [ ] a. Other than previous architectures, transformers can generalize across previously unseen",
      "languages without further pretraining.",
      "- [ ] b. Their attention mechanism makes them highly interpretable and transparent, unlike",
      "previous \"black box\" architectures like LSTMs.",
      "- [ ] c. They need little to no training data to learn the highly contextual semantics of sequences",
      "such as language.",
      "- [x] d. They can learn patterns from multiple parts/subsequences of a sequence simultaneously,",
      "rather than processing it sequentially.",
      "- [ ] e. Transformers are speciﬁcally designed to handle ﬁxed-length sequences, enhancing their",
      "performance with sequential data.",
      "---"
    ],
    "metadata": {
      "course_id": "1",
      "question_number": 13,
      "ocr_used": false,
      "has_choices": true,
      "char_len": 833,
      "page_start": 4,
      "ocr_languages_used": "",
      "topic": "unknown",
      "difficulty": "unknown",
      "page_end": 4,
      "chunk_ind": 12,
      "relevancy_score": 0.37377113103866577
    }
  },
  {
    "question": "## Frage 18 **What is a (are) some common reason(s) why LLMs may hallucinate or make mistakes?** ",
    "question_type": "multiple-choice",
    "answer_keys": [
      "- [x] a. An overgeneralization of statistical patterns in the training data.",
      "- [ ] b. Insuﬃcient computational resources during inference require the model to cut corners.",
      "- [ ] c. Syntax errors in the inference code.",
      "- [x] d. Adoption of incorrect information within the training data."
    ],
    "metadata": {
      "ocr_used": false,
      "char_len": 415,
      "course_id": "1",
      "question_number": 18,
      "has_choices": true,
      "chunk_ind": 17,
      "difficulty": "unknown",
      "topic": "unknown",
      "page_end": 5,
      "ocr_languages_used": "",
      "page_start": 5,
      "relevancy_score": 0.34658974409103394
    }
  },
  {
    "question": "## Frage 12 **What deﬁnes a token in the context of LLMs?** ",
    "question_type": "single-choice",
    "answer_keys": [
      "- [ ] a. The concept of tokens does not have a speciﬁc meaning in the context of LLMs.",
      "- [ ] b. A higher dimensional numerical identiﬁer for the whole sequence.",
      "- [x] c. The atomic unit of language that a model processes. This can be a word, part of a word, or",
      "a character.",
      "- [ ] d. The dense vector representation of the atomic unit of language processed by a transformer.",
      "- [ ] e. The smallest semantic unit of a language, which is always a single character.",
      "---"
    ],
    "metadata": {
      "topic": "unknown",
      "question_number": 12,
      "ocr_used": false,
      "difficulty": "unknown",
      "page_start": 3,
      "chunk_ind": 11,
      "char_len": 574,
      "page_end": 3,
      "ocr_languages_used": "",
      "course_id": "1",
      "has_choices": true,
      "relevancy_score": 0.33468055725097656
    }
  },
  {
    "question": "## Frage 2 **Which of these statement(s) about Knowledge Graphs (KGs) and LLMs is (are) CORRECT?** ",
    "question_type": "multiple-choice",
    "answer_keys": [
      "- [ ] a. KGs help bring generalizability to LLMs.",
      "- [x] b. KGs help bring domain-speciﬁc knowledge to LLMs.",
      "- [x] c. LLMs help bring language processing capabilities to KGs.",
      "- [ ] d. KGs can reduce the hardware requirements for training LLMs.",
      "- [ ] e. LLMs help avoid hallucinations in KGs.",
      "---"
    ],
    "metadata": {
      "has_choices": true,
      "topic": "unknown",
      "page_start": 1,
      "difficulty": "unknown",
      "question_number": 2,
      "course_id": "1",
      "char_len": 437,
      "page_end": 1,
      "ocr_languages_used": "",
      "chunk_ind": 1,
      "ocr_used": false,
      "relevancy_score": 0.32400214672088623
    }
  },
  {
    "question": "## Frage 16 **Which (What) statement(s) about the presented approach \"Tuning LLMs via KG Reasoning\" are CORRECT?** ",
    "question_type": "multiple-choice",
    "answer_keys": [
      "- [ ] a. The approach requires continuous access to the underlying knowledge graph during",
      "inference to maintain reasoning capabilities.",
      "- [x] b. It describes a way of using more than the original facts stored in the KG.",
      "- [x] c. The system incorporates a domain glossary to ensure accurate verbalization.",
      "- [x] d. Incorporates an LLM generating tokenized Q&A pairs from the verbalized templates.",
      "- [ ] e. It describes a way of incorporating graph structures into the attention layers.",
      "---"
    ],
    "metadata": {
      "ocr_languages_used": "",
      "topic": "unknown",
      "char_len": 653,
      "page_end": 4,
      "question_number": 16,
      "ocr_used": false,
      "course_id": "1",
      "has_choices": true,
      "chunk_ind": 15,
      "difficulty": "unknown",
      "page_start": 4,
      "relevancy_score": 0.31548231840133667
    }
  }
]
~~~

---

## GenAI — Generated Exam — Topic: Large Language Models

~~~json
{
  "course_id": 1,
  "course_name": "GenAI",
  "topics": "large language models",
  "n_requested": 5,
  "n_generated": 5,
  "context": {
    "course_material_chunks": 15,
    "old_exam_questions": 15
  },
  "questions": [
    {
      "question": "## Frage 19 **What is the primary goal of generative language modelling?**",
      "question_type": "single-choice",
      "answer_keys": [
        "a. To learn the conditional probability p(Y|X) for mapping inputs to specific output classes.",
        "b. To create explicit symbolic rules that can generate grammatically correct sentences.",
        "c. To capture the true distribution of language p(X) by modeling the probability of token sequences.",
        "d. To compress natural language sequences into fixed-length vector representations for downstream tasks."
      ],
      "metadata": {
        "topic": "Generative Language Modeling",
        "difficulty": "medium"
      }
    },
    {
      "question": "## Frage 20 **Which of the following statement(s) about discriminative and generative models is (are) CORRECT?**",
      "question_type": "multiple-choice",
      "answer_keys": [
        "a. Discriminative models learn p(X,Y) or p(X), making them suitable for generating new data samples.",
        "b. Generative models can be used for both generating new samples and performing classification tasks.",
        "c. Discriminative models learn p(Y|X), focusing on the decision boundary between classes.",
        "d. Generative models require less training data than discriminative models to achieve comparable performance."
      ],
      "metadata": {
        "topic": "Model Types",
        "difficulty": "medium"
      }
    },
    {
      "question": "## Frage 21 **According to the probability decomposition in generative language modeling, the probability of a sequence x = (s₁, s₂, ..., sₖ) is calculated as:**\n\n*p(x) = p(s₁) · p(s₂|s₁) · p(s₃|s₁,s₂) · ... · p(sₖ|s₁,...,sₖ₋₁)*\n\n**What does this formula represent?**",
      "question_type": "single-choice",
      "answer_keys": [
        "a. The sum of individual token probabilities normalized by sequence length.",
        "b. The product of the probability of the first token and the conditional probabilities of each subsequent token given all previous tokens.",
        "c. The joint probability distribution over all possible sequences in the vocabulary.",
        "d. The maximum likelihood estimate of token co-occurrence within a fixed context window."
      ],
      "metadata": {
        "topic": "Sequence Probability",
        "difficulty": "medium"
      }
    },
    {
      "question": "## Frage 22 **Which statement(s) about symbolic and subsymbolic AI is (are) CORRECT?**",
      "question_type": "multiple-choice",
      "answer_keys": [
        "a. Symbolic AI leverages mathematical models to learn patterns from data without requiring hand-crafted rules.",
        "b. Subsymbolic AI defines formal, humanly understandable symbols and employs explicit rules to draw logical conclusions.",
        "c. Symbolic AI employs explicit rules to draw logical conclusions from formal symbols.",
        "d. Subsymbolic AI uses mathematical models to learn patterns from data without hand-crafted rules."
      ],
      "metadata": {
        "topic": "AI Paradigms",
        "difficulty": "easy"
      }
    },
    {
      "question": "## Frage 23 **What is the key difference between sequence modeling and diffusion modeling in generative AI?**",
      "question_type": "single-choice",
      "answer_keys": [
        "a. Sequence models use a stochastic denoising process, while diffusion models process ordered sequences of discrete tokens.",
        "b. Sequence models process data as ordered sequences of discrete units mapped to embeddings, while diffusion models learn p(X) by iteratively denoising data.",
        "c. Sequence models are only applicable to language tasks, while diffusion models are designed exclusively for image generation.",
        "d. Sequence models require supervised learning with labeled data, while diffusion models are purely unsupervised."
      ],
      "metadata": {
        "topic": "Model Architectures",
        "difficulty": "medium"
      }
    }
  ]
}
~~~

---

## SQS — Slide Retrievals: Requirements-related (@k=5)

~~~json
[
  {
    "text": "56\nErfahrungsbasiertes Testen\n180.764 Software-Qualitätssicherung\nErwartet \n(explizit & implizit)\nImplementiertSpezifiziert",
    "metadata": {
      "has_images": true,
      "ocr_language": "",
      "chunk_ind": 54,
      "course_id": "2",
      "material_type": "slides",
      "page_start": 55,
      "page_end": 55,
      "char_len": 123,
      "topic": "unknown",
      "ocr_used": false,
      "relevancy_score": 0.3263434171676636
    }
  },
  {
    "text": "11\nDefinition – Software Qualität (nach ISO/IEC 25010)\n• ISO/IEC 25010 definiert ein Set an Qualitätsfaktoren und \nzugehörigen Qualitätskriterien\n• Qualitativ oder quantitativ messbar\n• Helfen bei der Spezifikation von Anforderungen\n• Ermöglichen Beurteilung des Erfüllungsgrades\n• Umfassendes Rahmenwerk zur Definition und Bewertung der \nSoftware Qualität\n• Projektumfeld und Domäne steuern den Stellenwert der \neinzelnen Qualitätsfaktoren\n• Unterteilung in zwei Untergruppen:\n• Funktionale Qualität\n• Strukturelle Qualität\n180.764 Software-Qualitätssicherung",
    "metadata": {
      "course_id": "2",
      "chunk_ind": 10,
      "ocr_language": "",
      "page_end": 11,
      "material_type": "slides",
      "char_len": 560,
      "page_start": 11,
      "has_images": true,
      "topic": "unknown",
      "ocr_used": false,
      "relevancy_score": 0.32524943351745605
    }
  },
  {
    "text": "12\nQualitätsfaktoren\nFunktionale Qualität\n• Die äußere Sicht (Benutzersicht) auf \nein System\n• Externe Merkmale des Systems\n• Definieren das “was?”\n• → Bezug zu funktionalen \nAnforderungen\nStrukturelle Qualität\n• Die innere Sicht auf ein System\n• Interne Merkmale und Eigenschaften \neines Systems\n• Definieren das “wie gut?”\n• → Bezug zu nicht-funktionalen \nAnforderungen\nFunktionale \nQualität\nStrukturelle\nQualität\n180.764 Software-Qualitätssicherung",
    "metadata": {
      "page_start": 12,
      "course_id": "2",
      "page_end": 12,
      "ocr_language": "",
      "chunk_ind": 11,
      "material_type": "slides",
      "ocr_used": false,
      "has_images": true,
      "char_len": 451,
      "topic": "unknown",
      "relevancy_score": 0.31999194622039795
    }
  },
  {
    "text": "36\nZusammenfassung\n• Die Qualität von Anforderungen trägt maßgeblich zum \nProjekterfolg bei, ihre Qualitätssicherung ist daher \nbesonders wichtig, um hohe Folgekosten zu vermeiden\n• Anforderungen können in funktional und nicht-funktional \nunterteilt werden\n• Reviews sind eine statische QS-Maßnahme, die eine \nsystematische Überprüfung div. Artefakte in einem SW-\nProjekt ermöglichen\n• Je nach Einsatzzweck stehen verschiedene Review-Typen \nzur Verfügung, die sich in Formalität, Rollen, Prozess und \nFlexibilität unterscheiden\n• Im Kontext von Code Reviews haben sich in den letzten \nJahren leichtgewichtige, toolgestützte Ansätze \ndurchgesetzt, die sich gut in den Arbeitsalltag der \nEntwicklung integrieren lassen\n180.764 Software-Qualitätssicherung",
    "metadata": {
      "course_id": "2",
      "chunk_ind": 35,
      "material_type": "slides",
      "page_start": 36,
      "ocr_used": false,
      "char_len": 752,
      "ocr_language": "",
      "has_images": true,
      "page_end": 36,
      "topic": "unknown",
      "relevancy_score": 0.3178445100784302
    }
  },
  {
    "text": "13\nQualitätsfaktoren\nBeispiel – Befundsystem\nIhr Unternehmen wurde mit der Entwicklung eines Befundsystems \nbeauftragt, das Patienten und Ärzten Laborbefunde bereitstellen soll.\nWelche (strukturellen) Qualitätsfaktoren haben hier besonders hohen \nStellenwert und warum? \n180.764 Software-Qualitätssicherung\n→ Sicherheit: es handelt sich um personenbezogene, sensible medizinische Daten\n→ Benutzbarkeit: es handelt sich um eine heterogene Benutzergruppe, die nicht zwingend technischen Background hat\n→ Zuverlässigkeit: Stabilität und hohe Verfügbarkeit, um das Tagesgeschäft abwickeln und rasch reagieren zu können\nKonkrete Aussagen, z.B. \n• „Laborbefunde sollen innerhalb von 3 Klicks abgerufen werden können“\n• „Das System soll eine Verfügbarkeit von 95% innerhalb der Kernzeiten (6-18 Uhr) haben“\n• „Verbindungen müssen per TLS abgesichert werden“",
    "metadata": {
      "ocr_language": "",
      "material_type": "slides",
      "page_end": 13,
      "page_start": 13,
      "ocr_used": false,
      "char_len": 850,
      "topic": "unknown",
      "has_images": true,
      "chunk_ind": 12,
      "course_id": "2",
      "relevancy_score": 0.30971354246139526
    }
  }
]
~~~

---

## SQS — Old Exam Questions (text-answer set of 5)

~~~json
[
  {
    "question": "8. Ablauf eines Reviews von Anforderungen erklären und skizzieren.",
    "question_type": "text-answer",
    "answer_keys": null,
    "metadata": {
      "ocr_used": false,
      "topic": "unknown",
      "difficulty": "unknown",
      "course_id": "2",
      "page_start": 1,
      "chunk_ind": 7,
      "page_end": 1,
      "question_number": 8,
      "has_choices": false,
      "ocr_languages_used": "",
      "char_len": 66,
      "relevancy_score": 0.3227834701538086
    }
  },
  {
    "question": "8. Ablauf eines Reviews von Anforderungen erklären und skizzieren. Planung: Objekt, Prüfziele, Auslösekriterien (Einstiegskriterien), Teilnehmer, Ort, Zeit. Vorbesprechung: Vorstellung des Prüfobjekts bei komplexen und neuen Produkten. Intensive Einzeldurcharbeitung Durchführung: Gemeinsames Lesen, Aufzeichnung von Mängeln; während des Reviews sollen Mängel entdeckt, nicht korrigiert werden. In der Nachbearbeitung werden dokumentierte Mängel korrigiert und in der Bewertung überprüft. Berichterstattung. Wiederholungen von Reviews sind möglich. Checklisten unterstützen Reviews. Typische Dauer: 2h",
    "question_type": "text-answer",
    "answer_keys": null,
    "metadata": {
      "ocr_used": false,
      "course_id": "2",
      "ocr_languages_used": "",
      "question_number": 30,
      "has_choices": false,
      "topic": "unknown",
      "chunk_ind": 29,
      "char_len": 601,
      "difficulty": "unknown",
      "relevancy_score": 0.2943604588508606
    }
  },
  {
    "question": "13. 6 Leistungen der QS-Stelle aufzählen Qualitätsplanung als Teil der Projektplanung. Herstellen lokaler Standards auf Projekt- und Organisationsebene. Review zentraler Projektdokumente. Organisieren von Reviews: Ausbildung, Planung, Durchführung, Verbesserungsvorschläge. Unterstützung bei Personalauswahl und Software-Zukauf. Vorbereitung und Auswertung von Produkttests.",
    "question_type": "text-answer",
    "answer_keys": null,
    "metadata": {
      "ocr_used": false,
      "page_end": 8,
      "course_id": "2",
      "chunk_ind": 34,
      "page_start": 8,
      "has_choices": false,
      "topic": "unknown",
      "difficulty": "unknown",
      "ocr_languages_used": "",
      "char_len": 374,
      "question_number": 35,
      "relevancy_score": 0.2789250612258911
    }
  },
  {
    "question": "6. Teststufen den Beschreibungen zuordnen (Komponententest, Integrationtest, Systemtest, Akzeptanztest, Lasttest, Regressionstest)",
    "question_type": "text-answer",
    "answer_keys": null,
    "metadata": {
      "question_number": 6,
      "chunk_ind": 5,
      "page_start": 1,
      "has_choices": false,
      "page_end": 1,
      "char_len": 130,
      "course_id": "2",
      "ocr_languages_used": "",
      "topic": "unknown",
      "ocr_used": false,
      "difficulty": "unknown",
      "relevancy_score": 0.27617204189300537
    }
  },
  {
    "question": "9. Nennen und beschreiben Sie 4 ISTQB Testprinzipien.",
    "question_type": "text-answer",
    "answer_keys": null,
    "metadata": {
      "course_id": "2",
      "chunk_ind": 8,
      "topic": "unknown",
      "ocr_used": false,
      "char_len": 53,
      "ocr_languages_used": "",
      "page_start": 1,
      "page_end": 1,
      "difficulty": "unknown",
      "has_choices": false,
      "question_number": 9,
      "relevancy_score": 0.26180601119995117
    }
  }
]
~~~

---

## SQS — Generated Exam — Topic: Requirements

~~~json
{
  "course_id": 2,
  "course_name": "SQS",
  "topics": "requirements",
  "n_requested": 5,
  "n_generated": 5,
  "context": {
    "course_material_chunks": 15,
    "old_exam_questions": 15
  },
  "questions": [
    {
      "question": "Erklären Sie den Unterschied zwischen funktionaler Qualität und struktureller Qualität gemäß ISO/IEC 25010. Geben Sie jeweils ein Beispiel für einen Qualitätsfaktor aus beiden Kategorien.",
      "question_type": "text-answer",
      "answer_keys": null,
      "metadata": {
        "topic": "Software Qualität",
        "difficulty": "medium"
      }
    },
    {
      "question": "Welche Aussagen über Qualitätssicherung in der Softwareentwicklung sind korrekt?",
      "question_type": "multiple-choice",
      "answer_keys": [
        "QS ist ein kontinuierlicher Prozess, der alle Phasen der Softwareentwicklung begleitet",
        "Qualität kann am Ende eines Projekts ohne hohe Kosten hinzugefügt werden",
        "QS-Aktivitäten finden in jedem Vorgehensmodell Anwendung",
        "Reviews sind eine dynamische QS-Maßnahme zur Überprüfung von Artefakten"
      ],
      "metadata": {
        "topic": "Software Qualitätssicherung",
        "difficulty": "medium"
      }
    },
    {
      "question": "Ihr Unternehmen entwickelt eine Online-Banking-Anwendung für eine große Bank. Nennen Sie mindestens drei strukturelle Qualitätsfaktoren, die in diesem Projekt besonders hohen Stellenwert haben, und begründen Sie jeweils kurz warum.",
      "question_type": "text-answer",
      "answer_keys": null,
      "metadata": {
        "topic": "Qualitätsfaktoren",
        "difficulty": "medium"
      }
    },
    {
      "question": "Was bedeutet Verifikation im Kontext der Software-Qualitätssicherung nach IEEE-730?",
      "question_type": "single-choice",
      "answer_keys": [
        "Bauen wir das richtige Produkt? - Konformität gegenüber dem vorgesehenen Zweck und den Bedürfnissen der Stakeholder",
        "Bauen wir das Produkt richtig? - Konformität gegenüber den spezifizierten Anforderungen",
        "Testen wir alle Funktionen? - Vollständige Überprüfung aller Systemkomponenten",
        "Erfüllen wir die Zeitvorgaben? - Einhaltung der Projekttermine"
      ],
      "metadata": {
        "topic": "Verifikation und Validierung",
        "difficulty": "easy"
      }
    },
    {
      "question": "Welche der folgenden Aussagen zu Mehrfach-Bedingungsüberdeckungstests sind korrekt?",
      "question_type": "multiple-choice",
      "answer_keys": [
        "Es werden alle Wahrheitswertekombinationen der atomaren Teilentscheidungen getestet",
        "Bei zwei atomaren Bedingungen werden genau 4 Testfälle benötigt",
        "Mehrfach-Bedingungsüberdeckung ist eine Form der erfahrungsbasierten Testmethode",
        "Die Anzahl der Testfälle steigt exponentiell mit der Anzahl der atomaren Bedingungen"
      ],
      "metadata": {
        "topic": "Testverfahren",
        "difficulty": "hard"
      }
    }
  ]
}
~~~