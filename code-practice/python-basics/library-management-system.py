# ==================== 图书管理系统 ====================
books = {}#定义字典，字典是一种键值对（key-value）存储结构，类似于现实中的"通讯录"（名字 → 电话号码）。
def generate_book_id():#定义一个生成书籍id的函数
    count = len(books)#获取字典中已有的书籍数量，Python 的内置数据类型（列表、字符串、字典、元组等）都统一使用 len() 来获取长度，保持了接口的一致性。
    return "B" + str(count + 1).zfill(3)#return结束后会把值扔回给调用者，zfill(width) 是字符串方法，用于在字符串左侧填充 0 直到达到指定宽度

def add_book():#定义一个增加图书功能的函数
    print("\n--- 添加新书 ---")
    title = input("请输入书名：").strip()#strip()表示去除两端空白，.lstrip()表示去除左端，.rstrip()表示去除左端，.strip("x")表示去除指定x符
    author = input("请输入作者：").strip()#strip()存在的意义是用户输入的字符串可能多种多样，系统录入就会不一样，所以需要.strip（）把字符串去掉首位统一
    
    if not title or not author:
        print("❌ 书名和作者不能为空！")
        return#return后面为空表示立即退出函数，不返回任何值，与刚才这个代码return "B" + str(count + 1).zfill(3)相比，return "B" + str(count + 1).zfill(3)则代表立即退出函数并返回书的编号值给调用者。
    
    book_id = generate_book_id()#设置book_id的意义，book_id是一个变量，gererate_book_id()是函数，每次调用它都会运行一次函数，所以需要设置一个变量把当前这个函数运行的结果保留下来。（也就是变量基于函数赋予的，函数赋予的值它不会变，但是如果是调用函数的话就会每次调用都不一样）
    book_info = { #info是information的意思
        "title": title,
        "author": author,
        "borrowed": False
    }
    books[book_id] = book_info#用[]，[] 的作用就是 "根据位置/编号，找到对应的东西"，[]前面就是位置的地方
    print(f"✅ 添加成功！书号：{book_id}，书名：《{title}》")#f""是f-string,字符串格式化语法{book_id}和{title}用{}是因为{}定义字典、f-string插变量

def delete_book():
    print("\n--- 删除图书 ---")
    book_id = input("请输入要删除的书号（如 B001）：").strip().upper()#upper()统一小写转换成大写，它和scrip()都属于方法，之前学的zfill(3)也是
    
    if book_id in books:
        title = books[book_id]["title"]
        confirm = input(f"确认删除《{title}》吗？(y/n)：").strip().lower()
        
        if confirm == "y":
            del books[book_id]
            print(f"✅ 已删除         《{title}》")
        else:
            print("⏹ 已取消删除")
    else:
        print("❌ 未找到该书号！")#这里的else是跟外层的if book_id in books:两者是联动的，代表如果在书库里面找不到编号。

def update_book():
    print("\n--- 修改图书信息 ---")
    book_id = input("请输入要修改的书号：").strip().upper()
    
    if book_id not in books:
        print("❌ 未找到该书号！")
        return#这里直接return的原因，即提前返回的核心思想：先把所有"错误情况"处理掉，然后干净地写"正常逻辑"。（程序员喜欢的方法）
    
    book = books[book_id]#上述return已经提前退出，直接紧接着执行这段代码
    print(f"当前信息：书名：《{book['title']}》 作者：{book['author']}")
    
    new_title = input("请输入新书名（直接回车保留原值）：").strip()#所以input=前面的变量名就是前端会自动翻译成中文对吗？但是这个英文要拼写正确
    new_author = input("请输入新作者（直接回车保留原值）：").strip()#一个变量只能存一个值，一旦被覆盖，旧值就再也找不回来了，所以这里出现新书名、新作者就要重新生成变量名。不可以理解为有新名词出现就有新变量，新名词 ≠ 新变量。变量是用来存储需要反复使用的数据的，而不是给每个名词都创建一个变量。
    
    if new_title:
        book["title"] = new_title
    if new_author:
        book["author"] = new_author
    
    print("✅ 图书信息已更新！")

def list_books():
    print("\n--- 全部图书列表 ---")
    if not books:
        print("📭 当前没有图书")
        return
    
    print(f"{'书号':<8} {'书名':<15} {'作者':<10} {'状态':<8}")
    print("-" * 45)
    for book_id, info in books.items():
        status = "已借出" if info["borrowed"] else "可借阅"
        print(f"{book_id:<8} {info['title']:<15} {info['author']:<10} {status:<8}")

def search_book():
    print("\n--- 搜索图书 ---")
    keyword = input("请输入搜索关键词（书名或作者）：").strip()
    if not keyword:
        print("❌ 关键词不能为空！")
        return
    
    results = []
    for book_id, info in books.items():
        if keyword.lower() in info["title"].lower() or keyword.lower() in info["author"].lower():
            results.append((book_id, info))
    
    if results:
        print(f"找到 {len(results)} 本相关图书：")
        print(f"{'书号':<8} {'书名':<15} {'作者':<10} {'状态':<8}")
        print("-" * 45)
        for book_id, info in results:
            status = "已借出" if info["borrowed"] else "可借阅"
            print(f"{book_id:<8} {info['title']:<15} {info['author']:<10} {status:<8}")
    else:
        print("❌ 未找到匹配的图书")

def borrow_book():
    print("\n--- 借阅图书 ---")
    book_id = input("请输入要借阅的书号：").strip().upper()
    
    if book_id not in books:
        print("❌ 未找到该书号！")
        return
    
    book = books[book_id]
    if book["borrowed"]:
        print(f"❌ 《{book['title']}》已被借出，无法再次借阅")
    else:
        book["borrowed"] = True
        print(f"✅ 成功借阅《{book['title']}》")

def return_book():
    print("\n--- 归还图书 ---")
    book_id = input("请输入要归还的书号：").strip().upper()
    
    if book_id not in books:
        print("❌ 未找到该书号！")
        return
    
    book = books[book_id]
    if not book["borrowed"]:
        print(f"❌ 《{book['title']}》未被借出，无需归还")
    else:
        book["borrowed"] = False
        print(f"✅ 成功归还《{book['title']}》")

def show_menu():
    print("\n" + "=" * 35)
    print("      📚 图书管理系统")
    print("=" * 35)
    print("1. 添加图书")
    print("2. 删除图书")
    print("3. 修改图书信息")
    print("4. 查看全部图书")
    print("5. 搜索图书")
    print("6. 借阅图书")
    print("7. 归还图书")
    print("0. 退出系统")
    print("-" * 35)

def main():
    print("欢迎使用图书管理系统！")
    books["B001"] = {"title": "Python入门", "author": "张三", "borrowed": False}
    books["B002"] = {"title": "数据结构", "author": "李四", "borrowed": True}
    books["B003"] = {"title": "算法导论", "author": "王五", "borrowed": False}
    print("已加载示例数据，输入对应数字进行操作。")
    
    while True:
        show_menu()
        choice = input("请输入操作编号：").strip()
        
        if choice == '1':
            add_book()
        elif choice == '2':
            delete_book()
        elif choice == '3':
            update_book()
        elif choice == '4':
            list_books()
        elif choice == '5':
            search_book()
        elif choice == '6':
            borrow_book()
        elif choice == '7':
            return_book()
        elif choice == '0':
            print("感谢使用，再见！")
            break
        else:
            print("❌ 无效输入，请重新选择")
        
        input("\n按 Enter 键继续...")

if __name__ == "__main__":
    main()