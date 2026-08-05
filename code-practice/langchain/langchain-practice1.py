import os
from dotenv import load_dotenv
load_dotenv()
from langchain.chat_modles import init_chat_model
#从langchain这个大包下，进入chat_models这个子模块，从子模块中导入init_chat_model这个函数，全称initialize（初始化）_chat_model,它是聊天模型的万能启动器，核心作用是统一、简便地初始化各种不同厂商的聊天模型，可以理解为“聊天模型的万能启动器”。在没有它之前，每用一个别的模型就要重新导入一次，现在就只需要加上一段代码，model=init_chat_model("claude-3-sonnet",model_provider="anthropic")这样的表述，不然旧方式就要从重新导入from langchain_anthropic import ChatAnthropic这样，如何再配置model=ChatAnthropic(model="claude-3",api_key="...")
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder#template是模板的意思，ChatPromptTemplate聊天提示模板
#ChatPromptTemplate:结构化的对话脚本，它指定了每条消息在对话中的角色。一个典型的对话模板长这样：
# prompt=ChatPromptTemplate.from_messages（[
# ("system","你是一位精通（领域）的专家，请用专业且友好的语气回答问题。")]，
# ("human","你好，我想咨询一下（问题）。")
#])
#ChatPromptTemplate的核心作用是定义整个对话的结构和流程，核心目的就是为了在写代码时避免角色混乱、同时能实现提示词复用。在langchain的对话体系里面，标准的角色主要有;system系统、human用户、AI助手，将多个角色的消息，按照对话发生的先后顺序，组装成一个结构化的列表。
#langchain_core是整个langchain生态系统的基础核心库，里面装满了搭建 AI 应用所需的各种基础工具。
#from langchain_core.prompts import ChatPromptTemplate ,"从 langchain_core 这个包（工具箱）里面，找到 prompts 这个模块（文件），再从 prompts 这个模块里面，找到 ChatPromptTemplate 这个类（具体工具）。"
#from langchain_core.prompts import ChatPromptTemplate,MessagePlaceholder #从LangChain核心包的"提示词"工具包里，拿出"聊天提示词模板"和"消息占位符"这两个工具。从 LangChain 核心库的 prompts（提示词）工具箱里，拿出两个工具：ChatPromptTemplate 和 MessagesPlaceholder，准备在我的代码里使用。
#ChatPromptTemplate是一个对话的框架，规定了谁说话、说的顺序、哪些话是固定的。代表把对话框架框死了；messagesplaceholder是留白位置，代表之前可以用它把之前某段历史对话插入进来。
#template=ChatPromptTemplate.from_messages([ 
#   ("system","你是一个python编程助手")，（)里面装的是函数的参数/元组、[]方括号/中括号装的是有顺序的列表、{}花括号/大括号装的是字典、集合；“”''引号装的是文字（字符串）。
#   ("human","{user_input}"),
#   ("ai","好的，我；来帮你把这个问题解决了")
#])
#写代码时，所有符号（引号、括号、逗号、等号）都用英文输入法打。只有注释和字符串内容（用户看的文字）可以用中文。
#观察到ChatPromptTemplate的C/P/T是大写，这种写法就是“大驼峰命名法”。每个词首字母大写，代表类，它是一种编程惯例。全小写代表变量/函数/方法，如book_id/user_name/format_meaaages()
#message =template.format_messages(
#   user_input="如何定义列表？"
#)
from langchain_core.output_parsers import StrOutParser #这句代码是从 LangChain 的工具箱里，拿出一个叫 StrOutputParser 的工具。StrOutputParser是“字符串输出解析器”工具。"把 AI 的回答整理成纯文字"的解析器。
from langchain.chains import create_retrieval_chain #create_retrieval_chain = "把『检索系统』和『问答系统』串联成一条流水线"的工厂函数。就是一条"信息传送带"（链子），把各个环节（检索、检索、问答）串起来，让数据像流水一样自动往下走。
from langchain.chains.combine_documents import create_stuff_document_chain#也就是有一个提示词模板，然后这个函数把检索到的信息和提示词模板连接起来组成一个链。
from langchain_community.docunment_loaders import PyPDFloader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings



model=init_chat_model(model='deepseek:deepseek-v4-flash',temperature=0.3)#temperature是控制“AI创造力”或“随机性'的一个按钮，越低，AI的回答越保守，这个名字来源于物理学里的"温度"概念：温度高，分子越活跃，越低分子越稳定。
#init_chat_model = "初始化聊天模型"，"启动聊天 AI 模型"——就像打开一台机器，让它进入待命状态，准备回答用户的问题。 
rag_prompt=ChatPromptTemplate.from_message ([ #rag_prompt变量名，存储创建的提示词模板对象，ChatPromptTemplate是类名，用这个类来创建模板对象。Python 本身就有"类"（Class）这个概念！ ChatPromptTemplate 是 LangChain 这个第三方库中定义的类，但它遵循的正是 Python 原生的类语法和机制。也就是langchain中的类可以直接沿用到python中，他们两个不分家（langchain中的类。本质上就是python类——只是它由第三方库定义，不是python自带），python是房子地基，langchain是python框架上建起来的工具库。
    ("system","你是一个助手，请参考以下上下文回答：(context)"),
    MessagesPlaceholder(variable_name="chat_history"),#这里variable_name是MessagesPlaceholder这个类里面预先定义好的固定参数名，是固定的，variable_name是“留白位置”起的变量名，chat_history就是在里面天的内容叫chat_history,只不过chat_history还没有定义
    ("human","{input}")#元组代表一组固定搭配好的数据，顺序固定。比如（1、2),(3,4)这两个元组里面的1、3都代表角色，2、4都代表内容。元组的作用就是让程序能稳定地按顺序取值，不会搞混。因为也可以换字典来表达，如{"role":"system","centent":"内容"}，而按键名：["role"]、["content"]是通过标签名去柜子里取东西，比较复杂，相对来说元组更轻量更快。
])#字典（Dictionary）就是一个"带标签的柜子"——每个格子上贴着一个"标签（键）"，格子里放着"内容（值）"，你想拿东西就喊标签名字。
#{
 #   "title": "Python入门",    # 标签"title" → 内容"Python入门"
#    "author": "张三",         # 标签"author" → 内容"张三"
#    "borrowed": False        # 标签"borrowed" → 内容False
#}
#Python 字典就是"程序世界里的词典"——通过一个词（键）找到对应的解释（值）。字典 = "带标签的柜子" = "程序世界的词典" —— 通过"标签/词（键）"找到对应的"内容/解释（值）"。用 { } 表示，用 : 连接键和值，用 , 分隔不同的组合。 
parser=StrOutputParser()#第24行把StrOutputParser类名引出来了，纯Python本质：parser = 某个类()，标准的类实例化。整行翻译：创建一个"字符串输出解析器"对象，存入变量 parser。
basic_chain=rag_template|model|parser #|是管道符/或，python的运算符重载，在这里表示”串联“，整行翻译：把"提示词模板"、"AI模型"、"输出解析器"三个组件用管道符串联成一条流水线，存入变量 basic_chain
document_chain=create_stuff_document_chain(model,rag_template)#整行翻译：调用 create_stuff_documents_chain 函数，传入 model 和 rag_template，创建一个"文档填充问答链"，存入变量 document_chain。纯Python本质：document_chain = 某个函数(模型对象, 模板对象)。函数后面的 ( ) 就像一个"原料投料口"，括号里的参数就是"扔进去的原料"，函数拿到这些原料后按照预设的流程加工，最终产出结果。
loader=PyPDFloader("./sample.pdf")
docs=loader.load()
print(f"成功加载{len(docs)}页文档。")
text_splitter=RecursiveCharacTextSplitter(
    chunk_size=500,
    chunk_overlap=80
)
chunks=text_splitter.split_documents(os)
peint(f"文档被分割为{len(chunks)}个文本块。")
vectorstore=Chroma.from_documents(
documents=chunks,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)
print("向量库构建完成,已保存到./chroma_db")
retriever=vectorstore.as_retriever(search_kwargs={"k":3})#vector=向量，store=存储，vectorstore变量名（假设前面创建过），指向向量数据库对象。as=作为，retriever=检索器，as_retriever方法名，把向量库对象"转换"成一个检索器对象
rag_chain=create_retrieval_chain(retriever,document_chain)#rag_chain变量名，存储最终的RAG系统；函数名，把"检索器"和"问答链"组装成完整RAG；retriever检索器，参数1，传入检索器对象；document_chain文档链，参数2，传入文档问答链对象。纯Python本质：rag_chain = 组装函数(检索器, 问答器)。整行翻译：调用 create_retrieval_chain 函数，把 retriever 和 document_chain 组装成一个完整的RAG系统，存入变量 rag_chain。
result=rag_chain.invoke({"input":"这份文档讲了什么？"})#invoke调用/执行，它是python中固定的调用函数吗？invoke 是 LangChain 中几乎所有"链"和"模型"对象都通用的一个方法，意思是"启动/调用这个工具，它不是 Python 内置的通用函数，而是 LangChain 框架定义的标准方法，专门用来启动 AI 工作流。
print("AI助手:",result['answer'])#打印结果中的answer的内容

